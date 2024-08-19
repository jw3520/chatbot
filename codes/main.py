import os
from retriever import Retriever
from llm import LLM, ChatBot, key
from langchain.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableLambda
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from crawler import Crawler
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from fastapi import FastAPI

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from enum import Enum, auto
from define_persona import Persona_Movie, Movie_Info
from crawler import Crawler

app = FastAPI()

print("Server Booting: Data Model Setting....")
# Define Path
resource_root_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
script_root_path = os.path.join(resource_root_path, 'script')
template_root_path = os.path.join(resource_root_path, 'templates')
dialogue_root_path = os.path.join(resource_root_path, 'dialogues')
vector_root_path = os.path.join(resource_root_path, 'vector')

# Define Movie
movie_0 = Persona_Movie.NewWorld
movie_1 = Persona_Movie.InsideMen
movie_2 = Persona_Movie.WarOnCrime
movies = [Persona_Movie.NewWorld,Persona_Movie.InsideMen,Persona_Movie.WarOnCrime]

retrievers = []
for movie in movies:
#Retriever
    character_retreiver = Retriever(dialogue_root_path,vector_root_path, movie)
    doc_script = []
    if character_retreiver.exist_dialoguefile():
        doc_script = character_retreiver.load_dialogue()
    else:
        #Script Crawler
        script_crawler = Crawler(resource_root_path)
        documents = script_crawler.load_script(movie)
        doc_script = character_retreiver.extract_dialogue(LLM, documents)

    persona_ret = character_retreiver.create_retriever(key, doc_script)
    
    retrievers.append(persona_ret)

print(retrievers)
chatbot_00 = ChatBot(template_root_path, movies[0])
chatbot_00.create_persona_chain(retrievers[0])
print("Persona about Juncheong in New World is Ready...")

chatbot_01 = ChatBot(template_root_path, movies[1])
chatbot_01.create_persona_chain(retrievers[1])
print("Persona about Sangku in Inside Men is Not Ready...")

chatbot_02 = ChatBot(template_root_path, movies[2])
chatbot_02.create_persona_chain(retrievers[2])
print("Persona about Ikhyun in War On Crime is Not Ready...")

def query_to_character(character, query):
    print(f'query to character:{character}:{query}')
    match character:
        case 'jungcheong':
            history, answer = chatbot_00.get_response(query)
        case 'sangku':
            history, answer = chatbot_01.get_response(query)
        case 'ikhyun':
            history, answer = chatbot_02.get_response(query)
    return history, answer
    #result = chat_chain.invoke(query)  
    #persona_memory.save_context({'query': query}, {"answer": result["answer"]})
    #return result["prompt"].messages[0].content.split("###")[-1], result['answer']
    
print("Server Ready")

@app.post("/chatinmovie/")
async def chat_with_character(param: dict = {}):
    print("Input from Client:")
    print(param)

    selected_character = param.get("character")
    user_message = param.get("msg")
    history, answer = query_to_character(selected_character,user_message)
    return {"character": selected_character, "history":history ,"reply":answer }
