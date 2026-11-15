# Changelog

All notable changes to this project will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/)  
Versioning: [Semantic Versioning](https://semver.org/)

## [2.0.0] – 2026-11-15

### Added

**Complete Refactor from Monolithic → Modular**
- Original v1: 665-line monolithic `mlx-control-center.py`
- v2.0: Clean package with 8 focused modules
  - `commands.py` – All menu handlers (chat, models, monitor, logs, config)
  - `config.py` – Settings, API keys, system prompts
  - `api.py` – HTTP client with error handling
  - `ssh_remote.py` – Remote Mac operations (btop, nettop, hardware info)
  - `models.py` – Model parsing (family/size/quantization)
  - `chat.py` – Chat session management
  - `huggingface.py` – Model download/delete from HuggingFace
  - `cli.py` – Menu and input utilities

**Full Feature Set**
- Interactive menu with 8 commands
- Subcommands: `mlx chat`, `mlx editor`, `mlx models`, `mlx status`, `mlx logs`, `mlx config`
- `mlx init` – First-time setup wizard (SSH host, API URL, API key)
- Live system monitoring (btop, nettop)
- Real-time log streaming
- Model management (list, download, delete with safety checks)
- Advanced chat editor (system prompt, temperature, max_tokens)
- Configuration management (CLI + file-based)

**Quality & Reliability**
- 13 unit tests (config, API client, model parsing)
- Type hints throughout
- Proper error handling with logging
- SSH connection validation
- Safety checks (don't delete active model, size limits, key validation)

**Setup & Docs**
- `pyproject.toml` – Modern Python packaging
- `README.md` – Complete setup guide for users and Mac configuration
- `CONTRIBUTING.md` – Developer guide (setup, testing, commit messages)
- `.github/workflows/test.yml` – GitHub Actions (Python 3.9-3.12, pytest, black, mypy)
- `Makefile` – Common tasks (`make test`, `make lint`, `make format`)
- `.gitignore` – Proper Python ignore rules

**Security**
- API key stored in `~/.config/mlx-api/api-key` (mode 0600)
- No hardcoded secrets or personal data
- SSH key-based auth recommended
- Config directory permissions (0700)

### Changed

- **Language**: English (international)
- **API Key Handling**: Secure file storage instead of plaintext env vars
- **Default Host**: Generic prompt instead of hardcoded IP
- **Error Messages**: Clearer, emoji-marked indicators
- **Logging**: Proper Python logging module (not prints)

### Removed

- Monolithic single-file design
- Mixed German/English UI strings
- Hardcoded personal configurations (IP address, account names)
- Inline shell scripts (replaced with proper Python functions)

### Fixed

- SSH connection timeout handling
- Model deletion safety (protect active model)
- HuggingFace API error reporting
- Missing status displays in menu

### Known Limitations

- Chat history not persisted between sessions
- No local model caching (relies on Mac's cache)
- Monitor/network commands are interactive only (no batch output)
- Logs require live API server (no historical log storage on client)

## [1.0.0] – 2024-11-08

Initial release:
- SSH tunnel to Mac mini
- Chat interface with model selection
- System monitoring (btop, nettop)
- Basic model management
- Configuration UI
- Status diagnostics
- Single-file script (665 lines)

---

## Upgrade Guide: v1 → v2

**No Breaking Changes** – All existing configs are compatible.

1. **Install v2.0**:
   ```bash
   pip install --upgrade mlx-control-center
   ```

2. **Settings are preserved**:
   - `~/.config/mlx-control/settings.json` – unchanged
   - `~/.config/mlx-control/system-prompt.txt` – unchanged

3. **API key location**:
   - Old: `MLX_API_KEY` environment variable
   - New: `~/.config/mlx-api/api-key`
   
   Move existing key:
   ```bash
   mkdir -p ~/.config/mlx-api
   echo "$MLX_API_KEY" > ~/.config/mlx-api/api-key
   chmod 600 ~/.config/mlx-api/api-key
   ```

4. **No config migration needed** – First run will auto-detect old settings.

---

## Future Roadmap

- [ ] Persistent chat history (SQLite or JSON)
- [ ] Web UI (optional FastAPI server)
- [ ] Model quantization helpers
- [ ] Batch file operations
- [ ] Metrics/telemetry dashboard
- [ ] Docker support for the API server
