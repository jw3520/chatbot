# 벡터화를 통해 KB를 구축하는 역할을 합니다.
import os
import numpy as np
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, vector_file_path, embed_model, model_name='paraphrase-MiniLM-L6-v2'):
        """
        텍스트 데이터를 벡터화하고 저장할 수 있는 VectorStore 클래스
        
        Parameters:
            model_name (str): 사용할 사전 학습된 SentenceTransformer 모델의 이름.
        """
        self.embed_model = embed_model
        self.vector_file_path = vector_file_path
        #self.model = SentenceTransformer(model_name)  # 텍스트를 벡터로 변환하기 위한 모델을 로드
        #self.index = faiss.IndexFlatL2(384)  # FAISS 인덱스를 초기화 (벡터의 차원은 384).
        #self.texts = []  # 원본 텍스트를 저장할 리스트를 초기화.

    def exist_vectorIndex(self):
        """
        Check vector index file is exist
        If exist, return True, if else return False
        """
        return os.path.isdir(self.vector_file_path)

    def get_vectorindex_from_documents(self, documents):
        self.vector_index = FAISS.from_documents(documents, self.embed_model)
        self.save_index()

    def save_index(self):
        self.vector_index.save_local(self.vector_file_path)
        
    def load_index(self):
        self.vector_index = FAISS.load_local(self.vector_file_path, self.embed_model, allow_dangerous_deserialization=True)

    def get_vectorindex(self):
        return self.vector_index


    #def add_texts(self, texts):
    #    """
    #    텍스트 리스트를 벡터화하여 인덱스에 추가하는 함수.
    #    
    #    Parameters:
    #        texts (list of str): 벡터화할 텍스트 리스트.
    #    """
    #    for text in texts:
    #        self.texts.append(text)  # 원본 텍스트를 리스트에 추가.
    #        embeddings = self.model.encode([text])  # 텍스트를 벡터로 변환.
    #        self.index.add(np.array(embeddings))  # 벡터를 인덱스에 추가.