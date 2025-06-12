import tkinter as tk
from pynput import keyboard
import random
import time

class TypeTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TypeTrack - Typing Tracker")
        self.shift_pressed = False
        self.caps_lock_active = False
        self.typing = False
        self.root.geometry("1000x600")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.keyboard_layout = [
            [('`', '~'), ('1', '!'), ('2', '@'), ('3', '#'), ('4', '$'), ('5', '%'),
             ('6', '^'), ('7', '&'), ('8', '*'), ('9', '('), ('0', ')'), ('-', '_'), ('=', '+'), 'backspace'],
            ['tab', ('q', 'Q'), ('w', 'W'), ('e', 'E'), ('r', 'R'), ('t', 'T'), ('y', 'Y'),
             ('u', 'U'), ('i', 'I'), ('o', 'O'), ('p', 'P'), ('[', '{'), (']', '}'), ('\\', '|')],
            ['capslock', ('a', 'A'), ('s', 'S'), ('d', 'D'), ('f', 'F'), ('g', 'G'), ('h', 'H'),
             ('j', 'J'), ('k', 'K'), ('l', 'L'), (';', ':'), ("'", '"'), 'enter'],
            ['shift', ('z', 'Z'), ('x', 'X'), ('c', 'C'), ('v', 'V'), ('b', 'B'), ('n', 'N'),
             ('m', 'M'), (',', '<'), ('.', '>'), ('/', '?'), 'shift'],
            ['space']
        ]

        self.sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Typing helps improve your focus and speed.",
            "Python is a versatile programming language.",
            "Always proofread your work before submission.",
            "The sky turned orange as the sun set.",
            "Practice makes perfect when learning new skills.",
            "Consistency is key to mastering typing.",
            "Keep your fingers on the home row keys.",
            "Accuracy matters more than speed at first.",
            "Every day is a new opportunity to improve.",
            "La la la lava chi chi chi chicken"
        ]

        self.current_text = ""
        self.typed_text = ""
        self.start_time = None
        self.keystrokes = 0

        self.create_widgets()
        self.reset_session()

        self.listener = keyboard.Listener(on_press=self.on_key_press_global, on_release=self.on_key_release)
        self.listener.start()

    def create_widgets(self):
        heading = tk.Label(
            self.root, text="Type the sentence below:",
            bg="#121212", fg="#ffffff",
            font=("Segoe UI", 16)
        )
        heading.pack(pady=10)

        self.text_display = tk.Text(
            self.root, height=4, width=100,
            bg="#1e1e1e", fg="white",
            font=("Consolas", 16),
            wrap="word", bd=2, relief="solid",
            highlightthickness=1, highlightbackground="#333"
        )
        self.text_display.pack(padx=20, pady=5)
        self.text_display.configure(state="disabled")

        stats_frame = tk.Frame(self.root, bg="#121212")
        stats_frame.pack(pady=10)

        self.wpm_label = tk.Label(stats_frame, text="WPM: 0", fg="#00e676", bg="#121212", font=("Segoe UI", 14, "bold"))
        self.wpm_label.pack(side="left", padx=30)

        self.accuracy_label = tk.Label(stats_frame, text="Accuracy: 100%", fg="#29b6f6", bg="#121212", font=("Segoe UI", 14, "bold"))
        self.accuracy_label.pack(side="left", padx=30)

        self.keystrokes_label = tk.Label(stats_frame, text="Keystrokes: 0", fg="#fdd835", bg="#121212", font=("Segoe UI", 14, "bold"))
        self.keystrokes_label.pack(side="left", padx=30)

        self.result_label = tk.Label(stats_frame, text="", fg="#ffffff", bg="#121212", font=("Segoe UI", 14, "italic"))
        self.result_label.pack(side="left", padx=30)

        self.keyboard_frame = tk.Frame(self.root, bg="#121212")
        self.keyboard_frame.pack(pady=15)

        self.key_buttons = {}
        layout = [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
            ["Space"]
        ]

        for row in layout:
            row_frame = tk.Frame(self.keyboard_frame, bg="#121212")
            row_frame.pack()
            for key in row:
                key_char = " " if key.lower() == "space" else key
                btn = tk.Label(
                    row_frame,
                    text=key_char if key_char != " " else "␣",
                    width=6 if key_char != " " else 30,
                    height=2,
                    fg="#ffffff",
                    bg="#2c2c2c",
                    font=("Segoe UI", 12),
                    relief="flat"
                )
                btn.pack(side="left", padx=3, pady=3)
                self.key_buttons[key_char.upper()] = btn

        reset_btn = tk.Button(
            self.root, text="New Sentence", command=self.reset_session,
            bg="#00acc1", fg="white", font=("Segoe UI", 12, "bold"),
            relief="flat", padx=12, pady=6, cursor="hand2"
        )
        reset_btn.pack(pady=10)

        self.update_key_labels()

    def reset_session(self):
        self.current_text = random.choice(self.sentences)
        self.typed_text = ""
        self.start_time = None
        self.keystrokes = 0
        self.result_label.configure(text="")
        self.update_text_display()
        self.update_stats(0, 100)
        self.typing = False

    def update_text_display(self):
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", tk.END)

        for i, char in enumerate(self.current_text):
            if i < len(self.typed_text):
                typed_char = self.typed_text[i]
                if typed_char == char:
                    self.text_display.insert(tk.END, char, ("correct",))
                else:
                    self.text_display.insert(tk.END, char, ("incorrect",))
            elif i == len(self.typed_text):
                self.text_display.insert(tk.END, char, ("next_char",))
            else:
                self.text_display.insert(tk.END, char)

        self.text_display.tag_configure("correct", foreground="#00e676")
        self.text_display.tag_configure("incorrect", foreground="#ff5252")
        self.text_display.tag_configure("next_char", foreground="white", background="#1976d2")
        self.text_display.configure(state="disabled")

    def on_key_press_global(self, key):
        # Track shift and caps lock states
        if key in [keyboard.Key.shift, keyboard.Key.shift_r]:
            self.shift_pressed = True
            self.update_key_labels()
            return
        elif key == keyboard.Key.caps_lock:
            self.caps_lock_active = not self.caps_lock_active
            self.update_key_labels()
            return

        if not self.typing:
            self.typing = True
            self.start_time = time.time()

        try:
            if hasattr(key, 'char') and key.char:
                self.typed_text += key.char
            elif key == keyboard.Key.space:
                self.typed_text += ' '
            elif key == keyboard.Key.backspace:
                self.typed_text = self.typed_text[:-1]
            elif key == keyboard.Key.enter:
                self.typed_text += '\n'
            else:
                return
        except AttributeError:
            return

        self.keystrokes += 1
        self.update_text_display()

        # Check if completed
        if len(self.typed_text) == len(self.current_text):
            if self.typed_text == self.current_text:
                elapsed_time = time.time() - self.start_time
                wpm = (len(self.typed_text) / 5) / (elapsed_time / 60)
                correct_chars = sum(1 for i in range(len(self.typed_text))
                                    if self.typed_text[i] == self.current_text[i])
                accuracy = (correct_chars / len(self.typed_text)) * 100
                self.result_label.configure(
                    text=f"✔ Finished! WPM: {int(wpm)}, Accuracy: {int(accuracy)}%")
            else:
                self.result_label.configure(text="❌ Check your typing.")

        correct_chars = sum(1 for i in range(len(self.typed_text))
                            if i < len(self.current_text) and self.typed_text[i] == self.current_text[i])
        accuracy = (correct_chars / len(self.typed_text)) * 100 if self.typed_text else 100
        elapsed_time = time.time() - self.start_time if self.start_time else 1
        wpm = (len(self.typed_text) / 5) / (elapsed_time / 60)
        self.update_stats(int(wpm), int(accuracy))

    def on_key_release(self, key):
        if key in [keyboard.Key.shift, keyboard.Key.shift_r]:
            self.shift_pressed = False
            self.update_key_labels()

    def update_key_labels(self):
        # For each key in layout, update label based on shift or caps lock state
        for row in self.keyboard_layout:
            for key in row:
                if isinstance(key, tuple):
                    base, shifted = key
                    key_id = base.upper()
                    if key_id in self.key_buttons:
                        if self.shift_pressed ^ self.caps_lock_active:
                            # Show shifted/uppercase symbol
                            self.key_buttons[key_id].configure(text=shifted)
                        else:
                            # Show base lowercase symbol
                            self.key_buttons[key_id].configure(text=base)
                elif isinstance(key, str):
                    key_id = key.upper()
                    if key_id in self.key_buttons:
                        # Show special keys in uppercase, else lowercase
                        if key in ["space", "enter", "shift", "tab", "capslock", "backspace"]:
                            label = key.upper()
                        else:
                            # Show lowercase letter if letter key
                            label = key.lower()
                        self.key_buttons[key_id].configure(text=label)

    def update_stats(self, wpm, accuracy):
        self.wpm_label.configure(text=f"WPM: {wpm}")
        self.accuracy_label.configure(text=f"Accuracy: {accuracy}%")
        self.keystrokes_label.configure(text=f"Keystrokes: {self.keystrokes}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypeTrackApp(root)
    root.mainloop()