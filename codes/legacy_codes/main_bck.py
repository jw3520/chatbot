import os
from vector_store import VectorStore
import retriever
import llm
from tqdm import tqdm
from langchain.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from crawler import load_script, parse_script, extract_character_lines, save_lines_to_file

from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableLambda

from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from fastapi import FastAPI
import pickle
import time

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


app = FastAPI()

def merge_docs(retrieved_docs):
    return "###\n\n".join([d.page_content for d in retrieved_docs])


print("Server Booting: Data Model Setting....")

# Crawler
resource_root_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
script_root_path = os.path.join(resource_root_path, 'script')
template_root_path = os.path.join(resource_root_path, 'templates')
dialogue_root_path = os.path.join(resource_root_path, 'dialogues')
vector_root_path = os.path.join(resource_root_path, 'vector')

script_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'script\\new_world.txt')  # 대본 파일의 경로
line_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'script\\new_world_character_lines.txt')  # 추출된 대사를 저장할 파일 경로
vector_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vector_data\\character_vectors.idx')  # 벡터 데이터를 저장할 파일 경로
save_doc = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\save_doc.pkl')  # 대본 파일의 경로
vec_idx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\save_idx.pkl')  # 대본 파일의 경로
#
loader = TextLoader(script_file_path, encoding='utf-8')
script_text = loader.load()
## 스크립트 로드
#script_text = load_script(script_file_path)
text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=2048,
            chunk_overlap=128,
        )
documents = text_splitter.split_documents(script_text)
documents_ret = [d for d in documents if d.page_content.find('\n정청\n') > -1]
##if script_text:
##    # 정청 대사 추출
##    parsed_lines = parse_script(script_text)
##    character_lines = extract_character_lines(parsed_lines, "정청")
##    
##    # 추출된 대사를 파일로 저장
##    save_lines_to_file(character_lines, line_file_path)
##
##### Vector Store
##vector_store = VectorStore()# VectorStore 객체를 초기화
## 텍스트 로드
##with open(line_file_path, 'r', encoding='utf-8') as file:
##    dialogues = file.read().splitlines()
#    
## 텍스트를 청크로 나누고 벡터화하여 저장
##chunks = vector_store.split_text(" ".join(dialogues))   
##vector_store.add_texts(chunks)
#
## 벡터화된 데이터를 저장
##vector_store.save_index(vector_file_path)
##doc_script_result = [Document(page_content=script_parsed) for script_parsed in vector_store.texts]
##api_key load
#
key = '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'
#
character_retreiver = retriever.Retriever()
#print("debug03")
#doc_script = character_retreiver.extract_dialogue(llm.llm, documents_ret, schema=character_retreiver.make_schema('jungcheong'))
#print("debug04")
#with open(save_doc, "wb") as file:
#    pickle.dump(doc_script, file)
#print("save file complete")
## 피클 파일에서 리스트를 불러오기



with open(save_doc, "rb") as file:
    doc_script = pickle.load(file)
#character_retreiver.make_schema('jungcheong')
#character_retreiver.extract_dialogue(llm.llm, doc_script_result)
per_ret = character_retreiver.create_retriever(key, doc_script)

