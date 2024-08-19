import os
import re

def load_script(filename):
    """
    텍스트 파일에서 데이터를 읽어옵니다.
    
    Parameters:
        filename (str): 읽을 파일명
    
    Returns:
        str: 파일에서 읽어온 텍스트 데이터
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            script_text = file.read()
        return script_text
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {filename}")
        return None
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

def parse_script(script_text):
    """
    스크립트를 파싱하여 라인 단위로 분리합니다.
    
    Parameters:
        script_text (str): 파싱할 스크립트 텍스트
    
    Returns:
        list: 파싱된 스크립트 라인들의 리스트
    """
    lines = script_text.splitlines()
    return lines

def remove_parentheses_content(text):
    """
    텍스트에서 괄호로 감싸진 내용을 제거합니다.
    
    Parameters:
        text (str): 원본 텍스트
    
    Returns:
        str: 괄호 안의 내용이 제거된 텍스트
    """
    return re.sub(r'\([^)]*\)', '', text).strip()

def extract_character_lines(parsed_lines, character_name):
    """
    특정 캐릭터의 대사만을 추출합니다. 지문과 괄호친 내용은 제외합니다.
    
    Parameters:
        parsed_lines (list): 파싱된 스크립트 라인들
        character_name (str): 대사를 추출할 캐릭터의 이름
    
    Returns:
        list: 캐릭터의 대사 리스트
    """
    character_lines = []
    capture = False
    for line in parsed_lines:
        # 캐릭터 이름으로 시작하는 줄을 찾음
        if re.match(rf'^{character_name} :', line.strip()):
            capture = True
            # 대사 부분만 추출 (캐릭터 이름 뒤에 나오는 부분), 괄호 내용 제거
            clean_line = remove_parentheses_content(line.split(":", 1)[1].strip())
            if clean_line:
                character_lines.append(clean_line)
            continue

        if capture:
            # 다른 캐릭터 이름이 나오거나 빈 줄이 나오면 대사 추출 종료
            if re.match(r'^[^\s]+ :', line.strip()) or line.strip() == "":
                capture = False
            else:
                # 이어지는 대사를 추가, 괄호 내용 제거
                clean_line = remove_parentheses_content(line.strip())
                if clean_line:
                    character_lines.append(clean_line)

    return character_lines

def save_lines_to_file(lines, filename):
    """
    추출된 대사를 파일로 저장합니다.
    
    Parameters:
        lines (list): 저장할 대사 리스트
        filename (str): 저장할 파일명
    
    Returns:
        None
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + "\n")
    print(f"대사가 {filename} 파일로 저장되었습니다.")

if __name__ == "__main__":
    # 파일 경로 설정
    script_file_path = 'script/inside_men.txt'  # 대본 파일의 경로
    output_file_path = 'script/inside_men_character_lines_02.txt'  # 추출된 대사를 저장할 파일 경로
    
    # 스크립트 로드
    script_text = load_script(script_file_path)
    
    if script_text:
        # 특정 캐릭터(예: 안상구)의 대사 추출
        parsed_lines = parse_script(script_text)
        character_lines = extract_character_lines(parsed_lines, "안상구")
        
        # 추출된 대사를 파일로 저장
        save_lines_to_file(character_lines, output_file_path)