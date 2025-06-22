import tkinter as tk
from logic.keymap import FINGER_COLORS, FINGER_MAP

class VirtualKeyboard(tk.Frame):
    def __init__(self, master, key_buttons, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(bg="#181A1B")
        self.key_buttons = key_buttons
        self.key_colors = {}
        self._build_keyboard()

    def _build_keyboard(self):
        layout = [
            # Row 0
            [("`", 0, 2), ("1", 2, 2), ("2", 4, 2), ("3", 6, 2), ("4", 8, 2), ("5", 10, 2), ("6", 12, 2), ("7", 14, 2), ("8", 16, 2), ("9", 18, 2), ("0", 20, 2), ("-", 22, 2), ("=", 24, 2), ("Backspace", 26, 6)],
            # Row 1
            [("Tab", 0, 4), ("Q", 4, 2), ("W", 6, 2), ("E", 8, 2), ("R", 10, 2), ("T", 12, 2), ("Y", 14, 2), ("U", 16, 2), ("I", 18, 2), ("O", 20, 2), ("P", 22, 2), ("[", 24, 2), ("]", 26, 2), ("\\", 28, 4)],
            # Row 2
            [("Caps Lock", 0, 5), ("A", 5, 2), ("S", 7, 2), ("D", 9, 2), ("F", 11, 2), ("G", 13, 2), ("H", 15, 2), ("J", 17, 2), ("K", 19, 2), ("L", 21, 2), (";", 23, 2), ("'", 25, 2), ("Enter", 27, 5)],
            # Row 3
            [("LSHIFT", 0, 6), ("Z", 6, 2), ("X", 8, 2), ("C", 10, 2), ("V", 12, 2), ("B", 14, 2), ("N", 16, 2), ("M", 18, 2), (",", 20, 2), (".", 22, 2), ("/", 24, 2), ("RSHIFT", 26, 6)],
            # Row 4
            [("LCTRL", 0, 4), ("LALT", 4, 4), ("Space", 8, 16), ("RALT", 24, 4), ("RCTRL", 28, 4)]
        ]
        KEY_HEIGHT = 48
        for row_idx, row in enumerate(layout):
            for key, col, colspan in row:
                # Display text for left/right modifiers
                if key == "LSHIFT":
                    display_text = "Shift"
                elif key == "RSHIFT":
                    display_text = "Shift"
                elif key == "LALT":
                    display_text = "Alt"
                elif key == "RALT":
                    display_text = "Alt"
                elif key == "LCTRL":
                    display_text = "Ctrl"
                elif key == "RCTRL":
                    display_text = "Ctrl"
                elif key.lower() == "space":
                    display_text = "␣"
                else:
                    display_text = key
                key_id = " " if key.lower() == "space" else key.upper()
                font_size = 10 if len(display_text) > 1 else 14
                key_upper = key.upper()
                # Assign color for modifiers
                if key_upper in ("LSHIFT", "LCTRL", "LALT"):
                    assigned_color = FINGER_COLORS["LEFT_PINKY"]
                elif key_upper in ("RSHIFT", "RCTRL", "RALT"):
                    assigned_color = FINGER_COLORS["RIGHT_PINKY"]
                else:
                    assigned_color = "#23272A"
                    for finger, keys in FINGER_MAP.items():
                        if key_upper in [k.upper() for k in keys]:
                            assigned_color = FINGER_COLORS[finger]
                            break
                btn = tk.Label(
                    self, text=display_text,
                    fg="#23272A" if assigned_color != "#23272A" else "#ffffff",
                    bg=assigned_color, font=("Segoe UI", font_size, "bold"),
                    relief="flat", bd=0, highlightthickness=0, cursor="hand2",
                    width=colspan*2, height=2
                )
                btn.grid(row=row_idx, column=col, columnspan=colspan, padx=2, pady=3, sticky="nsew")
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#00c853"))
                btn.bind("<Leave>", lambda e, b=btn, c=assigned_color: b.configure(bg=c))
                self.key_buttons[key_id] = btn
                self.key_colors[key_id] = assigned_color
        for i in range(32):
            self.grid_columnconfigure(i, weight=1)

    def highlight_key(self, key_id):
        if key_id in self.key_buttons:
            self.key_buttons[key_id].configure(bg="#00c853", fg="#ffffff")

    def unhighlight_key(self, key_id):
        if key_id in self.key_buttons:
            color = self.key_colors.get(key_id, "#23272A")
            self.key_buttons[key_id].configure(bg=color, fg="#23272A" if color != "#23272A" else "#ffffff")
