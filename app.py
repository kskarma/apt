import streamlit as st

def main():
    # テキストボックスで名前を入力
    name = st.text_input("名前を入力してください")
    #名前が入力されていればこんにちはと表示
    if name:
        st.write(f"こんにちは、{name}さん！")

if __name__ == "__main__":
    main()
