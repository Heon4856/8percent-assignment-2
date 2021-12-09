# 8percent-assignment-2



**✔️ API 목록**

- 거래내역 조회 API
- 입금 API
- 출금 API


---
## 기술적 고려사항

1. 잔액의 무결성 보장  
   트랜잭션의 무결성을 유지하도록 설계가 되어야한다.

이러기 위해서는 원자성, 일관성, 고립성, 지속성이 유지가 되어야한다.

 

1) 원자성이 보장되기 위해, atomic을 수행한다.
기본적으로 장고는 auto_commit이다.

이에 따라 해당 계좌에 가서,  잔액을 바꾸고, 거래내역을 등록하는 이 2가지 행위가 각각 이루어질 우려가 있으므로,

with transaction.atomic()을 넣어줘야 한다.

 

2) 일관성 같은 경우는 테이블이 생성될 때  명시되므로, 크게 신경 쓸 필요없다.
 

3) 고립성을 보장하기 위해, 동시성 제어를 한다.(concurrency control)
-은행이니 만큼, 최고수준의 격리를 하여서 안정성을 확보해야한다.

-main db 와 replication db로 나누어서, write, update는 main에서만 하고, read는 replication db 에서만 가능하게 한다.

-쓰기와 관련된 충돌은 select_for_update()를 통해서 방지한다.

-읽기/읽기와 관련된 충돌은 고립수준을 serializable 모드로 하여서 방지한다.


4.  지속성을 보장하기 위해서, 회복(recovery)기능을 도입해야한다.
aws-rds를 사용하여서 회복가능하도록 설정하였다.
    
    
2. 1억건 데이터일 경우  
    1) 인덱스 설정
    2) db 파티셔닝: transaction 데이터들을 월별로 partitioning을 하였다. 그 이유는 사람들이 잔액조회를 할 때 단위가 1개월, 3개월등  개월 단위이기 때문이다.(카카오뱅크 기준.)


---

## 모델링
<img width="787" alt="스크린샷 2021-11-11 오후 6 11 51" src="https://user-images.githubusercontent.com/70747064/141466644-eb3982f9-3aa9-40dd-9129-e837fbc2e051.png">

---


## Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8에서 출제한 과제를 기반으로 만들었습니다.
