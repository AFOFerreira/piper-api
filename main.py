from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import uuid
import os
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online"}

@app.post("/tts")
def tts(text: str = Form(...)):
    uid = str(uuid.uuid4())

    wav = f"/app/output/{uid}.wav"
    mp3 = f"/app/output/{uid}.mp3"

    cmd1 = f'echo "{text}" | piper --model /app/voices/voz.onnx --output_file {wav}'
    subprocess.run(cmd1, shell=True)

    cmd2 = f'ffmpeg -y -i {wav} -af "loudnorm,acompressor" {mp3}'
    subprocess.run(cmd2, shell=True)

    return FileResponse(mp3, media_type="audio/mpeg", filename="audio.mp3")