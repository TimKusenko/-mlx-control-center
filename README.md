# MLX Control Center

**Remote Control for MLX on Mac** – Chat with LLM models running on your Mac mini, from your Arch Linux laptop.

This is a **remote controller** (Fernbedienung). The AI models run on your Mac. You control them from your laptop via SSH.

## How It Works (In Plain English)

```
Your Laptop (Arch)        SSH          Mac mini
┌──────────────┐      ┌────────┐      ┌─────────────┐
│ mlx chat     │ ────►│  SSH   │─────►│ MLX Server  │
│ (you type)   │      └────────┘      │ (AI runs)   │
└──────────────┘      ◄────────┐      └─────────────┘
                       Answers  └──────►
```

1. **You** type a question on your laptop
2. **This tool** sends it via SSH to your Mac
3. **Mac's MLX** generates an answer (AI runs there)
4. **Answer** comes back to your laptop
5. **You see** the result

---

## What You Need

### ✅ On Your Mac (The AI Computer)

MLX framework installed and running. Something like:
```bash
brew install mlx-lm
pip install huggingface_hub
# MLX server listening on http://127.0.0.1:8080
```

### ✅ On Your Laptop (The Remote Control)

This tool:
```bash
pip install mlx-control-center
mlx init
mlx chat
```

---

## Quick Start (5 Steps)

### 1. Make Sure MLX Runs on Mac

```bash
# On your Mac:
python ~/security-ai/multi-model-api/server.py
# or systemctl --user start mlx-api
```

Server should be on `http://127.0.0.1:8080` (or note the URL).

### 2. Install Tool on Laptop

```bash
pip install mlx-control-center
```

### 3. Setup (One Time)

```bash
mlx init

# Asks:
# - Your Mac's address? → tim@192.168.178.49 (or your-mac.local)
# - API URL? → (just press Enter for default)
# - API key? → (your auth token)

# Done!
```

### 4. Test

```bash
mlx status

# Should show Mac is reachable + API online
```

### 5. Chat!

```bash
mlx chat

# → Pick model → Ask question → Get answer
```

---

## Commands

```bash
mlx              # Open menu (all options)
mlx chat         # Quick chat with AI
mlx editor       # Chat + system prompt + settings
mlx models       # Download/delete models
mlx monitor      # Watch CPU/RAM on Mac (btop)
mlx network      # Watch network traffic (nettop)
mlx status       # Quick system check
mlx logs         # See API errors live
mlx config       # Edit settings
mlx init         # Setup again
```

---

## Configuration

Your settings are saved in:
- `~/.config/mlx-control/settings.json` – temperature, max_tokens
- `~/.config/mlx-control/system-prompt.txt` – your custom AI instructions
- `~/.config/mlx-api/api-key` – your authentication (secret!)

---

## Troubleshooting

### "Mac: Unreachable"
```bash
# Check SSH connection:
ssh tim@192.168.178.49 'uname -a'

# Check MLX_MAC_HOST env var:
echo $MLX_MAC_HOST
```

### "API: OFFLINE"
```bash
# Check server is running on Mac:
curl http://127.0.0.1:8080/status

# Check MLX_API_URL env var:
echo $MLX_API_URL
```

### "No API key"
```bash
# Run setup again:
mlx init
```

---

## Requirements

- **Python** 3.9+
- **SSH access** to your Mac
- **MLX server** running on Mac (listening on a port)
- **Network**: Laptop and Mac on same WiFi

---

## Architecture

```
mlx_control/
├── __main__.py       Command routing
├── commands.py       All menu handlers
├── config.py         Settings & API key storage
├── api.py            Talk to MLX server
├── ssh_remote.py     Control Mac via SSH
├── models.py         Parse model names
├── chat.py           Chat session logic
├── huggingface.py    Download/delete models
└── cli.py            Menu UI
```

---

## Development

### Setup

```bash
git clone https://github.com/your-org/mlx-control-center
cd mlx-control-center
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Test

```bash
pytest tests/
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## License

MIT – [LICENSE](LICENSE)

## Author

Tim Kusenko

---

**Questions?** Check [SECURITY.md](SECURITY.md) or open an issue on GitHub.
