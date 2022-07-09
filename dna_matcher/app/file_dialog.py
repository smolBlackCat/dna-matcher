"""Multiplatform module for file dialogs."""

from zenipy import file_selection
from tkinter import filedialog
import sys

def _unix_file_dialog(win_title: str, win_text: str) -> str:
    result = file_selection(title=win_title, text=win_text)
    return result


def _windows_file_dialog(win_title: str, win_text: str) -> str:
    result = filedialog.askopenfilename()
    return result


def file_dialog(win_title: str, win_text: str) -> str:
    if sys.platform == "win32":
        return _windows_file_dialog(win_title, win_text)
    elif sys.platform == "linux":
        return _unix_file_dialog(win_title, win_text)
