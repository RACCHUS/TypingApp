import tkinter as tk
from ui.keyboard import VirtualKeyboard

class KeyboardContainer(tk.Frame):
    def __init__(self, master, key_buttons, *args, **kwargs):
        super().__init__(master, bg="#181A1B", highlightbackground="#23272A", highlightthickness=2, width=600, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)
        self.keyboard_frame = VirtualKeyboard(self, key_buttons)
        self.keyboard_frame.pack(fill="both", expand=True, padx=30)
