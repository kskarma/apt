import os
import streamlit as st
import openai
from os.path import join, dirname
from dotenv import load_dotenv


# APIキーの設定
load_dotenv(join(dirname(__file__), '.env'))
openai.api_key = os.environ.get("API_KEY") 

# 「送信」ボタンがクリックされた場合に、OpenAIに問い合わせる
def do_question():
    question = st.session_state.question_input.strip()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question},
        ],
    )
    answer = response.choices[0]["message"]["content"].strip()
    st.session_state.qa.append({"question":question,"answer":answer})
    st.session_state.question_input = ""

def main():
    # セッションステートに qaリストを初期化する
    if "qa" not in st.session_state:
        st.session_state.qa = []

    # テキストボックスで質問を入力
    st.text_input("質問を入力してください", key="question_input")
    # 送信ボタンがクリックするとOpenAIに問い合わせる
    st.button("送信", on_click=do_question)

    # リストをループして、質問と回答を表示
    for qa in st.session_state.qa:
        col1, col2 = st.columns(2)
        col1.write(qa["question"])
        col2.write(qa["answer"])

if __name__ == "__main__":
    main()        
