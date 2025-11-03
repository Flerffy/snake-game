"""Legacy helpers kept for backward compatibility.

Sound management has been moved to `sounds.py`. These thin wrappers keep the
old `utils.init_beep()` / `utils.get_beep_sound()` API working while forwarding
to the new implementation.
"""

from sounds import init_sounds, get_sfx, play_sfx  # re-export helpers
import os
import sys


def resource_path(relative_path: str) -> str:
    """Return an absolute path to a resource, working for dev and PyInstaller.

    When running as a PyInstaller bundle, PyInstaller extracts bundled files to
    a temporary folder accessible via sys._MEIPASS. This helper returns the
    correct path to use for file loads in both development and frozen modes.
    """
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path is None:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def init_beep(*args, **kwargs):
    """Initialize builtin beep SFX (wrapper around sounds.init_sounds)."""
    return init_sounds(*args, **kwargs)


def get_beep_sound():
    """Return the cached pygame.mixer.Sound for the built-in 'beep'."""
    return get_sfx('beep')


def play_beep(volume=None):
    """Convenience wrapper to play the built-in beep SFX."""
    return play_sfx('beep', volume=volume)
