# DevContainer Setup for apiconfig Development

This DevContainer setup provides a fully configured Python development environment for the apiconfig project using Visual Studio Code and Docker.

## Key Features

### 1. Multi-Python Version Support
- Python 3.11, 3.12, and 3.13 pre-installed via pyenv
- Configured for tox-based multi-version testing
- Poetry for dependency management

### 2. Development Tools
- Pre-configured VS Code extensions for Python development
- Pre-commit hooks automatically installed
- Sphinx documentation server available

### 3. Qdrant Vector Database
The setup includes a Qdrant vector database service that provides:
- **HTTP API**: Available at http://localhost:6333 (from host) or http://qdrant:6333 (from inside devcontainer)
- **gRPC API**: Available at localhost:6334 (from host) or qdrant:6334 (from inside devcontainer)
- **Persistent Storage**: Data is stored in `./data/qdrant/` directory for persistence between container rebuilds
- **Web UI**: Qdrant dashboard accessible at http://localhost:6333/dashboard

To interact with Qdrant:
- **From your host machine**: Use http://localhost:6333 for HTTP API
- **From inside the devcontainer**: Use http://qdrant:6333 for HTTP API
- **Python client example**:
  ```python
  from qdrant_client import QdrantClient
  # From devcontainer
  client = QdrantClient(host="qdrant", port=6333)
  # From host
  client = QdrantClient(host="localhost", port=6333)
  ```

### 4. VS Code Extension Data Persistence
The devcontainer preserves VS Code extension data between container rebuilds:
- **Volume**: `vscode_extensions_data` mounted to `/root/.vscode-server/data/User/globalStorage`
- **Benefits**:
  - Extension settings and data persist
  - No need to reconfigure extensions after rebuilding
- **Permissions**: Set to 777 for maximum compatibility

## Services

### 1. `app` Service
- Main development container
- Based on Python 3.13 with pyenv for multiple Python versions
- Poetry pre-installed for dependency management
- All project dependencies installed

### 2. `docs` Service
- Sphinx documentation server
- Available for building and serving documentation

### 3. `qdrant` Service
- Vector database for AI/ML features
- Automatically starts with the devcontainer
- Data persists in `./data/qdrant/`

## Port Forwarding

The following ports are automatically forwarded:
- **5051**: Coverage Live Server
- **6333**: Qdrant HTTP API
- **6334**: Qdrant gRPC API

## Getting Started

1. **Prerequisites**:
   - Docker Desktop installed
   - VS Code with Remote - Containers extension

2. **Open in DevContainer**:
   - Open the project in VS Code
   - Click "Reopen in Container" when prompted
   - Or press <kbd>F1</kbd> and select "Remote-Containers: Reopen in Container"

3. **First Time Setup**:
   - The container will build and install all dependencies
   - Pre-commit hooks will be installed automatically
   - Your git configuration will be preserved

## Working with the Environment

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apiconfig

# Run tox for multi-version testing
tox
```

### Working with Poetry
```bash
# Add a dependency
poetry add package-name

# Add a dev dependency
poetry add --group dev package-name

# Install dependencies
poetry install
```

### Using Qdrant
```bash
# Check Qdrant health
curl http://qdrant:6333/health

# Access Qdrant dashboard (from browser)
http://localhost:6333/dashboard
```

## Customization

### Adding VS Code Extensions
Edit `.devcontainer/devcontainer.json` and add extensions to the `extensions` array.

### Modifying Python Versions
Edit `.devcontainer/Dockerfile` to add or remove Python versions in the pyenv install commands.

### Environment Variables
Create a `.env` file in the project root (it's gitignored) for local environment variables.

## Troubleshooting

### Container Rebuild
If you need to rebuild the container:
1. Press <kbd>F1</kbd> in VS Code
2. Select "Remote-Containers: Rebuild Container"

### Permission Issues
The container runs as root by default. If you encounter permission issues:
- Check that the postStartCommand is setting proper permissions
- Ensure Docker Desktop has file sharing enabled for your project directory

### Qdrant Connection Issues
- From devcontainer: Use `qdrant` as hostname
- From host: Use `localhost` as hostname
- Ensure ports 6333 and 6334 are not already in use

## Notes

- The devcontainer uses broad permissions (777) for VS Code extension data to ensure compatibility
- Qdrant data persists in `./data/qdrant/` which is gitignored
- All project files are mounted at `/workspace` inside the container