import streamlit as st
import json
import openai
import re
import os
from langchain.llms import OpenAI
from langchain_community.document_loaders import NotebookLoader # 소화할 파일 
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI


st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
# model_name = "gpt-4-0125-preview",
print(openai_api_key)

def generate_response(message):
    llm = ChatOpenAI(model_name = "gpt-4-0125-preview", max_tokens = 1200, temperature=0, openai_api_key=openai_api_key)
    # st.write("Answer:")
    st.markdown(llm.invoke(message).content)


# file upload
st.title("📝 Code Summary")
uploaded_file = st.file_uploader("Upload an article", type=("ipynb"))


loader = NotebookLoader(uploaded_file)

#print(''.join(data['cells'][:]['source']).strip())

if uploaded_file and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

if uploaded_file and openai_api_key:
    # 파일 json parsing
    data = json.load(uploaded_file)
    #print(data.keys())
    # article은 source code
    text_for_article = ''
    article = []
    # source code 부분만 가져오기
    for idx,_ in enumerate(data['cells']):
        for i, line in enumerate(data['cells'][idx]['source']):
            if '#' not in line:
                
                line = re.sub(r'\s+',' ',line)
                line = line.replace('\n+','\n')
                
                text_for_article += line+'\n'
            if len(text_for_article) > 2000:
                article.append(text_for_article)
                text_for_article = ''
        if len(text_for_article) > 0:
            article.append(text_for_article)

        text_for_article = ''
    #print(len(article))
    #print(text_for_article)
    #print(article)
    #article = json.load(uploaded_file)
    for text_len,code_str in enumerate(article):
        prompt = f"Here's an code:\n\n{code_str}\n\n\n\n"
        messages = [
            SystemMessage(
                content=f"
                    I am a programmar.\
                    I will provide lines of Python code.
                    you are an expert in datascience. \
                    You have helped many people before me to understand and execute code for various purposes.\
                    Provide easy to understand and clear explanations about given python code. \
                    Write your explanations with title in English with proper syntax."
            ),
            HumanMessage(
                content=f"{prompt}."
            ),
        ]
        #client = OpenAI()
        #response = f"{prompt}"
        # st.code(code_str)
        st.write(generate_response(messages))
# 출력은 되지만 최대 토큰 수가 4097로 코드 구역을 나누는 것이 필요
# git pull --rebase origin main
# https://stackoverflow.com/questions/71768999/how-to-merge-when-you-get-error-hint-you-have-divergent-branches-and-need-to-s
        

# chatbot & RAG 만들기 
from langchain.chat_models import ChatOpenAI
