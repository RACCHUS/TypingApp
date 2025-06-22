import tkinter as tk

def create_titlebar(parent, wpm_var, correct_wpm_var, accuracy_var, keystrokes_var, reset_callback):
    title_frame = tk.Frame(parent, bg="#23272A", height=50)
    from ui.stats import StatsPanel
    stats_panel = StatsPanel(title_frame, wpm_var, correct_wpm_var, accuracy_var, keystrokes_var)
    stats_panel.pack(side="left", padx=20)
    button_frame = tk.Frame(title_frame, bg="#23272A")
    button_frame.pack(side="right", padx=18, pady=8)
    reset_btn = tk.Button(
        button_frame, text="New", command=reset_callback,
        bg="#00acc1", fg="white", font=("Segoe UI", 11, "bold"),
        relief="flat", padx=12, pady=4, cursor="hand2", bd=0, highlightthickness=0
    )
    reset_btn.pack()
    return title_frame, stats_panel
