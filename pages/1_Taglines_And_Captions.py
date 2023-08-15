import streamlit as st
import openai
from openai_utils import completeChat

st.title("Generate captions and taglines")

asistant_role=st.text_input("Tell assistant its role")
question=st.text_area("Input the text here")
button=st.button("Generate ")

if asistant_role and question and button:
    messages = [
        {"role": "system", "content": asistant_role},
        {"role": "user", "content": question},
    ]
    response = completeChat(messages)
    st.write(response)