from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid, subprocess, os

app = FastAPI()

class TTSRequest(BaseModel):
    text: str

# Garante que a pasta de saída exista ao iniciar
OUTPUT_DIR = "/app/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/tts") # Certifique-se de chamar /tts sem a barra no final
def tts(data: TTSRequest):
    uid = str(uuid.uuid4())
    wav = os.path.join(OUTPUT_DIR, f"{uid}.wav")
    mp3 = os.path.join(OUTPUT_DIR, f"{uid}.mp3")

    # 1. Gerar WAV
    # Usamos check=True para que o Python levante um erro se o comando falhar
    try:
        cmd_piper = f'echo "{data.text}" | piper --model /app/voices/voz.onnx --output_file {wav}'
        subprocess.run(cmd_piper, shell=True, check=True, capture_output=True)
        
        # 2. Converter para MP3
        cmd_ffmpeg = f'ffmpeg -y -i {wav} -af "loudnorm,acompressor" {mp3}'
        subprocess.run(cmd_ffmpeg, shell=True, check=True, capture_output=True)
        
    except subprocess.CalledProcessError as e:
        # Se algum comando falhar, retornamos o erro para facilitar o debug
        error_msg = e.stderr.decode() if e.stderr else "Erro desconhecido no subprocesso"
        raise HTTPException(status_code=500, detail=f"Erro no processamento de áudio: {error_msg}")

    if not os.path.exists(mp3):
        raise HTTPException(status_code=500, detail="Arquivo MP3 não foi gerado.")

    return FileResponse(mp3, media_type="audio/mpeg", filename="audio.mp3")