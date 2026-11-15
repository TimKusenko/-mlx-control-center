# MLX Control Center

Remote control and monitoring for [MLX](https://ml-explore.github.io/mlx/) (Machine Learning on Apple Silicon) running on Mac mini.

**Status**: Beta. Works with a running MLX API server on Mac. Install dependencies on Mac first (see [Mac Setup](#mac-setup)).

## Features

- **Chat Interface** — Talk to multiple LLM models
- **Model Management** — List, download, delete models from Hugging Face
- **System Monitoring** — CPU, RAM, disk, network stats (btop, nettop)
- **Live Logs** — Stream API logs in real-time
- **Configuration** — Set temperature, max tokens, system prompts
- **SSH Tunnel** — Works over network (no local API required)

## Quick Start

### 1. Install

```bash
pip install mlx-control-center
```

### 2. First-Time Setup

```bash
mlx init
```

You'll be prompted for:
- **SSH host**: Your Mac's address (e.g., `user@mac.local` or `user@192.168.1.100`)
- **API URL**: Where the MLX API runs (default: `http://127.0.0.1:8080`)
- **API key**: Authentication token

### 3. Verify

```bash
mlx status
```

Should show Mac hardware and API status.

## Usage

### Interactive Menu
```bash
mlx
```

### Direct Commands
```bash
mlx chat              # Quick chat with a model
mlx editor            # Advanced chat (system prompt, parameters)
mlx models            # Manage cached models
mlx monitor           # System monitor (btop)
mlx network           # Network monitor (nettop)
mlx status            # System status
mlx logs              # Live API logs
mlx config            # Edit settings
mlx --help            # Help
```

## Mac Setup

Before using this tool, you need:

1. **MLX API Server** running on the Mac
2. **Python venv** with dependencies
3. **SSH access** (key-based auth recommended)

### On Your Mac

```bash
# 1. Clone or download the MLX API server
# (This example assumes it's at ~/security-ai/multi-model-api)

# 2. Create venv
cd ~/security-ai
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install mlx mlx-lm huggingface_hub

# 4. Start the server
python multi-model-api/server.py
```

The server should listen on `http://127.0.0.1:8080` (or configure via `MLX_API_URL`).

### SSH Configuration

For passwordless access:
```bash
# On your Arch machine
ssh-copy-id timkusenko@your-mac-ip
```

## Configuration

### Files

- **Settings**: `~/.config/mlx-control/settings.json`
  - `temperature` (0.0–2.0, default 0.7)
  - `max_tokens` (1–8192, default 512)
- **System Prompt**: `~/.config/mlx-control/system-prompt.txt`
- **API Key**: `~/.config/mlx-api/api-key` (mode 0600, never commit)

### Environment Variables

```bash
export MLX_MAC_HOST="user@your-mac-ip"
export MLX_API_URL="http://api-server:8080"
```

## Architecture

```
mlx_control/
├── __main__.py         Command routing
├── commands.py         All menu handlers
├── config.py           Settings management
├── api.py              HTTP API client
├── ssh_remote.py       SSH operations
├── models.py           Model parsing
├── chat.py             Chat session
├── huggingface.py      HF model download/delete
└── cli.py              Menu utilities
```

## Development

### Setup

```bash
git clone https://github.com/your-org/mlx-control-center
cd mlx-control-center
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Testing

```bash
pytest tests/ -v
black mlx_control tests
mypy mlx_control --ignore-missing-imports
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Requirements

- **Python** 3.9+
- **SSH access** to Mac mini
- **MLX API server** running on Mac
- Standard library only (no pip dependencies for the client)

## Troubleshooting

### "API: OFFLINE"
- Confirm MLX API server is running on Mac: `curl http://localhost:8080/status`
- Check `MLX_API_URL` environment variable
- Verify network connectivity to Mac

### "Mac: Unreachable"
- Test SSH: `ssh user@your-mac.local 'uname -a'`
- Check `MLX_MAC_HOST` environment variable
- Ensure SSH key is configured

### "No API key"
- Run `mlx init` to set up credentials
- Manually create: `~/.config/mlx-api/api-key` with your token

## License

MIT – See [LICENSE](LICENSE)

## Author

Tim Kusenko

---

**GitHub**: https://github.com/your-org/mlx-control-center  
**Issues**: Report bugs and feature requests on GitHub
