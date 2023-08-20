import streamlit as st
from openai_utils import completeChat
import pandas as pd

st.title("Generate captions and taglines")

potions = dict()
targets = dict()

def changePotionKey(key):
    potions[st.session_state["potion_key"+key]] = potions[key]
    del potions[key]
    st.session_state['potions'] = potions

def changePotionValue(key):
    potions[key] = st.session_state["potion_value"+key]
    st.session_state['potions'] = potions

def addNewPotion():
    potions[''] = ''
    st.session_state['potions'] = potions

def changeTargetKey(key):
    targets[st.session_state["target_key"+key]] = targets[key]
    del targets[key]
    st.session_state['targets'] = targets

def changeTargetValue(key):
    targets[key] = st.session_state["target_value"+key]
    st.session_state['targets'] = targets

def addNewTarget():
    targets[''] = ''
    st.session_state['targets'] = targets

@st.cache_data
def convertDfToCSV(df):
   return df.to_csv(index=False).encode('utf-8')

def potionsCSV():
    df = pd.DataFrame(potions.items(), columns=['Potion Title', 'Potion Effect'])
    return convertDfToCSV(df)

def targetsCSV():
    df = pd.DataFrame(targets.items(), columns=['Target Title', 'Target Effect'])
    return convertDfToCSV(df)

uploadPotionCol, uploadTargetCol = st.columns(2)
with uploadPotionCol:
    if 'potions' in st.session_state:
        potions = st.session_state['potions']
        uploaded_potions = st.file_uploader("Upload your potions", type=['csv'])
    else:
        uploaded_potions = st.file_uploader("Upload your potions", type=['csv'])
        if uploaded_potions:
            df = pd.read_csv(uploaded_potions)

            for ind in df.index:
                potions[df['Potion Title'][ind]] = df['Potion Effect'][ind]
            
            st.session_state['potions'] = potions

with uploadTargetCol:
    if 'targets' in st.session_state:
        targets = st.session_state['targets']
        uploaded_targets = st.file_uploader("Upload your targets", type=['csv'])
    else:
        uploaded_targets = st.file_uploader("Upload your targets", type=['csv'])
        if uploaded_targets:
            df = pd.read_csv(uploaded_targets)

            for ind in df.index:
                targets[df['Target Title'][ind]] = df['Target Effect'][ind]
            
            st.session_state['targets'] = targets

potionsCol, targetsCol = st.columns(2)
with potionsCol:
    for key in potions:
        col1, col2 = st.columns(2)

        with col1:
            potion_key = st.text_input('potion key', value = key, label_visibility='hidden', key="potion_key"+key,
                                        on_change=changePotionKey, args=(key,))
        with col2:
            potion_value = st.text_area('potion value', value = potions[key], label_visibility='hidden', key="potion_value"+key,
                                        on_change=changePotionValue, args=(key,))

    if len(potions) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.button("Add new potion", on_click=addNewPotion)
        with col2:
            st.download_button(
                "Save Potions",
                potionsCSV(),
                "Potions.csv",
                "text/csv",
                key='download-potions'
            )

with targetsCol:
    for key in targets:
        col1, col2 = st.columns(2)

        with col1:
            target_key = st.text_input('target key', value = key, label_visibility='hidden', key="target_key"+key,
                                        on_change=changeTargetKey, args=(key,))
        with col2:
            target_value = st.text_area('target value', value = targets[key], label_visibility='hidden', key="target_value"+key,
                                        on_change=changeTargetValue, args=(key,))

    if len(targets) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.button("Add new target", on_click=addNewTarget)
        with col2:
            st.download_button(
                "Save Targets",
                targetsCSV(),
                "Targets.csv",
                "text/csv",
                key='download-targets'
            )

asistant_role=st.text_input("Tell assistant its role")
question=st.text_area("Input the text here")
temperature=st.slider("Temperature - Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.", min_value=0.0, max_value=2.0, value=1.0)
presencePenalty=st.slider("Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.", min_value=-2.0, max_value=2.0, value=0.0)
frequencyPenalty=st.slider("Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.", min_value=-2.0, max_value=2.0, value=0.0)
button=st.button("Generate ")

if asistant_role and question and button:
    for key, value in potions.items():
        placeholder = f"`{key}`"
        question = question.replace(placeholder, value)

    for key, value in targets.items():
        placeholder = f"@{key}"
        question = question.replace(placeholder, value)

    messages = [
        {"role": "system", "content": asistant_role},
        {"role": "user", "content": question},
    ]
    response = completeChat(messages, temperature, presencePenalty, frequencyPenalty)
    st.write(response)