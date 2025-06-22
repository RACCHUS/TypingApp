import tkinter as tk

class Dropdowns:
    def __init__(self, parent, letter_var, test_time_var, on_letter_select, on_test_time_select, timer_var, timer_label):
        self.frame = tk.Frame(parent, bg="#181A1B")
        self.frame.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        # Letter selection dropdown
        tk.Label(self.frame, text="Practice key:", bg="#181A1B", fg="#ffffff", font=("Segoe UI", 12)).pack(side="left", padx=(0, 8))
        letter_options = ["All"] + [chr(i) for i in range(ord('A'), ord('Z')+1)]
        dropdown = tk.OptionMenu(self.frame, letter_var, *letter_options, command=on_letter_select)
        dropdown.config(font=("Segoe UI", 12), bg="#23272A", fg="#ffffff", highlightthickness=0)
        dropdown.pack(side="left")
        # Test time dropdown
        tk.Label(self.frame, text="  Test length:", bg="#181A1B", fg="#ffffff", font=("Segoe UI", 12)).pack(side="left", padx=(16, 8))
        test_time_options = ["None", "1 min", "2 min", "3 min", "4 min", "5 min"]
        time_dropdown = tk.OptionMenu(self.frame, test_time_var, *test_time_options, command=on_test_time_select)
        time_dropdown.config(font=("Segoe UI", 12), bg="#23272A", fg="#ffffff", highlightthickness=0)
        time_dropdown.pack(side="left")
        # Timer label
        timer_label_widget = tk.Label(self.frame, textvariable=timer_var, bg="#181A1B", fg="#ffb300", font=("Segoe UI", 14, "bold"))
        timer_label_widget.pack(side="left", padx=(16, 0))
        timer_label[0] = timer_label_widget

    def get_frame(self):
        return self.frame
