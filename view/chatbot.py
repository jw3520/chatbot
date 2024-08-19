from data_fetcher import DataFetcher
import gradio as gr

class Character:
    def __init__(self, key, name, img):
        self.key = key
        self.name = name
        self.img = img

chracter = Character("jungcheong", "[신세계] 정청", "https://blog.kakaocdn.net/dn/NmJfr/btqH0o5ulF9/lCbz7L2fikbGkELkXJ07eK/img.png")
selected = 0

def get_response(message, history):
    fetcher = DataFetcher(chracter.key, message)
    return chracter.name + " : " + fetcher.get_reply()

with gr.ChatInterface(
        fn=get_response,
        textbox=gr.Textbox(placeholder="대화를 입력해주세요.", container=False, scale=7),
        title="배우의 페르소나로 답변하는 챗봇입니다.",
        description="Chat in Movie [Chat bot 4팀]",
        theme="soft",
        examples=[["안녕하세요."], ["당신은 누군가요?"], ["나는 누군가요?"], ["우리는 무슨 관계인가요?"], ["우리의 계획은 뭔가요?"]],
        retry_btn="🔄  다시보내기 ↩",
        undo_btn="↩️ 이전 채팅 삭제",
        clear_btn="🗑️  전체 채팅 삭제") as app:
    html = gr.HTML("<img src='" + chracter.img + "' style='width: 300px'>")

app.launch(share=True)