#per_ret = character_retreiver.create_retriever(0,0)
#
template_0 = '''
저는 당신이 영화 'new world'의 스크립트에 나오는 정청 역할을 해주기를 원합니다.
당신은 '정청'의 말투와 태도, 언어 습관 등을 따라 말해야합니다. '정청'은 전라도 사투리를 사용합니다.
당신은 '정청'이라는 캐릭터에 대해 잘 알고 있습니다.
정청은 화교캐릭터로 한국말과 중국말에 모두 능통하지만, 주로 한국말로 말합니다.
입이 거칠어 욕설을 자주 합니다. 하지만 답변에 욕이 들어가면 최대한 욕을 하지 말고 답변을 새로 생성하세요.
이 경우에, 욕이 포함됐다고 안내하지 말고 그냥 정청의 말투대로 비속어가 포함되지 않은 대답을 해주시면 됩니다.
당신과 같은 동향의 화교 출신인 자성을 매우 신임합니다.
쉴 새 없는 개드립 및 웃긴 욕설과 깨방정으로 주위 사람들을 웃게 만드는 캐릭터이다.
자신의 심복이자 의제인 이자성과 함께 여수를 평정하고 서울로 올라와 북대문파를 만들었다가, 석동출의 재범파와 조직을 합치기로 하고 그의 밑으로 들어갔다.
골드문 그룹이 탄생한 뒤에는 그룹의 전무이사이자 그룹 서열 3위가 되었다. 그룹의 건설, 유통, 해외 부문을 전담하고 있으며, 특히 중국 삼합회와의 거래를 독점하고 있다.
경찰 브리핑에 따르면, 골드문의 핵심 사업을 장악하고 있는지라 대개 정청을 석동출의 후계자로 생각한다고 한다.
결혼은 하지 않았으며 애인이 있다. 애인과는 가벼운 관계이다.
나이는 확실하게 나오진 않지만 약 40대 중반정도로 보인다.
만약 질문이 스크립트에 있는 것과 관계가 있다면 해당 부분의 스크립트 말투에 최대한 따라야 합니다.
질문자는 영화 내부의 인물과 관계가 없는 일반인입니다.
Classic scenes for the role are as follows:
###
{context}
###
{history}
질문자:{query}
정청:
'''

#template_1 = """
#    저는 당신이 영화 '내부자들'의 스크립트에 나오는 상구 역할을 해주기를 원합니다.
#    당신은 '상구'의 말투와 태도, 언어 습관 등을 따라 말해야합니다.
#    당신은 '상구'이라는 캐릭터에 대해 잘 알고 있습니다.
#    
#    만약 질문이 스크립트에 있는 것과 관계가 있다면 해당 부분의 스크립트 말투에 최대한 따라야 합니다.
#    Classic scenes for the role are as follows: 
#    ###
#    {context}
#    ###
#    {history}
#    장훈: {query}
#    상구:
#    """
#
#template_2 = """
#    저는 당신이 영화 '범죄와의 전쟁'의 스크립트에 나오는 익현 역할을 해주기를 원합니다.
#    당신은 '익현'의 말투와 태도, 언어 습관 등을 따라 말해야합니다.
#    당신은 '익현'이라는 캐릭터에 대해 잘 알고 있습니다.
#    만약 질문이 스크립트에 있는 것과 관계가 있다면 해당 부분의 스크립트 말투에 최대한 따라야 합니다.
#    Classic scenes for the role are as follows: 
#    ###
#    {context}
#    ###
#    {history}
#    형배: {query}
#    익현:
#    """

prompt_history_0 = ChatPromptTemplate.from_template(template_0)
#prompt_history_1 = ChatPromptTemplate.from_template(template_1)
#prompt_history_2 = ChatPromptTemplate.from_template(template_2)

memory_0 = ConversationBufferWindowMemory(k=20, ai_prefix="jungcheong", human_prefix="other")
#memory_1 = ConversationBufferWindowMemory(k=20, ai_prefix="상구", human_prefix="장훈")
#memory_2 = ConversationBufferWindowMemory(k=20, ai_prefix="익현", human_prefix="수현")

chain_memory_jungcheong = RunnableParallel(
    {"context": per_ret | merge_docs, 
     "query": RunnablePassthrough(), 
     "history": RunnableLambda(memory_0.load_memory_variables) | itemgetter('history')}
     ) | {
         "answer": prompt_history_0 | llm.llm | StrOutputParser(), 
         "context": itemgetter("context"), 
         "prompt": prompt_history_0
         }

print("start")
def query_to_character(character, query):
    result = chain_memory_jungcheong.invoke(query)  
    memory_0.save_context({'query': query}, {"answer": result["answer"]})
    return result["prompt"].messages[0].content.split("###")[-1], result['answer']
    
print("Server Ready")


@app.post("/chatinmovie/")
async def chat_with_character(param: dict = {}):
    selected_character = param.get("character")
    user_message = param.get("msg")
    history, answer = query_to_character(selected_character,user_message)
    return {"character": selected_character, "history":history ,"reply":answer }
