# Sample FastAPI Project with tlpy DevContainer

This is a sample project demonstrating how to use the `tonylampada/tlpy` Docker image for Python development with a clean DevContainer setup.

## 🚀 Features

- **FastAPI** TODO application with full CRUD operations
- **Comprehensive tests** with pytest and coverage
- **Code quality tools**: ruff, black, mypy
- **AI assistants**: Claude Code and OpenAI Codex pre-installed
- **DevContainer** ready for VS Code

## 📋 Prerequisites

- Docker and Docker Compose
- VS Code with Dev Containers extension (optional)

## 🛠️ Quick Start

### Option 1: VS Code DevContainer (Recommended)

1. Open this folder in VS Code
2. When prompted, click "Reopen in Container"
3. Wait for the container to build (dependencies are installed at build time)
4. You're ready to code!

### Option 2: Command Line

```bash
# Build the container with dependencies
docker compose -f .devcontainer/docker-compose.yml build

# Enter the development container
docker compose -f .devcontainer/docker-compose.yml run --rm dev bash
```

## 📁 Project Structure

```
sample_project/
├── .devcontainer/
│   ├── devcontainer.json  # VS Code configuration
│   ├── docker-compose.yml # Single dev container
│   └── Dockerfile         # Installs deps from pyproject.toml
├── app/
│   ├── __init__.py
│   └── main.py           # FastAPI application
├── tests/
│   ├── __init__.py
│   └── test_main.py      # Test suite
├── pyproject.toml        # Project configuration & dependencies
└── README.md             # This file
```

## 🚀 Essential Commands

All commands are run inside the container. First, enter the container:

```bash
docker compose -f .devcontainer/docker-compose.yml run --rm dev bash
```

### Running the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# The API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Testing

```bash
# Run tests with coverage
pytest -v --cov=app --cov-report=term-missing

# Run tests in watch mode
pytest --watch
```

### Code Quality

```bash
# Format code
black app/ tests/
ruff check --fix app/ tests/

# Type checking
mypy app/

# Run all checks
black --check app/ tests/ && ruff check app/ tests/ && mypy app/
```

### Development Tools

```bash
# Interactive Python shell
ipython

# Jupyter notebook
jupyter notebook --ip=0.0.0.0 --allow-root --no-browser

# AI Assistants (if authenticated)
claude
codex
```

## 🌐 API Endpoints

Once the application is running, you can access:

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /todos` - List all todos
- `GET /todos/{id}` - Get a specific todo
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo
- `GET /stats` - Get todo statistics

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Create a TODO
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Build amazing APIs"}'

# List all TODOs
curl http://localhost:8000/todos

# Get statistics
curl http://localhost:8000/stats
```

## 🔧 Managing Dependencies

Dependencies are defined in `pyproject.toml`:
- Main dependencies in `[project] dependencies`
- Dev dependencies in `[project.optional-dependencies] dev`

To rebuild the container after changing dependencies:

```bash
docker compose -f .devcontainer/docker-compose.yml build --no-cache
```

## 🤖 AI Assistants

The container includes Claude Code and OpenAI Codex. To use them:

1. **Authenticate on your host machine first:**
   ```bash
   claude login  # Creates ~/.claude/
   codex login   # Creates ~/.codex/
   ```

2. **The docker-compose.yml mounts these directories**, so authentication persists

3. **Or use API keys** by creating a `.env` file:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-...
   OPENAI_API_KEY=sk-...
   ```

## 💡 Tips

- **Hot reload**: The application runs with `--reload`, changes are reflected immediately
- **All dependencies pre-installed**: No need to install packages at runtime
- **Single container**: One container serves all purposes (dev, test, lint)
- **VS Code integration**: Full IntelliSense and debugging support

## 🐳 Docker Commands Reference

```bash
# Build the container
docker compose -f .devcontainer/docker-compose.yml build

# Start interactive shell
docker compose -f .devcontainer/docker-compose.yml run --rm dev bash

# Run a specific command
docker compose -f .devcontainer/docker-compose.yml run --rm dev pytest

# Start container in background
docker compose -f .devcontainer/docker-compose.yml up -d

# Stop and remove containers
docker compose -f .devcontainer/docker-compose.yml down

# View logs
docker compose -f .devcontainer/docker-compose.yml logs -f
```

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [tlpy Container Documentation](https://github.com/tonylampada/tlpy)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)