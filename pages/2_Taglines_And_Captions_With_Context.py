import streamlit as st
from openai_utils import completeChat

messages = []
st.session_state.disabled = False

st.title("Generate captions and taglines")

asistant_role=st.text_input("Tell assistant its role")
set_asistant_role=st.button("Set ", key="set button", disabled=st.session_state.disabled)


if 'messages' in st.session_state:
    messages = st.session_state['messages']
    st.session_state.disabled = True

# Append to messages
def appendMessages(message):
    messages.append(message)
    st.session_state['messages'] = messages
    return messages

if asistant_role and set_asistant_role and len(messages) == 0:
    appendMessages({"role": "system", "content": asistant_role})

question=st.text_area("Input the text here")
button=st.button("Generate ")

if question and button:
    messages.append(
        {"role": "user", "content": question}
    )
    response = completeChat(messages, 0)
    messages.append(
        {"role": "assistant", "content": response}
    )
    st.write(response)
    st.session_state['messages'] = messages