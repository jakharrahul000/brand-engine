import streamlit as st
import openai

def completeChat(messages):
    # TODO save api key in secrets
    openai.api_key=st.secrets["openai_key"]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages]
    )

    return response.choices[0].message.content