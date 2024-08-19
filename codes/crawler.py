import os
import re
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from define_persona import Movie_Info

class Crawler:
    def __init__(self, res_path):
        """
        Set Movie Title and Resource Path

        Parameters:
            res_path (str) : Resources Root Path
            
        """
        self.res_path = res_path
        self.script_path = os.path.join(self.res_path, 'script')
        
    def split_text(self, text, movie, chunk_size=2048, overlap=128): # 청크 크기와 오버랩 크기 확장 
        """
        Split Chunk From Long Text
        
        Parameters:
            text (str): 나눌 텍스트.
            movie ()
            chunk_size (int): 각 청크의 최대 단어 수.
            overlap (int): 청크 간 겹치는 단어 수 (문맥 유지를 위해).
        
        Returns:
            list of str: 나눠진 텍스트 청크 리스트.
        """
        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=chunk_size,
            chunk_overlap=overlap,
        )
        documents = text_splitter.split_documents(text)
        if Movie_Info.GetMovieCharacterKorean(movie) == "안상구":
            documents_ret = [d for d in documents if d.page_content.find(f'{Movie_Info.GetMovieCharacterKorean(movie)} :') > -1]    
        else:
            documents_ret = [d for d in documents if d.page_content.find(f'\n{Movie_Info.GetMovieCharacterKorean(movie)}\n') > -1]
        return documents_ret
        
    def load_script(self, movie):
        """
        1. Read data and split chunk from file
        2. Find Script include conversation of main character
    
        Parameters:
            movie (Persona_Movie) : movie Enum
    
        Returns:
            Documents List: Splitted data from file
        """
        script_file_path = os.path.join(self.script_path, f'{Movie_Info.GetMovieTitle(movie)}.txt')
        loader = TextLoader(script_file_path, encoding='utf-8')
        script_text = loader.load()
        documents = self.split_text(script_text, movie, 2048, 128)
        print(f'LEN DOCUMENT:{len(documents)}')
        return documents

#def load_script(filename):
#    """
#    텍스트 파일에서 데이터를 읽어옵니다.
#    
#    Parameters:
#        filename (str): 읽을 파일명
#    
#    Returns:
#        str: 파일에서 읽어온 텍스트 데이터
#    """
#    try:
#        with open(filename, 'r', encoding='utf-8') as file:
#            script_text = file.read()
#        return script_text
#    except FileNotFoundError:
#        print(f"파일을 찾을 수 없습니다: {filename}")
#        return None
#    except Exception as e:
#        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
#        return None
#
#def parse_script(script_text):
#    """
#    스크립트를 파싱하여 라인 단위로 분리합니다.
#    
#    Parameters:
#        script_text (str): 파싱할 스크립트 텍스트
#    
#    Returns:
#        list: 파싱된 스크립트 라인들의 리스트
#    """
#    lines = script_text.splitlines()
#    return lines
#
#def remove_parentheses_content(text):
#    """
#    텍스트에서 괄호로 감싸진 내용을 제거합니다.
#    
#    Parameters:
#        text (str): 원본 텍스트
#    
#    Returns:
#        str: 괄호 안의 내용이 제거된 텍스트
#    """
#    return re.sub(r'\([^)]*\)', '', text).strip()
#
#def extract_character_lines(parsed_lines, character_name):
#    """
#    특정 캐릭터의 대사만을 추출하며, 괄호 안의 내용을 제거합니다.
#    
#    Parameters:
#        parsed_lines (list): 파싱된 스크립트 라인들
#        character_name (str): 대사를 추출할 캐릭터의 이름
#    
#    Returns:
#        list: 캐릭터의 대사 리스트
#    """
#    character_lines = []
#    capture = False
#    for line in parsed_lines:
#        if line.strip() == character_name:
#            capture = True
#            continue
#        if capture:
#            # 괄호 안의 내용을 제거한 뒤 대사 리스트에 추가
#            clean_line = remove_parentheses_content(line)
#            if clean_line:  # 빈 줄이 아닌 경우만 추가
#                character_lines.append(clean_line)
#            capture = False
#    return character_lines
#
#def save_lines_to_file(lines, filename):
#    """
#    추출된 대사를 파일로 저장합니다.
#    
#    Parameters:
#        lines (list): 저장할 대사 리스트
#        filename (str): 저장할 파일명
#    
#    Returns:
#        None
#    """
#    os.makedirs(os.path.dirname(filename), exist_ok=True)
#    
#    with open(filename, 'w', encoding='utf-8') as file:
#        for line in lines:
#            file.write(line + "\n")
#    print(f"대사가 {filename} 파일로 저장되었습니다.")
#
#if __name__ == "__main__":
#    # 파일 경로 설정
#    script_file_path = os.path.join('script', 'new_world.txt')  # 대본 파일의 경로
#    output_file_path = os.path.join('script', 'new_world_character_lines.txt')  # 추출된 대사를 저장할 파일 경로
#    
#    # 스크립트 로드
#    script_text = load_script(script_file_path)
#    
#    if script_text:
#        # 정청 대사 추출
#        parsed_lines = parse_script(script_text)
#        character_lines = extract_character_lines(parsed_lines, "정청")
#        
#        # 추출된 대사를 파일로 저장
#        save_lines_to_file(character_lines, output_file_path)