from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid, subprocess

app = FastAPI()

class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
def tts(data: TTSRequest):

    uid = str(uuid.uuid4())

    wav = f"/app/output/{uid}.wav"
    mp3 = f"/app/output/{uid}.mp3"

    cmd = f'echo "{data.text}" | piper --model /app/voices/voz.onnx --output_file {wav}'
    subprocess.run(cmd, shell=True)

    subprocess.run(
        f'ffmpeg -y -i {wav} -af "loudnorm,acompressor" {mp3}',
        shell=True
    )

    return FileResponse(mp3, media_type="audio/mpeg", filename="audio.mp3")