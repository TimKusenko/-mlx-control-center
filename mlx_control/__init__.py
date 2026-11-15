"""MLX Control Center — Remote control for MLX inference API."""

__version__ = "2.0.0"
__author__ = "Contributors"
__description__ = "Remote control and monitoring for MLX models running on your Mac"

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
