# MLX Control Center

Control your Mac's MLX models from your laptop. Chat, manage models, monitor performance.

SSH-based remote controller for MLX on Mac.

## How It Works

```
Your Computer        SSH           Your Mac
[mlx chat]  ────►  [tunnel]  ────►  [MLX Server]
            ◄────  [return]  ◄────  [Running]
```

Type on your computer. Models run on your Mac.

## Install

```bash
pip install mlx-control-center
```

## Quick Start

### 1. Mac: Start MLX Server

```bash
python ~/mlx-server/server.py
# Should say: Server running on http://127.0.0.1:8080
```

### 2. Laptop: Setup

```bash
mlx init
# Asks for: Mac address, API URL, API key
```

### 3. Chat!

```bash
mlx chat
```

## Commands

```
mlx              Menu
mlx chat         Quick chat
mlx editor       Chat with system prompt
mlx models       Download/delete models
mlx monitor      CPU/RAM monitor
mlx network      Network stats
mlx status       System check
mlx logs         API logs
mlx config       Settings
```

## Config

Settings stored in:
- `~/.config/mlx-control/settings.json`
- `~/.config/mlx-control/system-prompt.txt`
- `~/.config/mlx-api/api-key`

## Requirements

- Python 3.9+
- SSH to Mac
- MLX server running
- No external dependencies

## Setup Details

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions.

## Troubleshooting

### Mac unreachable
```bash
ssh user@your-mac 'uname -a'
```

### API offline
```bash
curl http://127.0.0.1:8080/status
```

### No API key
```bash
mlx init
```

## License

MIT
