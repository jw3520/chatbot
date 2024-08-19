import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableLambda
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser

from define_persona import Persona_Movie, Movie_Info

resource_root_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
api_key_path = os.path.join(resource_root_path, 'api_key.txt')
#API Key

with open(api_key_path, "rb") as file:
      key = file.read()

LLM = ChatOpenAI(
    api_key = key,
    model_name="gpt-4o-mini",
    temperature=0
)

class ChatBot:
    def __init__(self, template_path, movie):
        self.template_path = template_path
        self.movie = movie

    def merge_docs(self, retrieved_docs):
        return "###\n\n".join([d.page_content for d in retrieved_docs])    

    def create_persona_chain(self, retreiver):
        template = Templates(self.template_path)
        self.persona_template = ChatPromptTemplate.from_template(template.load_templates(self.movie))
        self.persona_memory = ConversationBufferWindowMemory(k=20, ai_prefix=Movie_Info.GetMovieCharacterKorean(self.movie), human_prefix="질문자")
        self.chat_chain = RunnableParallel({"context": retreiver | self.merge_docs, "query": RunnablePassthrough(), "history": RunnableLambda(self.persona_memory.load_memory_variables) | itemgetter('history')}) \
         | {"answer": self.persona_template | LLM | StrOutputParser(), "context": itemgetter("context"),  "prompt": self.persona_template }

    def get_response(self, query):
        result = self.chat_chain.invoke(query)
        self.persona_memory.save_context({'query': query}, {"answer": result["answer"]})
        print(f'HISTORY:{result["prompt"].messages[0].content.split("###")[-1]}')
        print(f'ANSWER:{result}')
        return result["prompt"].messages[0].content.split("###")[-1], result['answer']

        #character_chain = prompt | self.llm | StrOutputParser()
        ## 결과 반환
        #result = character_chain.invoke({})
        #return result
    

class Templates:
    def __init__(self, template_path):
        self.root_path = template_path

    def load_templates(self, movie):
        path = os.path.join(self.root_path, f'{Movie_Info.GetMovieTitle(movie)}_template.tpl')
        with open(path, "r", encoding="utf-8") as file:
            template = file.read()
        return template

    #def get_template(self, movie):
#
    #    templates_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'templates\\{self.character}.txt')  
    #    with open(templates_path, "r", encoding="utf-8") as file:
    #        template = file.read()
    #    
    #    # 파일에서 읽은 템플릿에 context와 query를 포함시키는 방식으로 설정
    #    return template.format(context=self.context, query=self.query)

    