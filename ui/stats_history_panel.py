import tkinter as tk

class StatsHistoryPanel(tk.Frame):
    def __init__(self, master, profile_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.profile_manager = profile_manager
        self.text_var = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.text_var, justify="left", anchor="w", font=("Consolas", 10), bg="#23272A", fg="#fff", padx=6, pady=6)
        self.label.pack(fill="both", expand=True)
        # Place text ID entry and button below the stats
        bottom = tk.Frame(self, bg="#23272A")
        bottom.pack(fill="x", pady=(2, 2))
        self.text_id_var = tk.StringVar()
        self.text_id_entry = tk.Entry(bottom, textvariable=self.text_id_var, width=18)
        self.text_id_entry.pack(side="left", padx=2, pady=2)
        tk.Button(bottom, text="Show Text Stats", command=self.show_text_stats, font=("Segoe UI", 9)).pack(side="left", padx=2)
        self.update_stats()

    def update_stats(self):
        # Always reload the profile data from disk before updating stats
        if self.profile_manager.current_profile:
            try:
                self.profile_manager.load_profile(self.profile_manager.current_profile)
            except Exception:
                pass
        stats = self.profile_manager.get_stats()
        lines = [
            f"Races: {stats['num_races']}",
            f"Avg WPM: {stats['avg_wpm']}  (Correct: {stats['avg_correct_wpm']})",
            f"Avg Accuracy: {stats['avg_accuracy']}%",
            f"Last 10 WPM: {stats['last10_wpm']}  (Correct: {stats['last10_correct_wpm']})",
            f"Last 10 Accuracy: {stats['last10_accuracy']}%",
        ]
        self.text_var.set("\n".join(lines))

    def show_text_stats(self):
        text_id = self.text_id_var.get().strip()
        if not text_id:
            return
        stats = self.profile_manager.get_text_stats(text_id)
        if not stats:
            self.text_var.set(f"No stats for text: {text_id}")
            return
        lines = [
            f"Text: {text_id}",
            f"Races: {stats['num_races']}",
            f"Avg WPM: {stats['avg_wpm']}  (Correct: {stats['avg_correct_wpm']})",
            f"Avg Accuracy: {stats['avg_accuracy']}%",
            f"Last 10 WPM: {stats['last10_wpm']}  (Correct: {stats['last10_correct_wpm']})",
            f"Last 10 Accuracy: {stats['last10_accuracy']}%",
        ]
        self.text_var.set("\n".join(lines))
