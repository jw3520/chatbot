from data_fetcher import DataFetcher
import gradio as gr

class Character:
    def __init__(self, key, name, img):
        self.key = key
        self.name = name
        self.img = img

dropdownList = ["[신세계] 정청", "[내부자들] 상구", "[범죄와의 전쟁] 익현"]
chracterList = [
    Character("jungcheong", dropdownList[0], "https://blog.kakaocdn.net/dn/NmJfr/btqH0o5ulF9/lCbz7L2fikbGkELkXJ07eK/img.png"),
    Character("sangku", dropdownList[1], "https://mblogthumb-phinf.pstatic.net/20160826_147/jayryu97_1472177190182GCOVt_PNG/image_394415091472177143295.png?type=w800"),
    Character("ikhyun", dropdownList[2], "https://img1.daumcdn.net/thumb/R1280x0/?fname=http://t1.daumcdn.net/brunch/service/user/8Irx/image/MXlqT7x-YhPP4g9ljI3XWX7RP64.jpg")
]

# 선택된 dropdown의 index
selected = 0
# 대화 기록을 저장할 전역 변수
history = []

def get_response(message):
    fetcher = DataFetcher(chracterList[selected].key, message)
    return fetcher.get_reply()

def handle_submit(message, history):
    response = get_response(message)
    history.append((message, response))
    return history, ""

def reset_chat():
    global history
    history = []  # 대화 기록 초기화
    return [], ""  # 초기화된 대화 기록과 빈 텍스트 박스

def undo_last_chat(history):
    if history:
        last_message = history[-1][0]  # 마지막 메시지
        response = get_response(last_message)
        history.append((last_message, response))  # 마지막 메시지를 다시 보냄
    return history, ""

def clear_last_chat(history):
    if history:
        history.pop()  # 마지막 메시지 삭제
    return history, ""

def setCharacter(x):
    global selected
    selected = dropdownList.index(x)
    return reset_chat()  # 선택된 캐릭터로 변경 후 대화 기록 초기화

with gr.Blocks() as app:
    gr.HTML("<h1>배우의 페르소나로 답변하는 챗봇입니다.</h1>")
    gr.HTML("<h3>Chat in Movie [Chat bot 4팀]</h3>")
    
    with gr.Row():
        character_dropdown = gr.Dropdown(value=dropdownList[0],
                                         choices=dropdownList,
                                         label="어떤 배우와 대화를 하고 싶으신가요?",
                                         interactive=True)
        for character in chracterList:
            gr.HTML("<img src='" + character.img + "' style='width: 400px; height: 200px'><br><span style='display: block; text-align: center;'><strong>" + character.name + "</strong></span>")
        
    chatbot = gr.Chatbot()
    textbox = gr.Textbox(
        placeholder="메시지를 입력해주세요.",
        container=False,
        scale=7
    )
    
    with gr.Row():
        undo_button = gr.Button("🔄  다시보내기 ↩")
        clear_button = gr.Button("↩️ 이전 채팅 삭제")
        reset_button = gr.Button("🗑️  전체 채팅 삭제")
        
        undo_button.click(undo_last_chat, inputs=[chatbot], outputs=[chatbot, textbox])
        clear_button.click(clear_last_chat, inputs=[chatbot], outputs=[chatbot, textbox])
        reset_button.click(reset_chat, outputs=[chatbot, textbox])
  
    textbox.submit(handle_submit, inputs=[textbox, chatbot], outputs=[chatbot, textbox])
    character_dropdown.change(setCharacter, inputs=[character_dropdown], outputs=[chatbot, textbox])
    
app.launch(share=True)