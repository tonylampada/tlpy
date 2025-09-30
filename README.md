# tlpy - Python DevContainer

Imagem Docker otimizada para desenvolvimento Python com ferramentas modernas e AI assistants, pronta para uso como DevContainer.

🐳 **Docker Hub:** `tonylampada/tlpy:latest`

## 🚀 Características

### Linguagens e Runtimes
- **Python 3.12** - Versão estável do Python
- **Node.js LTS** - Para ferramentas JavaScript/TypeScript
- **uv** - Gerenciador de pacotes Python ultra-rápido da Astral

### Ferramentas Python
- **ruff** - Linter e formatter extremamente rápido
- **black** - Formatter Python opinativo
- **mypy** - Type checker estático
- **pytest** - Framework de testes com coverage
- **ipython** - Shell Python interativo aprimorado
- **jupyter** - Notebooks interativos
- **rich** - Biblioteca para terminal com formatação rica
- **httpx** - Cliente HTTP moderno

### Ferramentas JavaScript
- **pnpm** - Gerenciador de pacotes eficiente
- **typescript** - Suporte a TypeScript
- **tsx** - Execute TypeScript diretamente
- **biome** - Formatter e linter rápido para JS/TS

### Ferramentas de Sistema
- **ripgrep** - Busca ultrarrápida em arquivos
- **fd-find** - Alternativa moderna ao find
- **bat** - Cat com syntax highlighting
- **eza** - Substituto moderno do ls
- **httpie** - Cliente HTTP de linha de comando
- **jq** - Processador JSON
- **tree** - Visualização de árvore de diretórios

### 🤖 AI Assistants
- **Claude Code** - AI assistant da Anthropic
- **OpenAI Codex** - AI assistant da OpenAI

## 📦 Como Usar

### Uso Rápido

```bash
# Baixar e executar a imagem
docker pull tonylampada/tlpy:latest
docker run -it --rm -v $(pwd):/workspace tonylampada/tlpy bash
```

### Com Docker Compose

Crie um `docker-compose.yml` no seu projeto:

```yaml
services:
  dev:
    image: tonylampada/tlpy:latest
    volumes:
      - .:/workspace
      # Montar credenciais dos AI assistants (se já autenticado)
      - ~/.claude:/home/vscode/.claude:ro
      - ~/.codex:/home/vscode/.codex:ro
    environment:
      # Se preferir usar API keys
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
    stdin_open: true
    tty: true
    command: bash
```

Depois execute:
```bash
docker-compose run --rm dev
```

### Como DevContainer no VS Code

1. Crie uma pasta `.devcontainer` no seu projeto
2. Adicione um arquivo `devcontainer.json`:

```json
{
  "name": "Python Dev Environment",
  "image": "tonylampada/tlpy:latest",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
        "ms-python.black-formatter",
        "ms-python.mypy-type-checker"
      ]
    }
  },
  "postCreateCommand": "uv pip install -r requirements.txt || true",
  "remoteUser": "vscode",
  "mounts": [
    "source=${localEnv:HOME}/.claude,target=/home/vscode/.claude,type=bind,consistency=cached",
    "source=${localEnv:HOME}/.codex,target=/home/vscode/.codex,type=bind,consistency=cached"
  ]
}
```

3. Reabra o projeto no container (Ctrl+Shift+P → "Reopen in Container")

### Aliases Disponíveis

O container vem com aliases úteis pré-configurados:

- `ll` → `eza -la` (listagem detalhada com ícones)
- `ls` → `eza` (listagem moderna)
- `cat` → `batcat` (visualização com syntax highlighting)
- `find` → `fdfind` (busca moderna de arquivos)

## 🎯 Casos de Uso

- **Desenvolvimento Python** - Ambiente completo para projetos Python
- **Data Science** - Com Jupyter e ferramentas de análise
- **Web Development** - Suporte a frameworks modernos
- **Automação** - Scripts e ferramentas CLI
- **Testes** - Ambiente isolado para CI/CD

## 🔐 Autenticação dos AI Assistants

### Claude Code
```bash
# Primeira vez - autenticar na máquina host
claude login

# As credenciais ficam em ~/.claude/
# O docker-compose.yml já monta esse diretório
```

### OpenAI Codex
```bash
# Primeira vez - autenticar na máquina host
codex login

# As credenciais ficam em ~/.codex/
# O docker-compose.yml já monta esse diretório
```

### Alternativa: Usar API Keys
```bash
# Criar arquivo .env no seu projeto
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
echo "OPENAI_API_KEY=sk-..." >> .env

# O docker-compose.yml já está configurado para usar essas variáveis
```

## 🔧 Customização

Para adicionar mais ferramentas Python ao seu projeto:

```bash
# Dentro do container (com sudo)
sudo uv pip install --system pandas numpy matplotlib

# Ou para instalação local no projeto
uv pip install pandas numpy matplotlib
```

## 📝 Notas

- O usuário padrão é `vscode` com acesso sudo
- O diretório de trabalho padrão é `/workspace`
- Python usa o ambiente do sistema (`UV_SYSTEM_PYTHON=1`)
- Todas as ferramentas estão disponíveis globalmente

## 📄 Licença

MIT