# 8percent-assignment-2



**✔️ API 목록**

- 거래내역 조회 API
- 입금 API
- 출금 API


---
## 기술적 고려사항

1. 잔액의 무결성 보장  
   트랜잭션의 무결성을 유지하도록 설계가 되어야한다. 이러기 위해서는 원자성, 일관성, 고립성, 지속성이 유지가 되어야한다.
   1) **원자성**이 보장되기 위해, atomic을 수행한다.
         기본적으로 장고는 auto_commit이다.   
         이에 따라 해당 계좌에 가서, 잔액을 바꾸고, 거래내역을 등록하는 이 2가지 행위가 각각 이루어질 우려가 있으므로, with transaction.atomic()을 넣어줘야 한다.
   2) **일관성**같은 경우는 테이블이 생성될 때  명시되므로, 크게 신경 쓸 필요없다.
 
   3) **고립성**을 보장하기 위해, 동시성 제어를 한다.(concurrency control)
      - 은행이니 만큼, 최고수준의 격리를 하여서 안정성을 확보해야한다.
      - main db 와 replication db로 나누어서, write, update는 main에서만 하고, read는 replication db 에서만 가능하게 한다.
      - 쓰기와 관련된 충돌은 select_for_update()를 통해서 방지한다.
      - 읽기/읽기와 관련된 충돌은 고립수준을 serializable 모드로 하여서 방지한다.
   4)  **지속성**을 보장하기 위해서, 회복(recovery)기능을 도입해야한다.
aws-rds를 사용하여서 회복가능하도록 설정하였다.
    
    
2. 1억건 데이터일 경우  
    1) 인덱스 설정:  
       거래방식(입금인지,출금인지)과 계좌번호로 인덱싱하였음.
    2) db 파티셔닝:   
       transaction 데이터들을 월별로 partitioning을 하였다. 그 이유는 사람들이 잔액조회를 할 때 단위가 1개월, 3개월등  개월 단위이기 때문이다.(카카오뱅크 기준.)


---
## DB를 설계 할때 각 칼럼의 타입과 제약

### User Table
| column name | 컬럼 이름   | data type   | 제약조건  | 이유    |
| ---------- | ---------- | ----------- | -------- |-------- |
| id         | 유저 아이디 | INT         | PK       | 일단 분산db가 아니므로 UUID대신 pk로 설정함.
| name       | 이름       | VARCHAR(10) | NotNull  | 법적으로 성을 제외한 이름이 5글자로 정해져있지만, 추후 법개정 가능성등을 염두에 두고 10자로 잡음.
| password   | 비밀번호    | VARCHAR(100) | NotNull  | -
|
</br>

### Account Table
| column name | 컬럼 이름   | data type   | 제약조건  | 이유     |
| ---------- | -----------| ----------- | -------- |-------- |
| id         | id | INT         | PK       | 일단 분산db가 아니므로 UUID대신 pk로 설정함.
| account    | 계좌번호    | CHAR      | NotNull       | 최대 20자리까지 표현하는 데이터 타입. (현재 14자리이므로 넉넉하게 20자리로 설정)|
| balance    | 잔액        | POSITIVEBIGINT      | NotNull  | 원단위 특성상 100억이상이 가능하고, 무조건 0이상이므로 positiviebiginteger로 설정함.
| created_at | 만든시각    | DATETIME    | NotNull  | 값 자동 부여
| userId     | 유저 아이디 | INT         | FK       | user가 지워지더라도 남겨두도록 하였는데, 현행법상 5년까지 보관해야하기 때문이다.
</br>

### Transaction Table
| column name   | 컬럼 이름   | data type   | 제약조건  | 이유     |
| ------------ | --------- | ----------- | -------- |-------- |
| id         | id | INT         | PK       | 일단 분산db가 아니므로 UUID대신 pk로 설정함.
| account      | 계좌번호    | CHAR      |    | partition시 fk설정이 불가능하여서 fk설정은 안하였다.
| created_at         | 거래일시    | DATETIME    | PK       | 
| amount | 거래금액    | POSITIVEBIGINT      | NotNull  | -
| balance      | 잔액       | BIGINT      | NotNull  | 나중에 마이너스 통장도 가능하므로 big int로 함.
| transaction_type   | 출/입금    | INT     | NotNull  | partition시 fk설정이 불가능하여서 fk설정은 안하였다.
| description         | 적요    | VARCHAR(7)   |         | 실제 은행들에서 최대 7글자만 기록한다는 것을 보고 최대 크기를 정함.
| counterparty         | 상대방    | VARCHAR(10)   |   NotNull      | 입출금시 대상이 필요할것 같아서 추가하였다.



### TransactionType Table
| column name   | 컬럼 이름   | data type   | 제약조건  | 이유     |
| ------------ | --------- | ----------- | -------- |-------- |
| id         | id | INT         | PK       | 일단 분산db가 아니므로 UUID대신 pk로 설정함.
| type         | 거래타입    | POSITIVE SMALL INTEGER    |    NOT NULL    | ENUM타입으로 대출 등 새로운 거래 유형이 추가될 수있는 것을 대비하고자 하였다.

---



## 모델링
<img width="787" alt="스크린샷 2021-11-11 오후 6 11 51" src="https://user-images.githubusercontent.com/70747064/141466644-eb3982f9-3aa9-40dd-9129-e837fbc2e051.png">

---

## 보완할 점
 1. 입출금을 많이 하거나, transaction test 수를 많이 늘리면,  django.db.utils.OperationalError: (2006, '')
 가 나고 있다.  
 2006에러가 mysql server가 꺼졌다는 에러인것 같아서, https://aws.amazon.com/ko/premiumsupport/knowledge-center/rds-mysql-server-gone-away/
 시키는대로 다해봤지만 아직 해결안되는중,  

2. django 스럽게 user 관리하기
3. counterpart빼기. (입출금이지, 입금 송금이 아니므로,)

## Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8에서 출제한 과제를 기반으로 만들었습니다.
