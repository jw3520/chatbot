import os
import re

def load_script(filename):
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
    lines = script_text.splitlines()
    return lines

def remove_parentheses_content(text):
    return re.sub(r'\([^)]*\)', '', text).strip()

def is_character_line(line, character_name):
    """
    줄이 캐릭터의 대사인지 확인합니다.
    
    Parameters:
        line (str): 확인할 줄
        character_name (str): 캐릭터 이름
    
    Returns:
        bool: 대사인지 여부
    """
    return line.strip().startswith(character_name)

def extract_character_lines(parsed_lines, character_name):
    character_lines = []
    capture = False
    for line in parsed_lines:
        if is_character_line(line, character_name):
            capture = True
            continue

        if capture:
            if not line.strip() or line.startswith(" ") or line.startswith("*"):
                capture = False
            else:
                clean_line = remove_parentheses_content(line.strip())
                if clean_line and not clean_line.startswith("*"):
                    character_lines.append(clean_line)

    return character_lines

def save_lines_to_file(lines, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + "\n")
    print(f"대사가 {filename} 파일로 저장되었습니다.")

if __name__ == "__main__":
    script_file_path = 'script/war_on_crime.txt'  # 대본 파일의 경로
    output_file_path = 'script/war_on_crime_character_lines.txt'  # 추출된 대사를 저장할 파일 경로
    
    script_text = load_script(script_file_path)
    
    if script_text:
        parsed_lines = parse_script(script_text)
        character_lines = extract_character_lines(parsed_lines, "익현")
        save_lines_to_file(character_lines, output_file_path)