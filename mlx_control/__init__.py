"""Remote control for MLX on Mac."""

__version__ = "2.0.0"
__description__ = "Control MLX models on Mac from your computer via SSH"

from .config import Config
from .api import APIClient
from .ssh_remote import SSHClient
from .models import ModelGrouper
from .chat import ChatSession

__all__ = [
    "Config",
    "APIClient",
    "SSHClient",
    "ModelGrouper",
    "ChatSession",
]
