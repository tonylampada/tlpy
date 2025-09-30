# tlpy - Python DevContainer

Um Dockerfile otimizado para desenvolvimento Python com ferramentas modernas, perfeito para uso como DevContainer em projetos.

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

## 📦 Como Usar

### Como DevContainer no VS Code

1. Crie uma pasta `.devcontainer` no seu projeto
2. Adicione um arquivo `devcontainer.json`:

```json
{
  "name": "Python Dev Environment",
  "dockerFile": "Dockerfile",
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
  "postCreateCommand": "uv pip install -r requirements.txt",
  "remoteUser": "vscode"
}
```

3. Copie o Dockerfile para `.devcontainer/Dockerfile`
4. Reabra o projeto no container

### Build Local

```bash
# Construir a imagem
docker build -t python-devcontainer .

# Executar um container
docker run -it --rm -v $(pwd):/workspace python-devcontainer bash

# Ou com docker-compose
docker run -it --rm -v ${PWD}:/workspace -w /workspace python-devcontainer bash
```

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

## 🔧 Customização

Para adicionar mais ferramentas Python ao seu projeto:

```bash
# Dentro do container
uv pip install pandas numpy matplotlib

# Ou adicione ao requirements.txt do seu projeto
echo "pandas>=2.0.0" >> requirements.txt
uv pip install -r requirements.txt
```

## 📝 Notas

- O usuário padrão é `vscode` com acesso sudo
- O diretório de trabalho padrão é `/workspace`
- Python usa o ambiente do sistema (`UV_SYSTEM_PYTHON=1`)
- Todas as ferramentas estão disponíveis globalmente

## 📄 Licença

MIT

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.