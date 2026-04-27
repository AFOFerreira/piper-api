FROM python:3.11-slim

RUN apt update && apt install -y \
ffmpeg \
curl \
wget \
libstdc++6 \
espeak-ng \
build-essential \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# instala piper tts
RUN pip install --no-cache-dir piper-tts

COPY . .

RUN chmod +x start.sh
RUN mkdir -p /app/output /app/voices

EXPOSE 8000

CMD ["./start.sh"]