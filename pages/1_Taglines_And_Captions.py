import streamlit as st
from openai_utils import completeChat
import pandas as pd

st.title("Generate captions and taglines")

potions = dict()

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

@st.cache_data
def convertDfToCSV(df):
   return df.to_csv(index=False).encode('utf-8')

def potionsCSV():
    df = pd.DataFrame(potions.items(), columns=['Potion Title', 'Potion Effect'])
    return convertDfToCSV(df)

if 'potions' in st.session_state:
    potions = st.session_state['potions']
else:
    uploaded_potions = st.file_uploader("Upload your potions", type=['csv'])
    if uploaded_potions:
        df = pd.read_csv(uploaded_potions)

        for ind in df.index:
            potions[df['Potion Title'][ind]] = df['Potion Effect'][ind]

        uploaded_potions.close()

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
            key='download-csv'
        )

asistant_role=st.text_input("Tell assistant its role")
question=st.text_area("Input the text here")
button=st.button("Generate ")

if asistant_role and question and button:
    for key, value in potions.items():
        placeholder = f"`{key}`"
        question = question.replace(placeholder, value)

    messages = [
        {"role": "system", "content": asistant_role},
        {"role": "user", "content": question},
    ]
    response = completeChat(messages)
    st.write(response)