import streamlit as st
from stablediffusion_utils import createImages
from utils import base64_to_image

st.title("Generate images")

question=st.text_area("Input the text here")
button=st.button("Generate ")

if question and button:
    prompt = question
    images = createImages(prompt)
    [st.image(base64_to_image(image)) for image in images]