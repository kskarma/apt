import openai
import streamlit as st
from llama_index import LLMPredictor, ServiceContext
from llama_index.readers import BeautifulSoupWebReader
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Replace "YOUR_API_KEY" with your actual OpenAI API key
openai.api_key = st.secrets["DB_KEY"]

st.title("Ask Kazuo GPT: ")

#text = st.secrets["DB_KEY"]
#st.write(text)
chat = ChatOpenAI(temperature=0)

# Get the user's message
message = st.text_input("Enter your message:")

# Generate a response from GPT if the user has entered a message
if message:
  ret = chat([HumanMessage(content="以下の例題にならって、知りたい情報を得るための適切な検索語句を3語以内で出力してください。\n"
"例：「今年のWBCのMVPは誰ですか？」：「WBC 2023 MVP」\n"
"例：「初代ポケットモンスターのゲームに登場するポケモンは何種類か知りたい。」：「初代 ポケモン 種類」\n"
"例：「旭化成様が抱える経営課題を教えて。」：「旭化成 経営 課題」\n"
"例：「Linuxで使えるコマンドとその意味を分かりやすくリストアップしてほしい」：「Linux コマンド 一覧」\n"
f"問題：「{question}」")])

  # ChatGPTの出力は「＜検索ワード＞」となるはずなので、「」の中身を取り出す
  search_query = re.findall('「(.*?)」', f"{ret.content}")[0]

  #response = openai.Completion.create(
  #  engine="text-davinci-002",
  #  prompt=f"/japanese {message}",
  #  max_tokens=1024,
  #  n=1,
  #  stop=None,
  #  temperature=0.5,
  #).choices[0].text
  #Display the response from GPT
  st.write(f"GPT response: {search_query}")
