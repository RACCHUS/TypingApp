import tkinter as tk
import random
import time
from pynput import keyboard
from ui.keyboard import VirtualKeyboard
from ui.stats import StatsPanel
from ui.text_display import TextDisplay
from logic.session import TypingSession
from data.practice_texts import LETTER_PRACTICE_SENTENCES, PRACTICE_SENTENCES, FIVE_MINUTE_TEXT

class TypeTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TypeTrack - Typing Tracker")
        self.root.geometry("1000x650")
        self.root.configure(bg="#181A1B")
        self.root.resizable(True, True)  # Allow resizing
        self.root.minsize(800, 400)  # Set minimum window size

        self.shift_pressed = False
        self.caps_lock_active = False
        self.paused = False

        self.session = TypingSession([
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
        ])

        self.key_buttons = {}
        self.wpm_var = tk.StringVar(value="WPM Gross: 0")
        self.correct_wpm_var = tk.StringVar(value="WPM Correct: 0")
        self.accuracy_var = tk.StringVar(value="Accuracy: 100%")
        self.keystrokes_var = tk.StringVar(value="Keystrokes: 0")
        self.result_var = tk.StringVar(value="")

        self.create_widgets()
        self.reset_session()

        self.listener = keyboard.Listener(on_press=self.on_key_press_global, on_release=self.on_key_release)
        self.listener.start()

        self.root.bind('<FocusIn>', self.on_focus_in)
        self.root.bind('<FocusOut>', self.on_focus_out)

    def create_widgets(self):
        # Main content frame (everything except the button)
        content_frame = tk.Frame(self.root, bg="#181A1B")
        content_frame.pack(side="top", fill="both", expand=True)
        content_frame.grid_rowconfigure(2, weight=1)  # Only text display expands vertically
        content_frame.grid_rowconfigure(0, weight=0)  # title/stats
        content_frame.grid_rowconfigure(1, weight=0)  # heading
        content_frame.grid_rowconfigure(2, weight=1)  # text display (main priority)
        content_frame.grid_rowconfigure(3, weight=0)  # (no longer used for stats)
        content_frame.grid_rowconfigure(4, weight=0)  # keyboard
        content_frame.grid_columnconfigure(0, weight=1)

        # Title bar (remove icon and title)
        title_frame = tk.Frame(content_frame, bg="#23272A", height=50)
        title_frame.grid(row=0, column=0, sticky="ew")
        # self.icon = tk.Label(title_frame, text="\u2328", font=("Segoe UI Emoji", 24), bg="#23272A", fg="#00e676")
        # self.icon.pack(side="left", padx=(20, 10), pady=5)
        # self.title = tk.Label(title_frame, text="TypeTrack", font=("Segoe UI", 20, "bold"), bg="#23272A", fg="#ffffff")
        # self.title.pack(side="left", pady=5)
        self.stats_panel = StatsPanel(title_frame, self.wpm_var, self.correct_wpm_var, self.accuracy_var, self.keystrokes_var)
        self.stats_panel.pack(side="left", padx=20)
        button_frame = tk.Frame(title_frame, bg="#23272A")
        button_frame.pack(side="right", padx=18, pady=8)
        reset_btn = tk.Button(
            button_frame, text="New", command=self.reset_session,
            bg="#00acc1", fg="white", font=("Segoe UI", 11, "bold"),
            relief="flat", padx=12, pady=4, cursor="hand2", bd=0, highlightthickness=0
        )
        reset_btn.pack()

        # Add dropdown for letter selection
        dropdown_frame = tk.Frame(content_frame, bg="#181A1B")
        dropdown_frame.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        tk.Label(dropdown_frame, text="Practice key:", bg="#181A1B", fg="#ffffff", font=("Segoe UI", 12)).pack(side="left", padx=(0, 8))
        self.letter_var = tk.StringVar(value="All")
        letter_options = ["All"] + [chr(i) for i in range(ord('A'), ord('Z')+1)]
        dropdown = tk.OptionMenu(dropdown_frame, self.letter_var, *letter_options, command=self.on_letter_select)
        dropdown.config(font=("Segoe UI", 12), bg="#23272A", fg="#ffffff", highlightthickness=0)
        dropdown.pack(side="left")
        # Add dropdown for timed tests
        tk.Label(dropdown_frame, text="  Test length:", bg="#181A1B", fg="#ffffff", font=("Segoe UI", 12)).pack(side="left", padx=(16, 8))
        self.test_time_var = tk.StringVar(value="None")
        test_time_options = ["None", "1 min", "2 min", "3 min", "4 min", "5 min"]
        time_dropdown = tk.OptionMenu(dropdown_frame, self.test_time_var, *test_time_options, command=self.on_test_time_select)
        time_dropdown.config(font=("Segoe UI", 12), bg="#23272A", fg="#ffffff", highlightthickness=0)
        time_dropdown.pack(side="left")
        # Timer label
        self.timer_var = tk.StringVar(value="")
        self.timer_label = tk.Label(dropdown_frame, textvariable=self.timer_var, bg="#181A1B", fg="#ffb300", font=("Segoe UI", 14, "bold"))
        self.timer_label.pack(side="left", padx=(16, 0))
        self.timer_running = False
        self.timer_seconds_left = 0
        self.timer_id = None

        heading = tk.Label(
            content_frame, text="Type the sentence below:",
            bg="#181A1B", fg="#ffffff", font=("Segoe UI", 16, "bold")
        )
        heading.grid(row=2, column=0, pady=(18, 8), sticky="ew")
        self.heading = heading  # Save reference for dynamic show/hide

        self.text_display = TextDisplay(content_frame)
        self.text_display.grid(row=3, column=0, padx=30, pady=5, sticky="nsew")

        # Remove old stats_panel location
        # self.stats_panel = StatsPanel(content_frame, self.wpm_var, self.accuracy_var, self.keystrokes_var, self.result_var)
        # self.stats_panel.grid(row=3, column=0, pady=10, sticky="ew")

        # Keyboard container: fixed width, centered, never stretches
        keyboard_container = tk.Frame(content_frame, bg="#181A1B", highlightbackground="#23272A", highlightthickness=2, width=600)
        keyboard_container.grid(row=4, column=0, pady=18)
        self.keyboard_frame = VirtualKeyboard(keyboard_container, self.key_buttons)
        self.keyboard_frame.pack(fill="both", expand=True, padx=30)
        # Center the keyboard container using grid column weights
        content_frame.grid_columnconfigure(0, weight=1)
        keyboard_container.grid_columnconfigure(0, weight=1)
        keyboard_container.grid_propagate(False)

        # Responsive: hide heading if window is too short
        def hide_heading_on_resize(event=None):
            min_height_for_heading = 520
            if self.root.winfo_height() < min_height_for_heading:
                self.heading.grid_remove()
            else:
                self.heading.grid()
        self.root.bind('<Configure>', hide_heading_on_resize)
        hide_heading_on_resize()

        # Responsive: shrink stats and keyboard font for small windows
        def responsive_shrink(event=None):
            width = self.root.winfo_width()
            # Shrink stats font
            stats_font = max(10, int(14 * width / 1000))
            for label in [self.stats_panel.wpm_label, self.stats_panel.correct_wpm_label, self.stats_panel.accuracy_label, self.stats_panel.keystrokes_label]:
                label.config(font=("Segoe UI", stats_font, "bold"))
            # Shrink keyboard font
            for btn in self.key_buttons.values():
                btn_font = btn.cget("font")
                base_size = 14 if isinstance(btn_font, tuple) and len(btn_font) > 1 else 12
                new_size = max(8, int(base_size * width / 1000))
                btn.config(font=("Segoe UI", new_size, "bold"))
        self.root.bind('<Configure>', responsive_shrink)
        responsive_shrink()

    def on_test_time_select(self, value):
        # Set up the test for the selected time
        if value == "None":
            self.timer_var.set("")
            self.timer_running = False
            self.timer_seconds_left = 0
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.on_letter_select(self.letter_var.get())
            return
        minutes = int(value.split()[0])
        self.timer_seconds_left = minutes * 60
        self.timer_var.set(self.format_time(self.timer_seconds_left))
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        # Use the long text for 5 min, otherwise repeat general sentences
        if minutes == 5:
            self.session.current_text = FIVE_MINUTE_TEXT
        else:
            # Repeat general sentences to fill the time
            text = " ".join(PRACTICE_SENTENCES * 10)
            self.session.current_text = text[:max(300, minutes*300)]
        self.session.typed_text = ""
        self.session.start_time = None
        self.session.keystrokes = 0
        self.session.typing = False
        self.result_var.set("")
        self.text_display.update_text(self.session.current_text, self.session.typed_text)
        self.update_stats(0, 0, 100)
        self.stats_panel.hide_checkmark()
        self.start_timer()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        if self.timer_seconds_left <= 0:
            self.timer_var.set("Time's up!")
            self.timer_running = False
            self.on_timer_end()
            return
        # Only update the timer label here
        self.timer_var.set(self.format_time(self.timer_seconds_left))
        self.timer_seconds_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def on_timer_end(self):
        # Called once when timer expires
        self.stats_panel.show_checkmark()
        self.update_stats(self.session.get_wpm(), self.session.get_correct_wpm(), self.session.get_accuracy())
        self.text_display.update_text(self.session.current_text, self.session.typed_text)
        # Optionally, unhighlight all keys
        for key in self.key_buttons:
            self.unhighlight_key(key)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m}:{s:02d}"

    def reset_session(self):
        self.session.reset()
        self.result_var.set("")
        self.text_display.update_text(self.session.current_text, self.session.typed_text)
        self.update_stats(0, 0, 100)
        self.stats_panel.hide_checkmark()
        self.timer_var.set("")
        self.timer_running = False
        self.timer_seconds_left = 0
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

    def update_text_display(self):
        self.text_display.update_text(self.session.current_text, self.session.typed_text)

    def on_focus_in(self, event):
        self.paused = False

    def on_focus_out(self, event):
        self.paused = True

    def on_key_press_global(self, key):
        if self.paused:
            return
        if self.session.is_complete() or (self.timer_running and self.timer_seconds_left <= 0):
            return
        # Handle modifier keys
        if key in (keyboard.Key.shift, keyboard.Key.shift_l):
            self.shift_pressed = True
            self.highlight_key("LSHIFT")
            return
        if key == keyboard.Key.shift_r:
            self.shift_pressed = True
            self.highlight_key("RSHIFT")
            return
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l):
            self.highlight_key("LCTRL")
            return
        if key == keyboard.Key.ctrl_r:
            self.highlight_key("RCTRL")
            return
        if key in (keyboard.Key.alt_l,):
            self.highlight_key("LALT")
            return
        if key in (keyboard.Key.alt_r, keyboard.Key.alt_gr):
            self.highlight_key("RALT")
            return
        if key == keyboard.Key.caps_lock:
            self.caps_lock_active = not self.caps_lock_active
            self.highlight_key("CAPS LOCK")
            return
        try:
            char = None
            if hasattr(key, "char") and key.char:
                char = key.char
            elif key == keyboard.Key.space:
                char = " "
            elif key == keyboard.Key.enter:
                char = "\n"
            elif key == keyboard.Key.backspace:
                self.session.backspace()
                self.highlight_key("BACKSPACE")
                self.update_text_display()
                return
            else:
                special_keys = {
                    keyboard.Key.tab: "TAB",
                }
                if key in special_keys:
                    self.highlight_key(special_keys[key])
                return
            if char is not None:
                self.session.add_char(char)
                self.highlight_key(char.upper() if char != " " else " ")
        except AttributeError:
            return
        self.update_text_display()
        gross_wpm, accuracy = self.session.get_stats()
        correct_wpm = self.session.get_correct_only_wpm()
        self.update_stats(gross_wpm, correct_wpm, accuracy)
        # Unhighlight last and previous key if session is complete or timer expired
        if (self.session.is_complete() or (self.timer_running and self.timer_seconds_left <= 0)) and self.session.typed_text:
            last_char = self.session.typed_text[-1]
            self.unhighlight_key(last_char.upper() if last_char != " " else " ")
            if len(self.session.typed_text) > 1:
                prev_char = self.session.typed_text[-2]
                self.unhighlight_key(prev_char.upper() if prev_char != " " else " ")
            self.stats_panel.show_checkmark()
        else:
            self.stats_panel.hide_checkmark()

    def on_key_release(self, key):
        if self.paused:
            return
        # Prevent further stats update if session is complete
        if self.session.is_complete():
            return
        # Handle modifier keys
        if key in (keyboard.Key.shift, keyboard.Key.shift_l):
            self.shift_pressed = False
            self.unhighlight_key("LSHIFT")
        if key == keyboard.Key.shift_r:
            self.shift_pressed = False
            self.unhighlight_key("RSHIFT")
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l):
            self.unhighlight_key("LCTRL")
        if key == keyboard.Key.ctrl_r:
            self.unhighlight_key("RCTRL")
        if key in (keyboard.Key.alt_l,):
            self.unhighlight_key("LALT")
        if key in (keyboard.Key.alt_r, keyboard.Key.alt_gr):
            self.unhighlight_key("RALT")
        try:
            char = None
            if hasattr(key, "char") and key.char:
                char = key.char.upper()
            elif key == keyboard.Key.space:
                char = " "
            else:
                special_keys = {
                    keyboard.Key.enter: "ENTER",
                    keyboard.Key.backspace: "BACKSPACE",
                    keyboard.Key.tab: "TAB",
                    keyboard.Key.caps_lock: "CAPS LOCK",
                }
                char = special_keys.get(key, None)
            if char:
                self.unhighlight_key(char)
        except AttributeError:
            pass

    def highlight_key(self, key_id):
        if key_id in self.key_buttons:
            self.key_buttons[key_id].configure(bg="#00c853", fg="#ffffff")

    def unhighlight_key(self, key_id):
        if key_id in self.key_buttons:
            color = self.keyboard_frame.key_colors.get(key_id, "#23272A")
            self.key_buttons[key_id].configure(bg=color, fg="#23272A" if color != "#23272A" else "#ffffff")

    def update_stats(self, wpm, correct_wpm, accuracy):
        self.wpm_var.set(f"WPM Gross: {wpm}")
        self.correct_wpm_var.set(f"WPM Correct: {correct_wpm}")
        self.accuracy_var.set(f"Accuracy: {accuracy}%")
        self.keystrokes_var.set(f"Keystrokes: {self.session.keystrokes}")

    def on_letter_select(self, value):
        if value == "All":
            self.session.current_text = random.choice(PRACTICE_SENTENCES)
        else:
            self.session.current_text = LETTER_PRACTICE_SENTENCES.get(value, "")
        self.session.typed_text = ""
        self.session.start_time = None
        self.session.keystrokes = 0
        self.session.typing = False
        self.result_var.set("")
        self.text_display.update_text(self.session.current_text, self.session.typed_text)
        self.update_stats(0, 0, 100)
        self.stats_panel.hide_checkmark()
