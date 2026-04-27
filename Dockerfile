FROM python:3.11-slim

# Instala dependências do sistema
RUN apt update && apt install -y \
    ffmpeg \
    curl \
    wget \
    libstdc++6 \
    espeak-ng \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala as dependências Python primeiro (cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir piper-tts

# Copia o restante dos arquivos
COPY . .

# AJUSTE DE PERMISSÕES CRÍTICO:
# 1. Garante que as pastas de trabalho existam
# 2. Dá permissão total de escrita para evitar o erro de "file not found" no Windows
# 3. Garante que o start.sh tenha quebras de linha Unix (comum dar erro ao editar no Windows)
RUN mkdir -p /app/output /app/voices && \
    chmod -R 777 /app/output /app/voices && \
    chmod +x start.sh && \
    sed -i 's/\r$//' start.sh

# Garante que o diretório de scripts do pip esteja no PATH
ENV PATH="/usr/local/bin:${PATH}"

EXPOSE 8000

CMD ["./start.sh"]