# Dockerfile
FROM python:3.12-slim

# Evita interação durante instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema necessárias para o Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Copia arquivos
COPY . /app

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala os navegadores do Playwright
RUN playwright install --with-deps

# Comando padrão para rodar o robô
CMD ["bash", "start.sh"]
