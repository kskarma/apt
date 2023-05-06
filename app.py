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
    return response["items"]
    
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

  url_data = search_google(search_query) 
  ### st.title(url_data)

  # URLのみ渡してスクレイピング
  documents = BeautifulSoupWebReader().load_data(urls=[data["link"] for data in url_data]) 

  max_texts = 500
  documents_text = ""
  references = {}
  black_list_text = ["JavaScript is not available.", "404", "403", "ページが見つか", "不適切なページ", "Server error"]
  def is_black_text(text):
    for bt in black_list_text:
        if bt in text:
            return True
    return False

  for i in range(len(url_data)):
    if is_black_text(documents[i].text):
        continue
    # 余分な空白や改行を除去
    text = documents[i].text.replace('\n', '').replace("  ", " ").replace("\t", "")
    # テキストの最初の方はサイトのメニュー関連が多いので、テキストの一部だけを抽出するなど前処理をする
    # text = text[len(text)//10:]
    documents_text += f"【文献{i + 1}】{url_data[i]['snippet']}\n{text}"[:max_texts] + "\n"
    references[f"文献{i + 1}"] = {
        "title": url_data[i]['title'],
        "link": url_data[i]['link']
    }
    if len(documents_text) > 3000:
        documents_text = documents_text[:3000]
        break
  ret = chat([HumanMessage(content=f"以下の文献を要約して、下の質問に答えてください。\n"
f"◆文献リスト\n{documents_text}\n"
f"◆質問：{question}\n"
f"◆回答する際の注意事項：文中に対応する参考文献の番号を【文献1】のように出力してください。"
f"◆回答："
)])

  # ChatGPTの回答を格納
  answer = ret.content
  answer = answer.replace("。","。\n")

  i = 0 # 参考文献の番号をリセット
  add_ref_text = ""
  for ref in references.keys():
    if ref in answer:
        i += 1
        answer = answer.replace(f"【{ref}】", f"[{i}]")
        answer = answer.replace(ref, f"[{i}]")
        add_ref_text += f"[{i}] {references[ref]['title']}. {references[ref]['link']}.\n"

  answer += f"\n【参考文献】\n{add_ref_text}"
        
  #response = openai.Completion.create(
  #  engine="text-davinci-002",
  #  prompt=f"/japanese {message}",
  #  max_tokens=1024,
  #  n=1,
  #  stop=None,
  #  temperature=0.5,
  #).choices[0].text

  #Display the response from GPT
  st.write(answer)
