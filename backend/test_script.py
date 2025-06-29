# test_script.py
import requests
import os

# Configs
BASE_URL = "http://localhost:5173/dashboard"
IMAGE_PATH = "//Product/muse/backend/test_assets/image.png"
IMAGE_FILENAME = os.path.basename(IMAGE_PATH)

# Step 0: Upload image and get server-side path
print("🖼️ Uploading image to backend...")
try:
    with open(IMAGE_PATH, "rb") as f:
        files = {"file": (IMAGE_FILENAME, f, "image/png")}
        upload_response = requests.post(f"{BASE_URL}/upload/", files=files)
        upload_response.raise_for_status()
        # uploaded_path = upload_response.json()["file_path"]  # Correct key
        uploaded_path = upload_response.json()["saved_path"]
        print(f"✅ Image uploaded: {uploaded_path}")
except Exception as e:
    # print("❌ Failed to upload image:", e)
    print("❌ Failed to upload image:", e, upload_response.text)
    exit()

# Step 1: Flow 1 - Generate meme ideas
print("🚀 Testing Flow 1: /ideas/ endpoint")

flow1_payload = {
    "product_name": "Pixel Helicopter",
    "product_description": "A tiny pixel-art toy helicopter that flies with lights.",
    "image_filename": uploaded_path
}

try:
    response = requests.post(f"{BASE_URL}/ideas/", json=flow1_payload)
    response.raise_for_status()
    ideas = response.json()
    print(f"✅ Received {len(ideas)} meme ideas:\n")
    for i, idea in enumerate(ideas, 1):
        print(f"Idea {i}: {idea['idea']}")
        print(f"Audio: {idea['audio_script']}")
        print(f"Video Prompt: {idea['video_prompt']}\n")
except Exception as e:
    print("❌ Error during Flow 1:", e)
    exit()

# Step 2: Flow 2 - Generate final video
first_idea = ideas[0]
print("🎬 Testing Flow 2: /generate/ endpoint\n")

flow2_payload = {
    "audio_script": first_idea["audio_script"],
    "video_prompt": first_idea["video_prompt"]
}

try:
    response = requests.post(f"{BASE_URL}/generate/", json=flow2_payload)
    response.raise_for_status()
    result = response.json()
    print("✅ Video generated at:", result["video_path"])
except Exception as e:
    print("❌ Error during Flow 2:", e)
