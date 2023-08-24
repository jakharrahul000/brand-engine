import streamlit as st
import requests

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"
api_key = st.secrets["stable_diffusion_key"]

def createImages(textPrompts, cfgScale, steps, clipGuidancePreset, sampler, seed, stylePreset):
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": textPrompts,
            "cfg_scale": cfgScale,
            "height": 1024,
            "width": 1024,
            "samples": 4,
            "steps": steps,
            "clip_guidance_preset": clipGuidancePreset,
            "sampler": sampler,
            "seed": seed,
            "style_preset": stylePreset
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