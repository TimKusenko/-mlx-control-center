"""Main entry point for MLX Control Center."""
import sys
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mlx-control")

from .config import Config
from .api import APIClient
from .ssh_remote import SSHClient
from .commands import Commands
from .cli import Menu


def show_help() -> None:
    """Show help message."""
    print("""
MLX Control Center – Mac mini LLM Model Manager

COMMANDS:
  mlx                  Interactive menu (default)
  mlx chat             Quick chat with model
  mlx editor           Advanced chat (system prompt)
  mlx models           Manage models
  mlx monitor          System CPU/RAM monitor
  mlx network          Network monitor
  mlx status           System status
  mlx logs             Live API logs
  mlx config           Edit configuration
  mlx init             First-time setup
  mlx --help           This help

SETUP (first time):
  $ mlx init           Configure SSH host and API key

ENVIRONMENT:
  MLX_MAC_HOST         SSH host (default: user@your-mac.local)
  MLX_API_URL          API URL (default: http://127.0.0.1:8080)

DOCS:
  https://github.com/your-org/mlx-control-center

For questions: Tim Kusenko <timkusenko.tk@gmail.com>
""")


class MLXApp:
    """Main application."""

    def __init__(self):
        self.config = Config()
        self.config.ensure_dirs()

        try:
            key = self.config.get_api_key()
            self.api = APIClient(self.config.api_url, key)
        except RuntimeError:
            logger.debug("API not configured")
            self.api = None

        self.ssh = SSHClient(self.config.mac_host)
        self.cmd = Commands(self.api, self.config, self.ssh)

    def dashboard(self) -> None:
        """Quick status dashboard."""
        print("\n" + "=" * 60)
        print("       MLX CONTROL CENTER v2.0")
        print("=" * 60)

        if self.api:
            try:
                st = self.api.get_status()
                model = st.get("active_model") or "None"
                backend = "🟢 running" if st.get("backend_running") else "🔴 inactive"
                print(f"🌐 API: ONLINE  |  Model: {model}  |  Backend: {backend}")
            except Exception as exc:
                print(f"🌐 API: OFFLINE – {str(exc)[:50]}")
        else:
            print("🌐 API: NOT CONFIGURED – Run 'mlx init'")

        try:
            from .cli import gib
            hw = self.ssh.get_hardware_info()
            print(f"🖥️  Mac: {hw['hostname']} | {hw['cores']} cores")
            print(f"   RAM: {gib(hw['memory_approx_used'])} / {gib(hw['memory_total'])}  |  "
                  f"SSD: {gib(hw['disk_total'] - hw['disk_free'])} / {gib(hw['disk_total'])}")
        except Exception:
            print("🖥️  Mac: Unreachable")

        print("-" * 60)

    def menu(self) -> None:
        """Interactive menu."""
        m = Menu("MLX CONTROL CENTER")
        m.add("chat", "Chat with model", self.cmd.chat_mode)
        m.add("editor", "Advanced chat", self.cmd.editor_mode)
        m.add("models", "Manage models", self.cmd.models_menu)
        m.add("monitor", "System monitor", self.cmd.monitor)
        m.add("network", "Network monitor", self.cmd.network)
        m.add("status", "System status", self.cmd.status)
        m.add("logs", "Live logs", self.cmd.logs)
        m.add("config", "Configuration", self.cmd.config)

        while True:
            self.dashboard()
            m.run()
            break

    def init_setup(self) -> None:
        """First-time setup."""
        print("\n=== MLX CONTROL CENTER SETUP ===\n")

        print("Step 1: SSH to Mac mini")
        default_host = "user@your-mac.local"
        host = input(f"SSH host [{default_host}]: ").strip()
        if not host:
            host = default_host

        print("\nStep 2: API URL")
        default_api = "http://127.0.0.1:8080"
        api_url = input(f"API URL [{default_api}]: ").strip()
        if not api_url:
            api_url = default_api

        print("\nStep 3: API Key")
        import getpass
        key = getpass.getpass("API key (hidden): ").strip()
        if not key:
            print("❌ API key required.")
            return

        # Save to config
        key_file = self.config.api_key_file
        key_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        key_file.write_text(key)
        key_file.chmod(0o600)

        print(f"\n✅ Configuration saved!")
        print(f"   SSH host: {host}")
        print(f"   API URL: {api_url}")
        print(f"   API key: {key_file}")
        print("\nTest connection with: mlx status")


def main() -> int:
    """Entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        if arg in ("--help", "-h", "help"):
            show_help()
            return 0

        if arg == "init":
            app = MLXApp()
            app.init_setup()
            return 0

        # Command routing
        app = MLXApp()

        if arg == "chat":
            app.cmd.chat_mode()
        elif arg == "editor":
            app.cmd.editor_mode()
        elif arg == "models":
            app.cmd.models_menu()
        elif arg == "monitor":
            app.cmd.monitor()
        elif arg == "network":
            app.cmd.network()
        elif arg == "status":
            app.cmd.status()
        elif arg == "logs":
            app.cmd.logs()
        elif arg == "config":
            app.cmd.config()
        else:
            print(f"❌ Unknown command: {arg}\n")
            show_help()
            return 1

        return 0

    # Default: interactive menu
    try:
        app = MLXApp()
        app.menu()
        return 0
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 130
    except Exception as exc:
        logger.error(f"Fatal: {exc}", exc_info=True)
        print(f"\n❌ {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
