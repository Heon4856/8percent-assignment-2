# 8percent-assignment-2



**✔️ API 목록**

- 거래내역 조회 API
- 입금 API
- 출금 API


---
## 기술적 고려사항
0. 아직 진행중인 사항
Read db와 write db를 분리 -- >진행중
파티셔닝 --> 1억건일경우를 대비하여.

1. 잔액의 무결성 보장  
    transaction-atomic사용  
   select_for_update() 사용.
    
    
    
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


## Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8에서 출제한 과제를 기반으로 만들었습니다.
