# MLX Control Center

**Remote control for MLX** – Chat with LLM models running on your Mac, from your laptop, via SSH.

This tool is a **remote controller**. AI models run on your Mac. You control them from your laptop.

---

## How It Works

```
Your Computer          SSH          Your Mac
┌──────────────┐   ┌────────┐   ┌──────────────┐
│ mlx chat     │──►│  SSH   │──►│ MLX Server   │
│ Type question│   └────────┘   │ Runs AI      │
└──────────────┘   ◄────────┐   └──────────────┘
                    Answers  └────►
```

1. You type on your computer
2. Tool sends via SSH to your Mac
3. Mac's MLX generates answer
4. Answer returns to your computer

---

## What You Need

**On Your Mac:**
- MLX framework installed
- API server running (listens on a port, e.g., `http://127.0.0.1:8080`)
- SSH enabled (default)

**On Your Computer:**
- Python 3.9+
- This tool: `pip install mlx-control-center`
- SSH access to your Mac

**Network:**
- Both devices on same network
- SSH working between them

---

## Quick Start

### 1. Ensure MLX Runs on Mac

```bash
# On your Mac:
python ~/path/to/mlx/server.py
# Should say: Server running on http://127.0.0.1:8080
```

### 2. Install on Your Computer

```bash
pip install mlx-control-center
```

### 3. Setup (Once)

```bash
mlx init

# Asks:
# Your Mac's address? → user@your-mac.local (or IP)
# API URL? → (default is fine)
# API key? → (your auth token)
```

### 4. Test

```bash
mlx status
# Should show Mac is reachable
```

### 5. Chat!

```bash
mlx chat
# Pick a model → Ask question → Get answer
```

---

## Commands

```bash
mlx              # Menu (all options)
mlx chat         # Quick chat
mlx editor       # Chat with system prompt
mlx models       # Download/delete models
mlx monitor      # Watch Mac (CPU/RAM)
mlx network      # Watch network traffic
mlx status       # System check
mlx logs         # Live API logs
mlx config       # Edit settings
mlx init         # Setup again
```

---

## Configuration

Settings stored in:
- `~/.config/mlx-control/settings.json` – Temperature, max tokens
- `~/.config/mlx-control/system-prompt.txt` – Your custom system message
- `~/.config/mlx-api/api-key` – Your auth token (secret!)

---

## Troubleshooting

### "Mac: Unreachable"
```bash
# Test SSH connection:
ssh user@your-mac-address 'uname -a'

# Check environment variable:
echo $MLX_MAC_HOST
```

### "API: OFFLINE"
```bash
# Check MLX server is running on Mac:
curl http://127.0.0.1:8080/status

# Check URL is correct:
echo $MLX_API_URL
```

### "No API key"
```bash
# Setup again:
mlx init
```

---

## Requirements

- Python 3.9+
- SSH access to Mac
- MLX server running on Mac
- Both on same network

**No external dependencies** – Uses Python standard library only.

---

## Architecture

```
mlx_control/
├── __main__.py         Command routing
├── commands.py         All menu handlers
├── config.py           Settings & secrets
├── api.py              HTTP client
├── ssh_remote.py       SSH operations
├── models.py           Model parsing
├── chat.py             Chat logic
├── huggingface.py      Model management
└── cli.py              Menu interface
```

---

## Development

### Setup

```bash
git clone https://github.com/your-username/mlx-control-center
cd mlx-control-center
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Test

```bash
pytest tests/
```

### Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## License

MIT – [LICENSE](LICENSE)

## Authors

Contributors

---

For help: See [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions.
