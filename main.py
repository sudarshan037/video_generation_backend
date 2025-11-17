import os
import uuid
import json
import base64
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

app = FastAPI(title="Video Generation Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

@app.get("/health")
async def health():
    return {"status": "ok"}

# image to video -> I2V-A14B -> Image-to-Video MoE model, supports 480P & 720P
# text to video -> NOT IMPLEMENTING
# effects, extend
# first and last frame -> FLF2V-14B
# references
# repaint
# inpaint

@app.post("/process/v1/image_to_video", tags=["Mock"])
async def process(
    data: str = Form(...),
    image: UploadFile = File(None),
):
    """
    Mock endpoint for image to video generation.
    request: data: JSON string, image: uploaded image file
    response: Blob Path of generated video
    """
    payload: Dict = json.loads(data)
    os.makedirs("data/uploaded_images", exist_ok=True)

    if image:
        image_filename = f"{payload['request_id']}.{image.filename.split(".")[-1]}"
        save_path = os.path.join("data/uploaded_images", image_filename)

        with open(save_path, "wb") as f:
            content = await image.read()
            f.write(content)

    video_path = f"data/generated_videos/{payload['request_id']}.mp4"
    # TODO: generate video from image
    if not os.path.isfile(video_path):
        return {"error": "Video file not found"}
    # TODO: upload to blob storage
    
    return {
        "request_id": payload["request_id"],
        "blob_path": f"{os.getenv('BLOB_BASE_URL')}/mugenverse/{video_path}?{os.getenv('BLOB_SAS_TOKEN')}"
    }

@app.post("/process/v2/image_to_video", tags=["Process"])
async def process(
    data: str = Form(...),
    image: UploadFile = File(None),
):
    """
    image and prompt to video generation.
    request: data: JSON string, image: uploaded image file
    response: Blob Path of generated video
    """
    payload: Dict = json.loads(data)
    os.makedirs("data/uploaded_images", exist_ok=True)

    if image:
        image_filename = f"{payload['request_id']}.{image.filename.split(".")[-1]}"
        save_path = os.path.join("data/uploaded_images", image_filename)

        with open(save_path, "wb") as f:
            content = await image.read()
            f.write(content)

    video_path = f"data/generated_videos/{payload['request_id']}.mp4"
    # TODO: generate video from image
    # python generate.py --task i2v-A14B --size 1280*720 --ckpt_dir ./Wan2.2-I2V-A14B
    # --offload_model True --convert_model_dtype --image examples/i2v_input.JPG
    # --prompt "Summer beach vacation style, a white cat wearing sunglasses sits on a surfboard. The fluffy-furred feline gazes directly at the camera with a relaxed expression. Blurred beach scenery forms the background featuring crystal-clear waters, distant green hills, and a blue sky dotted with white clouds. The cat assumes a naturally relaxed posture, as if savoring the sea breeze and warm sunlight. A close-up shot highlights the feline's intricate details and the refreshing atmosphere of the seaside."
    
    # python generate.py --task ti2v-5B --size 1280*704 --ckpt_dir ./Wan2.2-TI2V-5B
    # --offload_model True --convert_model_dtype --t5_cpu
    # --prompt "Two anthropomorphic cats in comfy boxing gear and bright gloves fight intensely on a spotlighted stage"
    
    if not os.path.isfile(video_path):
        return {"error": "Video file not found"}
    # TODO: upload to blob storage
    
    return {
        "request_id": payload["request_id"],
        "blob_path": f"{os.getenv('BLOB_BASE_URL')}/mugenverse/{video_path}?{os.getenv('BLOB_SAS_TOKEN')}"
    }


@app.post("/process/v1/first_and_last_frame_to_video", tags=["Mock"])
async def process(
    data: str = Form(...),
    first: UploadFile = File(None),
    last: UploadFile = File(None),
):
    """
    Mock endpoint for filler video generation.
    request: data: JSON string, image: uploaded image file
    response: Blob Path of generated video
    """
    payload: Dict = json.loads(data)
    os.makedirs("data/uploaded_images", exist_ok=True)

    if first and last:
        first_filename = f"{payload['request_id']}_first.{first.filename.split(".")[-1]}"
        save_path = os.path.join("data/uploaded_images", first_filename)

        with open(save_path, "wb") as f:
            content = await first.read()
            f.write(content)

        last_filename = f"{payload['request_id']}_last.{last.filename.split(".")[-1]}"
        save_path = os.path.join("data/uploaded_images", last_filename)

        with open(save_path, "wb") as f:
            content = await last.read()
            f.write(content)

    video_path = f"data/generated_videos/{payload['request_id']}.mp4"
    # TODO: generate video from image
    if not os.path.isfile(video_path):
        return {"error": "Video file not found"}
    # TODO: upload to blob storage
    
    return {
        "request_id": payload["request_id"],
        "blob_path": f"{os.getenv('BLOB_BASE_URL')}/mugenverse/{video_path}?{os.getenv('BLOB_SAS_TOKEN')}"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
