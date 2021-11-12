# 8percent-assignment-2

## 팀원 : 정성헌, 송빈호, 안다민
---
## 과제 출제 기업 정보
- 기업명 : 8퍼센트
- 8퍼센트 사이트 : https://8percent.kr/
- 원티드 채용 링크 : https://www.wanted.co.kr/wd/64695

---

## 필수 포함 사항
- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

**✔️ API 목록**

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

## 사용 기술 및 tools

> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/sqlite-1b9e41?style=for-the-badge&logo=Sqlite&logoColor=white"/>
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>

---

## 모델링
<img width="787" alt="스크린샷 2021-11-11 오후 6 11 51" src="https://user-images.githubusercontent.com/70747064/141466644-eb3982f9-3aa9-40dd-9129-e837fbc2e051.png">

---

## 구현기능 및 테스트

### 회원가입 및 로그인
- 회원가입시 password 같은 민감정보는 단방향 해쉬 알고리즘인 bcrypt를 이용해서 암호화 하여 database에 저장
- 로그인이 성공적으로 완료되면, user정보를 토큰으로 반환할때, 양방향 해쉬 알고리즘인 JWT를 사용해서 응답
- 포스트맨 예시

![스크린샷 2021-11-12 오후 9 34 41](https://user-images.githubusercontent.com/70747064/141468099-625429d1-2647-4bb4-b63d-929525cc4334.png)



### 거래 내역 조회 api

![스크린샷 2021-11-13 오전 12 50 21](https://user-images.githubusercontent.com/70747064/141508232-603d42c2-6c70-47b2-922c-44bfa7ac8834.png)


### 입금 api
- 계좌 비밀번호 : 

<img width="707" alt="스크린샷 2021-11-12 오후 9 48 16" src="https://user-images.githubusercontent.com/70747064/141473158-a594f34e-b201-46bb-9524-e40a04923d74.png">

- 계좌 조회 : 

<img width="696" alt="스크린샷 2021-11-12 오후 9 48 48" src="https://user-images.githubusercontent.com/70747064/141473221-9ad32f07-cdd6-470f-a990-4efc485d747c.png">

- 입금 : 

<img width="836" alt="스크린샷 2021-11-12 오후 10 11 51" src="https://user-images.githubusercontent.com/70747064/141473299-d94076b8-a425-45df-b04f-34ccc9bd9f9e.png">

### 출금 api

- 출금 : 

<img width="819" alt="스크린샷 2021-11-12 오후 10 12 14" src="https://user-images.githubusercontent.com/70747064/141473342-72a01081-f2ee-4f1a-8d57-0c835b4c7458.png">


## 폴더 구조
```
📦8percent-assignment-2
 ┃ ┣ 📜.gitignore
 ┣ 📂eight_percent
 ┃ ┣ 📂migrations
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜settings.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜wsgi.py
 ┣ 📂transaction
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜app.py
 ┃ ┣ 📂migrations
 ┃ ┣ 📜models.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┣ 📂users
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜app.py
 ┃ ┣ 📂migrations
 ┃ ┣ 📜models.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┣ 📜README.md
 ┣ 📜manage.py
 ┗ 📜requirements.txt
 ```



## Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8에서 출제한 과제를 기반으로 만들었습니다.
