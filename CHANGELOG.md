# Changelog

## 2.0.0 (2026-11-15)

Complete rewrite with modular architecture.

### New
- 8 subcommands: chat, editor, models, monitor, network, status, logs, config
- First-time setup wizard (mlx init)
- System monitoring (btop, nettop)
- Model download/delete from Hugging Face
- Live API log streaming
- Configuration management (settings file, system prompts)

### Improved
- Modular code: 10 separate files instead of one 665-line script
- Proper error handling with logging
- Type hints throughout
- Security: API keys stored safely (mode 0600)
- Documentation: setup guide, security info, contributing guide

### Tests
- 13 unit tests for config, API, models
- GitHub Actions CI (pytest, black, mypy)

### Requirements
- Python 3.9+
- SSH access to Mac
- MLX server running on Mac
- No external dependencies (stdlib only)

---

## 1.0.0 (2024-11-08)

Initial release. Single-file script with menu system.
