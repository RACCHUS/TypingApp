import tkinter as tk

class TextDisplay(tk.Text):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.base_font_size = 16
        self.min_font_size = 9
        self.configure(height=4, width=100, bg="#23272A", fg="white",
                       font=("Consolas", self.base_font_size), wrap="word", bd=0, relief="flat",
                       highlightthickness=2, highlightbackground="#333", padx=10, pady=10,
                       state="disabled")
        self.master.bind('<Configure>', self._responsive_font)

    def _responsive_font(self, event=None):
        width = self.master.winfo_width()
        # Shrink font size as width shrinks, but not below min_font_size
        new_size = max(self.min_font_size, int(self.base_font_size * width / 1000))
        self.configure(font=("Consolas", new_size))

    def update_text(self, current_text, typed_text):
        self.configure(state="normal")
        self.delete("1.0", tk.END)
        for i, char in enumerate(current_text):
            if i < len(typed_text):
                tag = "correct" if typed_text[i] == char else "incorrect"
                self.insert(tk.END, char, tag)
            elif i == len(typed_text):
                self.insert(tk.END, char, "next_char")
            else:
                self.insert(tk.END, char)
        self.tag_configure("correct", foreground="#00e676")
        self.tag_configure("incorrect", foreground="#ff5252")
        self.tag_configure("next_char", foreground="#23272A", background="#00e676")
        self.configure(state="disabled")
