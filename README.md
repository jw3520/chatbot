# Chat in Movie
- 영화 스크립트를 통한 영화 캐릭터 Persona Chatbot
  

<br>

## 프로젝트 소개

- 영화 대본파일을 입력해 해당 영화에 등장하는 등장인물의 페르소나를 바탕으로 한 Chatbot을 구현합니다.
- 이 프로젝트에서, 어느 대본을 입력하느냐에 따라 다양한 페르소나 Chatbot을 구현 가능하지만, 현재 세가지 영화의 캐릭터 챗봇만을 구현했습니다.
- '신세계'의 정청(황정민), '내부자들'의 상구(이병헌), '범죄와의 전쟁'의 익현(최민식)의 페르소나 챗봇이 적용되어 있습니다.
- 대본 정보를 입력하고, 추가로 Template을 통한 프롬프트 엔지니어링으로 캐릭터의 말투를 최대한 따라하도록 구현했습니다.
<br>

## 팀원 구성

<div align="center">

| **팀장** | **팀원 1** | **팀원 2** | **팀원 3** | **팀원 4** |
| :------: |  :------: | :------: | :------: | :------: |
|[<img src="https://github.com/user-attachments/assets/df23edc1-a610-49ed-a6d7-704a5242f5b5" height=150 width=150> <br/> 이동호<br> @Github](https://github.com/Horidong) |[<img src="https://github.com/user-attachments/assets/153d75a7-9cae-4bda-9864-b5948461ffbb" height=150 width=150> <br/> 권세진<br>@Github](https://github.com/sjkwon1023) |[<img src="https://github.com/user-attachments/assets/e45e5af0-17a5-495b-8ad7-881c94553396" height=150 width=150> <br/> 김윤환<br>@Github](https://github.com/yoon-py) |[<img src="https://github.com/user-attachments/assets/1dabb2e8-da0d-4b9b-9a6e-480ddb460068" height=150 width=150> <br/> 김정우<br>@Github](https://github.com/jw3520) |[<img src="https://github.com/user-attachments/assets/6b16588c-d583-4b1d-9cce-246467a0eb12" height=150 width=150> <br/> 천세민<br>@Github](https://github.com/affable17) |
</div>

<br>

## 1. 개발 환경

- 주 언어 : Python 3.10.14
- 버전 및 이슈관리 : Python Version 3.10, 라이브러리 버전은 'Persona Chatbot' 강의자료의 버전에 따름
- 협업 툴 : Git, Notion

<br>

## 2. 채택한 개발 기술과 브랜치 전략

### gpt-4o

- GPT 4o
  - GPT 3.5 turbo, Solar llm api적용해보았으나 각 버전의 이슈 문제로 최종 gpt 4o 버전을 택함
  - GPT 3.5 turbo는 동일한 말을 계속해서 반복하는 문제가 있었음. llm 버전 변경하니 해결되는 문제였기 때문에 해당 버전의 오류라고 판단함. Chatbot에 사용 불가능한 이슈.
  - Solar llm 사용 시 embedding 속도가 매우 느려 초기 세팅이 오래걸리는 이슈 있었음. 개발 테스트를 해야하는 상황에서 시간이 너무 많이 소요되어 gpt로 변경.


### Fast API
- Fast API
  - API 통신을 위해 채택
  - 해당 API 사용법은 강의자료에도 있었기 때문에 적용이 빨라 채택함

### 브랜치전략 
    
- 브랜치 전략
  - main 브랜치가 있었고, 각 팀원마다 자신의 모듈 이름으로 브랜치를 나누어 개발 진행
  - 따라서, 모듈별로 브랜치가 존재하였으나 최종버전에서는 main 브랜치로 병합

<br>

## 3. 프로젝트 구조
```
├── README.md
├── .gitignore
├── requirements.txt
├── codes
     ├── main.py
     ├── crawler.py
     ├── vector_store.py
     ├── retriever.py
     ├── llm.py
     ├── define_persona.py
     ├── legacy_codes
          ├── crawler_bck.py
          ├── crawler_inside_man.py
          ├── crawler_war_on_crime.py
          ├── main_bck.py
          └── vector_store_bck.py
     └── resources
          ├── api_key.txt
          ├── dialogues
          ├── script
          ├── templates
          └── vector
└── view
     ├── chatbot.py
     ├── chatbot_multi.py
     └── data_fetcher.py

```

<br>

## 4. 역할 분담

### 이동호 / 팀장
- **역할**
    - 프로젝트 전체 일정과 역할분담 등을 관리
    - 각 팀원이 개발한 모듈을 main.py에서 합쳐 하나의 프로젝트로 통합
- **기능**
    - 프론트엔드에서 호출 가능한 API 작성
    - 각 모듈을 main에서 클래스 호출을 통해 챗봇 구현
<br>

### 권세진
- **역할**
    - LLM 모듈 및 프롬프트 엔지니어링
- **기능**
    - llm 모델과 연결하여 chatbot에 연결해주는 모듈 개발
    - 모델 별 테스트 진행
    - 캐릭터 별 프롬프트 템플릿 작성
<br>

### 김윤환
- **역할**
    - crawling 및 벡터 인덱스 모듈
- **기능**
    - 대본파일 crawling 및 텍스트 split 모듈 개발
    - 벡터 인덱스 변환 기능 개발
<br>

### 김정우
- **역할**
    - 챗봇 프론트엔드
- **기능**
    - Gradio를 사용해 챗봇 프론트엔드 부분을 개발
    - 캐릭터를 선택하고 채팅을 직접 할 수 있는 UI 개발

<br>

### 천세민
- **역할**
    - retrieval 모듈
- **기능**
    - 레퍼런스를 찾아주는 retrieval  모듈 개발
    - LangChain에 사용할 텍스트 검색 및 retrieval 담당

## 5. 개발 기간 및 사용 방법

### 개발 기간
- 전체 개발 기간 : 2024-08-12 ~ 2024-08-19
- 프로젝트 요구사항 및 역할 분석 : 2024-08-12
- 기능 구현 : 2024-08-13 ~ 2024-08-17
- 발표자료 준비 및 프로젝트 문서 총 정리 : 2024-08-19
  
<br>

### 사용방법
1. api_key.txt파일에 본인의 openai api key를 입력합니다.
2. main.py를 서버처럼 사용해야 하므로, uvicorn 패키지를 사용합니다.
```python
pip install uvicorn
```
3. uvicorn 명령어를 사용해 main app을 포트 넘버 8888번에 맞춰 실행합니다.
```python
uvicorn main:app --port=8888
```
4. view Directory에 있는 'chatbot_multi.py'파일을 실행하면 프론트엔드 페이지가 생성됩니다.
5. 페이지 생성 후 페이지에 접근 가능한 링크가 나오므로, 해당 링크를 통해 접속하면 됩니다.


<br>

## 6. 프로젝트 후기

### 이동호
해당 프로젝트를 통해 Langchain과 RAG의 개념에 대해 조금 더 잘 이해할 수 있었습니다

### 권세진
어려웠지만 처음으로 개발과 관련된 프로젝트를 진행하게 되어 재미있었습니다

### 김윤환
팀원들과의 협업을 통해 저의 부족한 부분을 보완할 수 있었습니다. 
프로젝트 초반에는 개인적으로 부족함을 많이 느꼈지만, 팀원들이 각자의 강점을 발휘해 저의 약점을 채워주었습니다.
저 혼자서는 해내기 어려웠을 일이었지만, 함께 노력하면서 성장할 수 있는 소중한 계기가 되었습니다.

### 김정우
chat gpt 사용하면서 늘 사용자의 입장이었는데, 실습과 프로젝트를 진행하며 그 너머를 알아가는 게 재미있었습니다.

### 천세민
첫 프로젝트에 대한 걱정과 달리 배워가는 것이 많았고 좋은 경험이었습니다.
<br>

