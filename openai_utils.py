import streamlit as st
import openai

def completeChat(messages, temperature, presencePenalty, frequencyPenalty):
    openai.api_key=st.secrets["openai_key"]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        temperature=temperature,
        presence_penalty=presencePenalty,
        frequency_penalty=frequencyPenalty
    )

    return response.choices[0].message.content