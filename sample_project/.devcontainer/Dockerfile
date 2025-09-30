FROM tonylampada/tlpy:latest

# Copy only pyproject.toml for dependency caching
COPY pyproject.toml /tmp/
WORKDIR /tmp

# Install all dependencies at build time using uv
# First install main dependencies, then dev dependencies
RUN sudo uv pip install --system . && \
    sudo uv pip install --system '.[dev]'

# Clean up temporary files
RUN sudo rm -rf /tmp/pyproject.toml /tmp/sample_todo_api.egg-info

WORKDIR /workspace
USER vscode