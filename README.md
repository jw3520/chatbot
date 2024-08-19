# Chat in Movie
- 영화 스크립트를 통한 영화 캐릭터 Persona Chatbot
![image](https://github.com/user-attachments/assets/cde8bf85-1386-4d78-8bd2-f21b39f8d053)


<br>

## 프로젝트 소개

- 영화 대본파일을 입력해 해당 영화에 등장하는 등장인물의 페르소나를 바탕으로 한 Chatbot을 구현합니다.
- 이 프로젝트에서, 어느 대본을 입력하느냐에 따라 다양한 페르소나 Chatbot을 구현 가능하지만, 현재 세가지 영화의 캐릭터 챗봇만을 구현했습니다.
- '신세계'의 정청(황정민), '내부자들'의 상구(이병헌), '범죄와의 전쟁'의 익현(최민식)의 페르소나 챗봇이 적용되어 있습니다.
- 대본 정보를 입력하고, 추가로 Template을 통한 프롬프트 엔지니어링으로 캐릭터의 말투를 최대한 따라하도록 구현했습니다.
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
