import openai
import streamlit as st

# Replace "YOUR_API_KEY" with your actual OpenAI API key
openai.api_key = "取得したAPIキー"

st.title("GPT: ")

text = st.secrets["DB_KEY"]
st.write(text)

# Get the user's message
message = st.text_input("Enter your message:")

# Generate a response from GPT if the user has entered a message
if message:
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"/japanese {message}",
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
  ).choices[0].text
  #Display the response from GPT
  st.write(f"GPT response: {response}")
