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

GOOGLE_API_KEY = st.secrets["G_A_KEY"]
GOOGLE_CSE_ID = st.secrets["G_C_I"]

def search_google(keyword, num=6) -> dict:
    """Google検索を行い、レスポンスを辞書で返す"""
    search_service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    response = search_service.cse().list(
                q=keyword,
                cx=GOOGLE_CSE_ID,
                lr='lang_ja',
                num=num,
                start=1
            ).execute()
    response_json = json.dumps(response, ensure_ascii=False, indent=4)
    
st.title("Ask Kazuo GPT: ")

chat = ChatOpenAI(temperature=0)

url_data = search_google("自然言語処理") # 上位10件取得する
print(f"Webページをまとめています...\n")
# ブラックリスト
black_list_domain = [".pdf","note.com"]
def is_black(link): # 特定のリンクがブラックリストにあるかどうか
    for l in black_list_domain:
        if l in link:
            return True
    return False

# スクレイピングできないサイトデータは除去
# url_data = [data for data in url_data if not is_black(data["link"])]
for data in url_data:
  st.write(data["link"])

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
