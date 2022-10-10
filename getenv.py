from os import environ
from typing import Any


def env(name: str, default_value: Any | None = None) -> Any | None:
    """Get an environment variable"""
    return environ.get(name, default_value)
