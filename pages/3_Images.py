import streamlit as st
from stablediffusion_utils import createImages
from utils import base64_to_image
import pandas as pd

st.title("Generate images")

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
                "Images Potions.csv",
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
                "Images Targets.csv",
                "text/csv",
                key='download-targets'
            )

question=st.text_area("Input the prompt")
questionWeight=st.slider("Weight of prompt", min_value=0.0, max_value=1.0, value=1.0)
negativeQuestion=st.text_area("Input the negative prompt")
negativeQuestionWeight=st.slider("Weight of negative prompt", min_value=-1.0, max_value=0.0, value=-1.0)
steps=st.slider("steps - Number of diffusion steps to run", min_value=10, max_value=150, value=50)
cfgScale=st.slider("cfg_scale - How strictly the diffusion process adheres to the prompt text (higher values keep your image closer to your prompt)", min_value=0, max_value=35, value=7)
seed=st.slider("seed - Random noise seed", min_value=0, max_value=100, value=0)
clipGuidancePreset=st.selectbox(
    "clip_guidance_preset",
    ("NONE", "FAST_BLUE", "FAST_GREEN", "SIMPLE", "SLOW", "SLOWER", "SLOWEST")
)
sampler=st.selectbox(
    "sampler - Which sampler to use for the diffusion process",
    ("DDIM", "DDPM", "K_DPMPP_2M", "K_DPMPP_2S_ANCESTRAL", "K_DPM_2", "K_DPM_2_ANCESTRAL", "K_EULER", "K_EULER_ANCESTRAL", "K_HEUN", "K_LMS")
)
stylePreset=st.selectbox(
    "style_preset - Pass in a style preset to guide the image model towards a particular style",
    ("enhance", "anime", "photographic", "digital-art", "comic-book", "fantasy-art", "line-art", "analog-film", "neon-punk", "isometric", "low-poly", "origami", "modeling-compound", "cinematic", "3d-model", "pixel-art", "tile-texture")
)

button=st.button("Generate ")


if question and button:
    for key, value in potions.items():
        placeholder = f"`{key}`"
        question = question.replace(placeholder, value)

    for key, value in targets.items():
        placeholder = f"@{key}"
        question = question.replace(placeholder, value)

    positivePrompt = {
        "text": question,
        "weight": questionWeight
    }
    textPrompts = []
    textPrompts.append(positivePrompt)
    if len(negativeQuestion) > 0:
        negativePrompt = {
            "text": negativeQuestion,
            "weight": negativeQuestionWeight
        }
        textPrompts.append(negativePrompt)

    images = createImages(textPrompts, cfgScale, steps, clipGuidancePreset, sampler, seed, stylePreset)
    image1Col, image2Col = st.columns(2)
    image3Col, image4Col = st.columns(2)
    image1Col.image(base64_to_image(images[0]))
    image2Col.image(base64_to_image(images[1]))
    image3Col.image(base64_to_image(images[2]))
    image4Col.image(base64_to_image(images[3]))