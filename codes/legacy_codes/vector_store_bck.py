# 벡터화를 통해 KB를 구축하는 역할을 합니다.
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        """
        텍스트 데이터를 벡터화하고 저장할 수 있는 VectorStore 클래스
        
        Parameters:
            model_name (str): 사용할 사전 학습된 SentenceTransformer 모델의 이름.
        """
        self.model = SentenceTransformer(model_name)  # 텍스트를 벡터로 변환하기 위한 모델을 로드
        self.index = faiss.IndexFlatL2(384)  # FAISS 인덱스를 초기화 (벡터의 차원은 384).
        self.texts = []  # 원본 텍스트를 저장할 리스트를 초기화.

    def split_text(self, text, chunk_size=2048, overlap=128): # 청크 크기와 오버랩 크기 확장 
        """
        긴 텍스트를 작은 청크(조각)로 나누는 함수.
        
        Parameters:
            text (str): 나눌 텍스트.
            chunk_size (int): 각 청크의 최대 단어 수.
            overlap (int): 청크 간 겹치는 단어 수 (문맥 유지를 위해).
        
        Returns:
            list of str: 나눠진 텍스트 청크 리스트.
        """
        words = text.split()  # 텍스트를 단어 단위로 나눔.
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])  # 청크를 생성하고 리스트에 추가.
            chunks.append(chunk)
        return chunks

    def add_texts(self, texts):
        """
        텍스트 리스트를 벡터화하여 인덱스에 추가하는 함수.
        
        Parameters:
            texts (list of str): 벡터화할 텍스트 리스트.
        """
        for text in texts:
            self.texts.append(text)  # 원본 텍스트를 리스트에 추가.
            embeddings = self.model.encode([text])  # 텍스트를 벡터로 변환.
            self.index.add(np.array(embeddings))  # 벡터를 인덱스에 추가.

    def save_index(self, filename):
        """
        벡터화된 데이터를 파일로 저장.
        
        Parameters:
            filename (str): 저장할 파일명.
        
        Returns:
            None
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        faiss.write_index(self.index, filename)
        print(f"벡터 데이터가 {filename} 파일로 저장되었습니다.")
