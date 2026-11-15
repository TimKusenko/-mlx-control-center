"""Chat interface for model interactions."""
import json
import logging
import time
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ChatSession:
    """Manage a chat conversation with a model."""

    def __init__(self, api_client, config, model_id: str, system_prompt: str = "", editor_mode: bool = False):
        self.api = api_client
        self.config = config
        self.model_id = model_id
        self.system_prompt = system_prompt
        self.editor_mode = editor_mode
        self.history: List[Dict[str, str]] = []
        self.settings = config.load_settings()

    def get_commands_help(self) -> str:
        """Return available commands."""
        cmds = "/exit /clear /stats"
        if self.editor_mode:
            cmds += " /system /temp /max /save"
        return cmds

    def handle_command(self, cmd: str) -> bool:
        """
        Process special commands.

        Returns True if handled, False to continue chat.
        """
        if cmd == "/exit":
            return True

        if cmd == "/clear":
            self.history.clear()
            print("History cleared.")
            return False

        if cmd == "/stats":
            print("Last response stats not yet tracked.")
            return False

        if not self.editor_mode:
            return False

        if cmd == "/system":
            print(f"Current prompt: {self.system_prompt or '(empty)'}")
            new_prompt = input("Enter new system prompt (empty = unchanged):\n> ").strip()
            if new_prompt:
                self.system_prompt = new_prompt
            return False

        if cmd == "/save":
            self.config.save_system_prompt(self.system_prompt)
            print(f"Prompt saved to {self.config.prompt_file}")
            return False

        if cmd == "/temp":
            try:
                val = float(input("Temperature [0.0–2.0] > "))
                if not 0 <= val <= 2:
                    raise ValueError()
                self.settings["temperature"] = val
                self.config.save_settings(self.settings)
                print(f"Temperature set to {val}")
            except ValueError:
                print("Invalid temperature.")
            return False

        if cmd == "/max":
            try:
                val = int(input("Max tokens [1–8192] > "))
                if not 1 <= val <= 8192:
                    raise ValueError()
                self.settings["max_tokens"] = val
                self.config.save_settings(self.settings)
                print(f"Max tokens set to {val}")
            except ValueError:
                print("Invalid value.")
            return False

        return False

    def run(self) -> None:
        """Run interactive chat loop."""
        print(f"\nModel: {self.model_id}")
        print(f"Commands: {self.get_commands_help()}")

        while True:
            try:
                user_input = input("\nYou > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nSession ended.")
                break

            if not user_input:
                continue

            if user_input.startswith("/"):
                if self.handle_command(user_input):
                    break
                continue

            self._send_message(user_input)

    def _send_message(self, user_input: str) -> None:
        """Send message to model and display response."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        messages.extend(self.history)
        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": self.model_id,
            "messages": messages,
            "max_tokens": self.settings["max_tokens"],
            "stream": False,
        }
        if self.editor_mode:
            payload["temperature"] = self.settings["temperature"]

        print("\nGenerating...")
        start = time.perf_counter()

        try:
            result = self.api.chat_completion(payload)
            elapsed = time.perf_counter() - start

            message = result.get("choices", [{}])[0].get("message", {})
            answer = message.get("content") or ""
            if not isinstance(answer, str):
                answer = json.dumps(answer, ensure_ascii=False)

            print(f"\nAI > {answer}")

            if self.editor_mode:
                reasoning = message.get("reasoning_content")
                if reasoning:
                    print(f"\nReasoning: {reasoning}")
                if message.get("tool_calls"):
                    print("Tool calls:", json.dumps(message["tool_calls"], indent=2))

            self.history.append({"role": "user", "content": user_input})
            self.history.append({"role": "assistant", "content": answer})

            usage = result.get("usage", {})
            tokens_out = usage.get("completion_tokens")
            rate = f"{tokens_out/elapsed:.1f}" if isinstance(tokens_out, int) and elapsed > 0 else "?"

            print(f"\nTime: {elapsed:.2f}s | In: {usage.get('prompt_tokens', '?')} | Out: {tokens_out} | Rate: {rate} tok/s")

        except Exception as exc:
            logger.error(f"Chat request failed: {exc}", exc_info=True)
            print(f"Error: {exc}")
