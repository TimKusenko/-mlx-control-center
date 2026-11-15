"""Command handlers for all menu options."""
import logging
from typing import Callable

from .api import APIClient
from .config import Config
from .ssh_remote import SSHClient
from .huggingface import HuggingFaceManager
from .chat import ChatSession
from .models import ModelGrouper
from .cli import gib

logger = logging.getLogger(__name__)


class Commands:
    """All menu commands."""

    def __init__(self, api: APIClient, config: Config, ssh: SSHClient):
        self.api = api
        self.config = config
        self.ssh = ssh
        self.hf = HuggingFaceManager(ssh)

    def chat_mode(self) -> None:
        """Quick chat mode."""
        if not self.api:
            print("❌ API not configured.")
            return

        try:
            models = self.api.get_models()
            if not models:
                print("❌ No models available.")
                return

            grouped = ModelGrouper.group_models(models)
            families = sorted(grouped.keys())

            if not families:
                print("❌ No models found.")
                return

            print(f"\n📚 Found {len(families)} model families")
            choice = self._select_option(families, "Select model family")
            if not choice:
                return

            sizes = sorted(grouped[choice].keys(),
                          key=lambda x: self._parse_size(x))
            choice = self._select_option(sizes, "Select size")
            if not choice:
                return

            options = grouped[choice]
            choice_str = self._select_option(
                [f"{q:<12} {mid}" for q, mid in options],
                "Select quantization"
            )
            if not choice_str:
                return

            model_id = options[[f"{q:<12} {mid}" for q, mid in options].index(choice_str)][1]
            session = ChatSession(self.api, self.config, model_id, "", editor_mode=False)
            session.run()
        except Exception as exc:
            logger.error(f"Chat error: {exc}", exc_info=True)
            print(f"❌ Error: {exc}")

    def editor_mode(self) -> None:
        """Advanced mode with system prompt."""
        if not self.api:
            print("❌ API not configured.")
            return

        try:
            active = self.api.get_active_model()
            model_id = None

            if active:
                print(f"✅ Active model: {active}")
                ans = input("Use it? [Y/n]: ").strip().lower()
                if ans not in ("n", "no"):
                    model_id = active

            if not model_id:
                models = self.api.get_models()
                if not models:
                    print("❌ No models available.")
                    return
                model_id = models[0]
                print(f"Using: {model_id}")

            prompt = self.config.get_system_prompt()
            session = ChatSession(self.api, self.config, model_id, prompt, editor_mode=True)
            session.run()
        except Exception as exc:
            logger.error(f"Editor error: {exc}", exc_info=True)
            print(f"❌ Error: {exc}")

    def models_menu(self) -> None:
        """Model management."""
        if not self.api:
            print("❌ API not configured.")
            return

        while True:
            print("\n=== MODELS ===")
            try:
                active = self.api.get_active_model()
                print(f"Active: {active or 'None'}")
            except Exception:
                pass

            choice = self._select_option(
                ["List cached", "Search & download", "Delete", "Back"],
                "Action"
            )

            if not choice or choice == "Back":
                break
            elif choice == "List cached":
                try:
                    self.hf.list_cache()
                except Exception as exc:
                    print(f"❌ {exc}")
            elif choice == "Search & download":
                try:
                    family = input("Search (e.g., Llama-3.2): ").strip()
                    if not family:
                        continue
                    results = self.hf.search_mlx_community(family)
                    if not results:
                        print("❌ Not found.")
                        continue
                    selected = self._select_option(results, "Models")
                    if selected:
                        confirm = input(f"Download {selected}? Type 'DOWNLOAD {selected}': ").strip()
                        if confirm == f"DOWNLOAD {selected}":
                            self.hf.download_model(selected)
                            print("✅ Download started.")
                except Exception as exc:
                    logger.error(f"Download: {exc}", exc_info=True)
                    print(f"❌ {exc}")
            elif choice == "Delete":
                try:
                    repo = input("Enter repo ID (0=cancel): ").strip()
                    if repo in ("", "0"):
                        continue
                    active = self.api.get_active_model()
                    if repo == active:
                        print("❌ Cannot delete active model.")
                        continue
                    confirm = input(f"Delete {repo}? Type 'DELETE {repo}': ").strip()
                    if confirm == f"DELETE {repo}":
                        self.hf.delete_model(repo)
                        print("✅ Deleted.")
                except Exception as exc:
                    logger.error(f"Delete: {exc}", exc_info=True)
                    print(f"❌ {exc}")

    def monitor(self) -> None:
        """System monitor."""
        print("📊 btop (press 'q' to exit)")
        try:
            self.ssh.btop()
        except Exception as exc:
            print(f"❌ {exc}")

    def network(self) -> None:
        """Network monitor."""
        print("🌐 nettop (press 'q' to exit)")
        try:
            self.ssh.nettop()
        except Exception as exc:
            print(f"❌ {exc}")

    def status(self) -> None:
        """System status."""
        print("\n=== STATUS ===")
        if self.api:
            try:
                st = self.api.get_status()
                print(f"🌐 API: ONLINE")
                print(f"   Model: {st.get('active_model') or 'None'}")
                print(f"   Backend: {'running' if st.get('backend_running') else 'inactive'}")
                models = self.api.get_models()
                print(f"   Models: {len(models)}")
            except Exception as exc:
                print(f"🌐 API: OFFLINE – {exc}")
        else:
            print("🌐 API: Not configured")

        try:
            hw = self.ssh.get_hardware_info()
            print(f"\n🖥️  Mac: {hw['hostname']}")
            print(f"   CPU: {hw['cpu']}")
            print(f"   Cores: {hw['cores']}")
            print(f"   RAM: {gib(hw['memory_approx_used'])} / {gib(hw['memory_total'])}")
            print(f"   SSD: {gib(hw['disk_total'] - hw['disk_free'])} / {gib(hw['disk_total'])}")
        except Exception as exc:
            print(f"🖥️  Mac: Unreachable – {exc}")

    def logs(self) -> None:
        """View live logs."""
        print("📋 Logs (Ctrl+C to stop)")
        try:
            log_path = "~/security-ai/multi-model-api/logs"
            choice = self._select_option(
                ["server.log", "error.log"],
                "Which log?"
            )
            if choice:
                self.ssh.tail_log(f"{log_path}/{choice}")
        except Exception as exc:
            print(f"❌ {exc}")

    def config(self) -> None:
        """Configuration."""
        while True:
            settings = self.config.load_settings()
            print("\n=== CONFIG ===")
            print(f"Mac: {self.config.mac_host}")
            print(f"API: {self.config.api_url}")
            print(f"Temperature: {settings['temperature']}")
            print(f"Max tokens: {settings['max_tokens']}")

            choice = self._select_option(
                ["Set system prompt", "Temperature", "Max tokens", "Back"],
                "Edit"
            )

            if not choice or choice == "Back":
                break
            elif choice == "Set system prompt":
                print("Enter prompt (empty line ends, '.cancel' aborts):")
                lines = []
                while True:
                    line = input("> ")
                    if line == ".cancel":
                        break
                    if line == "":
                        break
                    lines.append(line)
                if lines:
                    prompt = "\n".join(lines)
                    self.config.save_system_prompt(prompt)
                    print("✅ Saved.")
            elif choice == "Temperature":
                try:
                    val = float(input("Temperature [0.0–2.0]: "))
                    if 0 <= val <= 2:
                        settings["temperature"] = val
                        self.config.save_settings(settings)
                        print("✅ Saved.")
                    else:
                        print("❌ Out of range.")
                except ValueError:
                    print("❌ Invalid number.")
            elif choice == "Max tokens":
                try:
                    val = int(input("Max tokens [1–8192]: "))
                    if 1 <= val <= 8192:
                        settings["max_tokens"] = val
                        self.config.save_settings(settings)
                        print("✅ Saved.")
                    else:
                        print("❌ Out of range.")
                except ValueError:
                    print("❌ Invalid number.")

    def _select_option(self, items, title="Select") -> str:
        """Select from list."""
        print(f"\n=== {title} ===")
        for i, item in enumerate(items, 1):
            print(f"{i:>2}. {item}")
        print(" 0. Cancel")
        try:
            choice = input("> ").strip()
            if choice == "0" or not choice:
                return ""
            if choice.isdigit() and 1 <= int(choice) <= len(items):
                return items[int(choice) - 1]
            return ""
        except (KeyboardInterrupt, EOFError):
            return ""

    @staticmethod
    def _parse_size(size_str: str) -> float:
        """Parse size string to number for sorting."""
        import re
        match = re.search(r"\d+(?:\.\d+)?", size_str)
        return float(match.group()) if match else 999
