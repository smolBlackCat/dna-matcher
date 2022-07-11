"""Multiplatform module for file dialogs."""

import sys


def fd(win_title: str = None) -> str:
    if sys.platform == "linux":
        from zenipy import file_selection
        result = file_selection(title=win_title, multiple=False)
        return result
    else:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        result = filedialog.askopenfilename()
        return result
