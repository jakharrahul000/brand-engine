import streamlit as st
import requests

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"
api_key = st.secrets["stable_diffusion_key"]

def createImages(json):
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json=json,
    )

    if response.status_code != 200:
        return []
    else:
        data = response.json()
        images = []

        for i, image in enumerate(data["artifacts"]):
            images.append(image["base64"])

        return images
    
def createImagesWithBaseImage(data, baseImage):
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/image-to-image",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        files={
            "init_image": baseImage
        },
        data=data,
    )

    if response.status_code != 200:
        return []
    else:
        data = response.json()
        images = []

        for i, image in enumerate(data["artifacts"]):
            images.append(image["base64"])

        return images