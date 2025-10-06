# Base image com Python já configurado para desenvolvimento
FROM mcr.microsoft.com/devcontainers/python:3.12

# Instalar Node.js LTS via NodeSource
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

# Instalar ferramentas globais do Node e AI assistants
RUN npm install -g --force \
    pnpm \
    typescript \
    tsx \
    @biomejs/biome \
    @anthropic-ai/claude-code \
    @openai/codex

# Instalar ferramentas de sistema úteis
RUN apt-get update && apt-get install -y \
    ripgrep \
    fd-find \
    bat \
    httpie \
    jq \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Instalar eza (substituto moderno do ls)
RUN wget -qO- https://github.com/eza-community/eza/releases/latest/download/eza_x86_64-unknown-linux-gnu.tar.gz | tar xz && \
    mv eza /usr/local/bin/

# Configurar sudo sem senha para vscode (permite instalar pacotes facilmente)
RUN echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER vscode

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/vscode/.bashrc && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/vscode/.zshrc

# Configurar uv para usar Python do sistema por padrão
ENV PATH="/home/vscode/.local/bin:${PATH}"
RUN uv venv /home/vscode/.venv

ENV VIRTUAL_ENV="/home/vscode/.venv" 
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Instalar ferramentas úteis para desenvolvimento Python
RUN uv pip install \
    ruff \
    black \
    mypy \
    pytest \
    pytest-cov \
    ipython \
    rich \
    httpx \
    jupyter



# Configurar aliases úteis
RUN echo 'alias ll="eza -la"' >> /home/vscode/.bashrc && \
    echo 'alias ls="eza"' >> /home/vscode/.bashrc && \
    echo 'alias cat="batcat"' >> /home/vscode/.bashrc && \
    echo 'alias find="fdfind"' >> /home/vscode/.bashrc && \
    echo 'alias ll="eza -la"' >> /home/vscode/.zshrc && \
    echo 'alias ls="eza"' >> /home/vscode/.zshrc && \
    echo 'alias cat="batcat"' >> /home/vscode/.zshrc && \
    echo 'alias find="fdfind"' >> /home/vscode/.zshrc

# Configurar o diretório de trabalho
WORKDIR /workspace

# Definir o usuário padrão
USER vscode