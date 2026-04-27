FROM python:3.11-slim

RUN apt update && apt install -y \
wget \
curl \
ffmpeg \
libstdc++6 \
ca-certificates \
unzip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala Piper correto
RUN wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz && \
tar -xzf piper_linux_x86_64.tar.gz && \
mv piper/piper /usr/local/bin/piper && \
chmod +x /usr/local/bin/piper && \
rm -rf piper*

COPY . .

RUN chmod +x start.sh
RUN mkdir -p /app/output
RUN mkdir -p /app/voices

EXPOSE 8000

CMD ["./start.sh"]