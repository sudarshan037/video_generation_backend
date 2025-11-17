import os
import uuid
import json
import base64
import uvicorn
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

@app.get("/health")
async def health():
    return {"status": "ok"}

# image to video
# text to video
# effects, extend
# first and last frame
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
    print(video_path)
    # TODO: generate video from image
    if not os.path.isfile(video_path):
        return {"error": "Video file not found"}
    # TODO: upload to blob storage
    
    return {
        "request_id": payload["request_id"],
        "blob_path": video_path
    }

@app.post("/process/v2/image_to_video", tags=["Process"])
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
    print(video_path)
    # TODO: generate video from image
    if not os.path.isfile(video_path):
        return {"error": "Video file not found"}
    # TODO: upload to blob storage
    
    return {
        "request_id": payload["request_id"],
        "blob_path": video_path
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
