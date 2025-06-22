import tkinter as tk
import random
from ui.stats import StatsPanel
from ui.text_display import TextDisplay
from ui.dropdowns import Dropdowns
from ui.timer import TimerController
from ui.key_events import KeyEventHandler
from ui.keyboard_container import KeyboardContainer
from logic.session import TypingSession
from data.practice_texts import LETTER_PRACTICE_SENTENCES, PRACTICE_SENTENCES, FIVE_MINUTE_TEXT
from ui.key_highlight import highlight_key, unhighlight_key
from ui.responsive import setup_responsive_ui
from ui.titlebar import create_titlebar
from logic.session_control import reset_session, pause_session, resume_session
from logic.stats_update import update_stats

class TypeTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TypeTrack - Typing Tracker")
        self.root.geometry("1000x650")
        self.root.configure(bg="#181A1B")
        self.root.resizable(True, True)
        self.root.minsize(800, 400)

        self.shift_pressed = False
        self.caps_lock_active = False
        self.paused = False

        self.session = TypingSession(PRACTICE_SENTENCES)
        self.key_buttons = {}
        self.wpm_var = tk.StringVar(value="WPM Gross: 0")
        self.correct_wpm_var = tk.StringVar(value="WPM Correct: 0")
        self.accuracy_var = tk.StringVar(value="Accuracy: 100%")
        self.keystrokes_var = tk.StringVar(value="Keystrokes: 0")
        self.result_var = tk.StringVar(value="")

        self.create_widgets()
        self.reset_session()

        self.key_event_handler = KeyEventHandler(self)
        self.root.bind('<KeyPress>', self.key_event_handler.on_key_press)
        self.root.bind('<KeyRelease>', self.key_event_handler.on_key_release)
        self.root.bind('<FocusIn>', self.on_focus_in)
        self.root.bind('<FocusOut>', self.on_focus_out)

    def create_widgets(self):
        content_frame = tk.Frame(self.root, bg="#181A1B")
        content_frame.pack(side="top", fill="both", expand=True)
        content_frame.grid_rowconfigure(2, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Title bar
        title_frame, self.stats_panel = create_titlebar(
            content_frame, self.wpm_var, self.correct_wpm_var, self.accuracy_var, self.keystrokes_var, self.reset_session
        )
        title_frame.grid(row=0, column=0, sticky="ew")

        # Dropdowns and timer label
        self.letter_var = tk.StringVar(value="All")
        self.test_time_var = tk.StringVar(value="None")
        self.timer_var = tk.StringVar(value="")
        self.timer_label = [None]
        self.dropdowns = Dropdowns(
            content_frame, self.letter_var, self.test_time_var,
            self.on_letter_select, self.on_test_time_select,
            self.timer_var, self.timer_label
        )

        heading = tk.Label(
            content_frame, text="Type the sentence below:",
            bg="#181A1B", fg="#ffffff", font=("Segoe UI", 16, "bold")
        )
        heading.grid(row=2, column=0, pady=(18, 8), sticky="ew")
        self.heading = heading

        self.text_display = TextDisplay(content_frame)
        self.text_display.grid(row=3, column=0, padx=30, pady=5, sticky="nsew")

        self.keyboard_container = KeyboardContainer(content_frame, self.key_buttons)
        self.keyboard_container.grid(row=4, column=0, pady=18)

        # Timer controller
        self.timer_controller = TimerController(self.root, self.timer_var, self.on_timer_end)
        self.timer_running = False
        self.timer_seconds_left = 0
        self.timer_id = None

        # Responsive UI logic (unchanged)
        def hide_heading_on_resize(event=None):
            min_height_for_heading = 520
            if self.root.winfo_height() < min_height_for_heading:
                self.heading.grid_remove()
            else:
                self.heading.grid()
        self.root.bind('<Configure>', hide_heading_on_resize)
        hide_heading_on_resize()

        def responsive_shrink(event=None):
            width = self.root.winfo_width()
            stats_font = max(10, int(14 * width / 1000))
            for label in [self.stats_panel.wpm_label, self.stats_panel.correct_wpm_label, self.stats_panel.accuracy_label, self.stats_panel.keystrokes_label]:
                label.config(font=("Segoe UI", stats_font, "bold"))
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
        # Use the long text for all timed tests
        self.session.current_text = FIVE_MINUTE_TEXT
        self.session.typed_text = ""
        self.session.start_time = None
        self.session.keystrokes = 0
        self.session.typing = False
        self.result_var.set("")
        self.text_display.update_text(self.session.current_text, self.session.typed_text)
        self.update_stats(0, 0, 100)
        self.stats_panel.hide_checkmark()
        self.start_timer()

    def on_timer_end(self):
        # Only update stats and text display ONCE when the timer ends
        self.stats_panel.show_checkmark()
        self.update_stats(self.session.get_wpm(), self.session.get_correct_wpm(), self.session.get_accuracy())
        self.text_display.update_text(self.session.current_text, self.session.typed_text)
        for key in self.key_buttons:
            self.unhighlight_key(key)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m}:{s:02d}"

    def reset_session(self):
        reset_session(self.session)
        self.result_var.set("")
        self.text_display.update_text(self.session.current_text, self.session.typed_text)
        update_stats(self, 0, 0, 100)
        self.stats_panel.hide_checkmark()
        self.timer_var.set("")
        self.timer_running = False
        self.timer_seconds_left = 0
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

    def update_text_display(self):
        self.text_display.update_text(self.session.current_text, self.session.typed_text)

    def on_focus_in(self, event):
        resume_session(self)

    def on_focus_out(self, event):
        pause_session(self)

    def update_stats(self, wpm, correct_wpm, accuracy):
        update_stats(self, wpm, correct_wpm, accuracy)

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

    def highlight_key(self, key_id):
        highlight_key(self.key_buttons, self.keyboard_container.keyboard_frame, key_id)

    def unhighlight_key(self, key_id):
        unhighlight_key(self.key_buttons, self.keyboard_container.keyboard_frame, key_id)

    # Timer delegation
    def start_timer(self):
        self.timer_running = True
        self.timer_controller.start(self.timer_seconds_left)

    def stop_timer(self):
        self.timer_running = False
        self.timer_controller.stop()
