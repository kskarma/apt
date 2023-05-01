import openai
import os
import re
import streamlit as st
from llama_index import LLMPredictor, ServiceContext
from llama_index.readers import BeautifulSoupWebReader
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Replace "YOUR_API_KEY" with your actual OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["DB_KEY"]

st.title("Ask Kazuo GPT: ")

#text = st.secrets["DB_KEY"]
#st.write(text)
chat = ChatOpenAI(temperature=0)

# Get the user's message
message = st.text_input("Enter your message:")

# Generate a response from GPT if the user has entered a message
if message:
  search_query = chat([HumanMessage(content=message)])

  #response = openai.Completion.create(
  #  engine="text-davinci-002",
  #  prompt=f"/japanese {message}",
  #  max_tokens=1024,
  #  n=1,
  #  stop=None,
  #  temperature=0.5,
  #).choices[0].text

  #Display the response from GPT
  st.write(f"Kazuo GPT's response: {search_query}")
