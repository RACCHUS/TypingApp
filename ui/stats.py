import tkinter as tk

class StatsPanel(tk.Frame):
    def __init__(self, master, wpm_var, correct_wpm_var, accuracy_var, keystrokes_var, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(bg="#181A1B")
        stat_style = {"font": ("Segoe UI", 14, "bold"), "bg": "#23272A", "padx": 18, "pady": 8, "bd": 0, "relief": "flat"}
        self.wpm_label = tk.Label(self, textvariable=wpm_var, **stat_style, fg="#00e676")
        self.wpm_label.pack(side="left", padx=10)
        self.correct_wpm_label = tk.Label(self, textvariable=correct_wpm_var, **stat_style, fg="#29b6f6")
        self.correct_wpm_label.pack(side="left", padx=10)
        self.accuracy_label = tk.Label(self, textvariable=accuracy_var, **stat_style, fg="#ffb300", highlightbackground="#ffb300", highlightthickness=2)
        self.accuracy_label.pack(side="left", padx=10)
        self.keystrokes_label = tk.Label(self, textvariable=keystrokes_var, **stat_style, fg="#fdd835")
        self.keystrokes_label.pack(side="left", padx=10)
        # Checkmark label (hidden by default)
        self.checkmark_label = tk.Label(self, text="\u2714", font=("Segoe UI", 20, "bold"), fg="#00c853", bg="#23272A")
        self.checkmark_label.pack(side="left", padx=10)
        self.checkmark_label.pack_forget()

    def show_checkmark(self):
        self.checkmark_label.pack(side="left", padx=10)

    def hide_checkmark(self):
        self.checkmark_label.pack_forget()
