"""Command-line interface and menu system."""
import logging
from typing import Callable, List, Optional, Tuple

logger = logging.getLogger(__name__)


def format_size(bytes_val: float) -> str:
    """Format bytes to human-readable size."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"


def gib(n: float) -> str:
    """Format bytes to GiB."""
    return f"{n / (1024 ** 3):.1f} GB"


class Menu:
    """Generic menu system."""

    def __init__(self, title: str):
        self.title = title
        self.options: List[Tuple[str, str, Callable]] = []

    def add(self, name: str, description: str, handler: Callable) -> None:
        """Add menu option."""
        self.options.append((name, description, handler))

    def select(self, items: List[str], title: str = "Selection") -> Optional[str]:
        """Present selection menu."""
        print(f"\n=== {title} ===")
        for i, item in enumerate(items, 1):
            print(f"{i:>2}. {item}")
        print(" 0. Back")

        while True:
            try:
                value = input("Choice > ").strip()
                if value in ("0", ""):
                    return None
                if value.isdigit() and 1 <= int(value) <= len(items):
                    return items[int(value) - 1]
                print("Invalid selection. Try again.")
            except (KeyboardInterrupt, EOFError):
                print("\nCancelled.")
                return None

    def run(self) -> None:
        """Display menu and run selected option."""
        while True:
            print(f"\n=== {self.title} ===")
            for i, (name, desc, _) in enumerate(self.options, 1):
                print(f"{i:>2}. {name:<12} {desc}")
            print(" 0. Back")

            try:
                choice = input("Choice > ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                return

            if choice == "0":
                return

            if choice.isdigit() and 1 <= int(choice) <= len(self.options):
                name, _, handler = self.options[int(choice) - 1]
                try:
                    handler()
                except (KeyboardInterrupt, EOFError):
                    print("\nCancelled.")
                except Exception as exc:
                    logger.error(f"Error in {name}: {exc}", exc_info=True)
                    print(f"Error: {exc}")
                    input("\nPress Enter to continue... ")
            else:
                print("Invalid choice.")


def prompt_confirm(message: str, default: bool = False) -> bool:
    """Ask for yes/no confirmation."""
    prompt = f"{message} ({'Y/n' if default else 'y/N'}): "
    ans = input(prompt).strip().lower()
    if default:
        return ans not in ("n", "no")
    else:
        return ans in ("y", "yes")


def prompt_secret(message: str) -> str:
    """Prompt for password/secret input."""
    import getpass
    return getpass.getpass(message)
