import json
import openai
import os
import re
import streamlit as st
from googleapiclient.discovery import build
from llama_index import LLMPredictor, ServiceContext
from llama_index.readers import BeautifulSoupWebReader
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Replace "YOUR_API_KEY" with your actual OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["DB_KEY"]

st.title("Ask Kazuo GPT: ")

chat = ChatOpenAI(temperature=0)

# Get the user's message
message = st.text_input("Enter your question:")

# Generate a response from GPT if the user has entered a message
if message:
  ret = chat([HumanMessage(content="以下の例題にならって、知りたい情報を得るための適切な検索語句を3語以内で出力してください。\n"
"例：「今年のWBCのMVPは誰ですか？」：「WBC 2023 MVP」\n"
"例：「初代ポケットモンスターのゲームに登場するポケモンは何種類か知りたい。」：「初代 ポケモン 種類」\n"
"例：「旭化成様が抱える経営課題を教えて。」：「旭化成 経営 課題」\n"
"例：「Linuxで使えるコマンドとその意味を分かりやすくリストアップしてほしい」：「Linux コマンド 一覧」\n"
f"問題：「{message}」")])

  # ChatGPTの出力は「＜検索ワード＞」となるはずなので、「」の中身を取り出す
  search_query = re.findall('「(.*?)」', f"{ret.content}")[0]
  st.title(search_query)

  #Display the response from GPT
  answer = chat([HumanMessage(content=message)])
  st.write(answer)
