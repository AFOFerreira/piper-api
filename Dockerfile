FROM python:3.11-slim

RUN apt update && apt install -y \
curl \
wget \
ffmpeg \
unzip \
libstdc++6 \
espeak-ng

WORKDIR /app

# instalar python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# instalar piper binário
RUN wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz && \
tar -xzf piper_amd64.tar.gz && \
mv piper /usr/local/bin/piper && \
chmod +x /usr/local/bin/piper && \
rm piper_amd64.tar.gz

COPY . .

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]