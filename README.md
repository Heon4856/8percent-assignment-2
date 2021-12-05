# 8percent-assignment-2

---
## 과제 출제 기업 정보
- 기업명 : 8퍼센트
- 8퍼센트 사이트 : https://8percent.kr/
- 원티드 채용 링크 : https://www.wanted.co.kr/wd/64695

---


**✔️ API 목록**

**POSTMAN Documentation**
https://www.postman.com/binooooo/workspace/1aa44ed7-4d2d-4563-ae5d-c1df4ba97e72/documentation/14665666-ed8f4018-6736-4c14-b60a-4af46f3fcb55

---

- 거래내역 조회 API
- 입금 API
- 출금 API

**✔️ 주요 고려 사항은 다음과 같습니다.**

---

- 계좌의 잔액을 별도로 관리해야 하며, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장
- DB를 설계 할때 각 칼럼의 타입과 제약

**✔️ 구현하지 않아도 되는 부분은 다음과 같습니다.**

---

- 문제와 관련되지 않은 부가적인 정보. 예를 들어 사용자 테이블의 이메일, 주소, 성별 등
- 프론트앤드 관련 부분

**✔️  제약사항은 다음과 같습니다.**
- (**8퍼센트가 직접 로컬에서 실행하여 테스트를 원하는 경우를 위해**) 테스트의 편의성을 위해 mysql, postgresql 대신 sqllite를 사용해 주세요.
(상세 설명 생략)

---
## 기술적 고려사항
1. 잔액의 무결성 보장  
    transaction-atomic사용  
    
2. 1억건 데이터일 경우  
    1) 인덱스 설정
    2) pk를 yyyymmdd*1000000000 + (transaction데이터의 pk%1000000000)+1 로 설정하였음.
이를 통해 기간을 통한 검색을 효율화하였음.
실제로 100만건의 데이터로 실험한 결과 
0.55초 --> 0.4초대로 낮출수 있었음
<img width="495" alt="스크린샷 2021-11-13 오전 3 23 55" src="https://user-images.githubusercontent.com/13060192/141516264-7d50745a-36eb-435a-8553-36a1346fcf10.png">

<img width="523" alt="스크린샷 2021-11-12 오후 8 25 01" src="https://user-images.githubusercontent.com/13060192/141516279-f35ab718-cfba-4bad-865b-8222099e3554.png">



---

## 모델링
<img width="787" alt="스크린샷 2021-11-11 오후 6 11 51" src="https://user-images.githubusercontent.com/70747064/141466644-eb3982f9-3aa9-40dd-9129-e837fbc2e051.png">

---


## 배포 도커 실행방법

## Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8에서 출제한 과제를 기반으로 만들었습니다.
