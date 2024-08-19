import os
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text
from tqdm import tqdm

from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_openai.embeddings import OpenAIEmbeddings
#from langchain_upstage import UpstageEmbeddings

import pickle
import define_persona
from define_persona import Movie_Info
import vector_store

class Retriever:
  def __init__ (self, dialogue_path, vector_path, movie):
    self.dialogue_path = dialogue_path
    self.vector_path = vector_path
    self.movie = movie
    self.document_path = os.path.join(self.dialogue_path, f'{Movie_Info.GetMovieTitle(self.movie)}_documents.dlg')
    self.vector_file_path = os.path.join(self.vector_path, f'{Movie_Info.GetMovieTitle(self.movie)}_vector.idx')

    
  def make_schema(self): #무엇이 추출되어야 할지 - 스키마 정의
    match self.movie:
      case define_persona.Persona_Movie.NewWorld:
        example_text = """
        강과장의 구둣발이 바닥에 떨어진 월병들을 으깨 밟고... 부서지는 월병들마다 비닐에 싸인 달러들을 토해낸다. 
        심드렁한 눈길로 가벼운 한숨을 내쉬는 강과장.
        
        정청
        왜요? 내용물이 별로 맘에 안 드셔? 좀 더 채워 드린다니까? 아니면... 차명 하나 터서 아예 우리 쪽 지분을 좀 태워 드리까?
        
        강과장
        어이 야... 정청이. 
        """
        result = [
           {"role": "정청", "dialogue": "왜요? 내용물이 별로 맘에 안 드셔? 좀 더 채워 드린다니까? 아니면... 차명 하나 터서 아예 우리 쪽 지분을 좀 태워 드리까?"},
           {"role": "강과장", "dialogue": "어이 야... 정청이."}
           ]

      case define_persona.Persona_Movie.InsideMen:
        example_text = """
        안상구 : (비자금 파일을 건네며) 형님께서 맡아주쇼. 나중에 요긴하게 써먹을 데가 
        있는지 두고 봅시다. 먼저 까는 건 예의가 아닌 거 아시죠?
        이강희 : (비릿한 미소) 이런 여우같은 곰을 봤나..
        
        책상에 엎어져있는 휴대폰.. 안상구 몰래 작동되고 있던 녹음기.
        """
        result=[
          {"role": "안상구", "dialogue": "형님께서 맡아주쇼. 나중에 요긴하게 써먹을 데가 있는지 두고 봅시다. 먼저 까는 건 예의가 아닌 거 아시죠?"},
          {"role": "이강희", "dialogue": "이런 여우같은 곰을 봤나.."}
          ]
      
      case define_persona.Persona_Movie.WarOnCrime:
        #actor = 'ikhyun'
        #moviename = "범죄와의 전쟁"
        example_text = """
        조 계장
        무슨 오해 임마?? 돈 없어가 힘들어 죽겠다던 놈이 가라오케
        에서 술 물 돈은 있는갑네... 뭐 좋은 일 있나?? 
        익현
        (피식 웃으며) 계장님 만난 게 좋은 일이라면 좋은 일 이
        지예... 전 이만 일어나겠습니다...
        
        자리에서 일어나 조 계장에게 다가가는 익현.
        """
        result=[
          {"role": "조 계장", "dialogue": "무슨 오해 임마?? 돈 없어가 힘들어 죽겠다던 놈이 가라오케에서 술 물 돈은 있는갑네... 뭐 좋은 일 있나??"},
          {"role": "이강희", "dialogue": "계장님 만난 게 좋은 일이라면 좋은 일 이지예... 전 이만 일어나겠습니다..."}
          ]

    schema = Object(id ='script', 
                    description= f"Extract dialogue from given movie '{Movie_Info.GetMovieTitle(self.movie)}', ignore the non dialgue parts. \
                    When analyzing the document, make the most of your knowledge about the {Movie_Info.GetMovieTitle(self.movie)} movie content you know. \
                    When the speaker is not clear, infer from the character's personality, occupation, and way of speaking.",
                    attributes=[Text(id="role", description="The character who is speaking, use context to predict the role"),
                                Text(id="dialogue", description="The dialogue spoken by the characters in the context")
                                ],
                    examples = [(example_text, result)], #아웃풋 형식
                    many=True)
    return schema
  
  def parse_kor_result(self, data):
    script = data['text']['data']['script']
    results = [f"{scr['role']}: {scr['dialogue']}\n" for scr in script if 'role' in scr]
    main_char_inc = any(scr['role'] == Movie_Info.GetMovieCharacterKorean(self.movie) for scr in script if 'role' in scr)
    return ''.join(results), main_char_inc

  def exist_dialoguefile(self):
    return os.path.isfile(self.document_path)

  def extract_dialogue(self, llm, documents): #dialogue 추출
    schema = self.make_schema()
    kor_chain = create_extraction_chain(llm, schema)
    doc_script = []
    pbar = tqdm(total = len(documents))

    idx = 0
    while idx < len(documents):
        try:
            doc = documents[idx]
            script = kor_chain.invoke(doc.page_content)
            script_parsed, main_char_inc = self.parse_kor_result(script)
            if main_char_inc:
                doc_script.append(script_parsed)
            idx += 1
            pbar.update(1)
        except Exception as e:
            print(e)

    source_text = self.movie
    doc_script_result = [Document(page_content=script_parsed,metadata={"source": Movie_Info.GetMovieTitle(self.movie)}) for script_parsed in doc_script]

    with open(self.document_path, "wb") as file:
      pickle.dump(doc_script_result, file)
    return doc_script_result
  
  def load_dialogue(self):
    with open(self.document_path, "rb") as file:
      doc_script_result = pickle.load(file)
    return doc_script_result
  

  def create_retriever(self, api_key, doc_script):
    embed_model = OpenAIEmbeddings(api_key=api_key, model='text-embedding-3-small') #임베딩 모델 만들어주기
    vectorstore = vector_store.VectorStore(self.vector_file_path, embed_model)

    if vectorstore.exist_vectorIndex():
      print("Load Index")
      vectorstore.load_index()
    else:
      print("Get Index")
      vectorstore.get_vectorindex_from_documents(doc_script)

    vector_index = vectorstore.get_vectorindex()
    self.retriever = vector_index.as_retriever(search_type="mmr", #리트리버 객체를 생성 #다양성을 고려한 mmr검색
                                         search_kwargs={"k":3}) #다큐먼트  3개까지 검색
    return self.retriever

  def retriever_result(self, query):
    result = self.retriever.get_relevant_documents(query) #리트리버가 쿼리에 알맞는 대화 맥락을 가져옴 
    return result