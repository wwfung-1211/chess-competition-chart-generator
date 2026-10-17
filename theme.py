"""Shared colours and portable Tkinter control styling."""
from tkinter import ttk

NAVY = "#374375"
CREAM = "#f5f3d8"
TEXT = "#20263d"
WHITE = "#ffffff"
WINNER = "#676d55"
LOSER = "#8c1d1a"
PENDING = "#626775"


def apply_theme(root):
    """Set explicit colours so system dark mode cannot hide text."""
    root.configure(background=NAVY)
    defaults = {
        "*Label.background": CREAM,
        "*Label.foreground": TEXT,
        "*Frame.background": CREAM,
        "*Text.background": WHITE,
        "*Text.foreground": TEXT,
        "*Text.insertBackground": TEXT,
        "*Text.selectBackground": NAVY,
        "*Text.selectForeground": WHITE,
        "*Menubutton.background": CREAM,
        "*Menubutton.foreground": TEXT,
        "*Menubutton.activeBackground": NAVY,
        "*Menubutton.activeForeground": WHITE,
        "*Menu.background": CREAM,
        "*Menu.foreground": TEXT,
        "*Menu.activeBackground": NAVY,
        "*Menu.activeForeground": WHITE,
        "*Canvas.background": CREAM,
    }
    for pattern, colour in defaults.items():
        root.option_add(pattern, colour)

    style = ttk.Style(root)
    # Clam honours custom button colours on macOS, unlike native Tk buttons.
    style.theme_use("clam")
    style.configure(
        "Chess.TButton", background=NAVY, foreground=WHITE,
        font=("Georgia", 10), borderwidth=1, padding=(10, 5),
        lightcolor=NAVY, darkcolor=NAVY, bordercolor=NAVY,
    )
    style.map(
        "Chess.TButton",
        background=[("disabled", PENDING), ("pressed", "#263054"), ("active", "#49598c")],
        foreground=[("disabled", "#eeeeee"), ("pressed", WHITE), ("active", WHITE)],
    )


def button(parent, **options):
    """Build a themed button using the existing window layout options."""
    for key in ("bg", "fg", "font"):
        options.pop(key, None)
    padding = (options.pop("padx", 10), options.pop("pady", 5))
    return ttk.Button(parent, style="Chess.TButton", padding=padding, **options)
