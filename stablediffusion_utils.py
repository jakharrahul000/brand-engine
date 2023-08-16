import streamlit as st
import base64
import os
import requests

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"
api_key = st.secrets["stable_diffusion_key"]

def createImages(prompt):
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 4,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        return []
    else:
        data = response.json()
        images = []

        for i, image in enumerate(data["artifacts"]):
            images.append(image["base64"])

        return images