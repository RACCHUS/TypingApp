import tkinter as tk

class TextDisplayFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.text_widget = TextDisplay(self, *args, **kwargs)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)
        self.text_widget.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

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
        # If current_text is a dict (with 'text' key), extract the text
        if isinstance(current_text, dict) and 'text' in current_text:
            current_text = current_text['text']
        self.configure(state="normal")
        self.delete("1.0", tk.END)

        next_char_index = None
        insert_index = self.index("1.0")

        for i, char in enumerate(current_text):
            if i < len(typed_text):
                tag = "correct" if typed_text[i] == char else "incorrect"
                self.insert(insert_index, char, tag)
                insert_index = self.index(f"{insert_index} + 1c")
            elif i == len(typed_text):
                self.insert(insert_index, char, "next_char")
                next_char_index = insert_index  # store where we just inserted
                insert_index = self.index(f"{insert_index} + 1c")
            else:
                self.insert(insert_index, char)
                insert_index = self.index(f"{insert_index} + 1c")

        self.tag_configure("correct", foreground="#00e676")
        self.tag_configure("incorrect", foreground="#ff5252")
        self.tag_configure("next_char", foreground="#23272A", background="#00e676")

        # Center the next char in the view if it's not visible
        if next_char_index and len(typed_text) > 0:
            try:
                bbox = self.bbox(next_char_index)
                if not bbox:
                    self.see(next_char_index)
                else:
                    line, _ = map(int, next_char_index.split("."))
                    total_lines = int(self.index('end-1c').split('.')[0])
                    visible_lines = int(self.winfo_height() // self.dlineinfo('1.0')[3])
                    first_visible = max(1, line - visible_lines // 2)
                    self.yview_moveto((first_visible - 1) / max(1, total_lines - visible_lines))
            except Exception:
                pass

        self.configure(state="disabled")
