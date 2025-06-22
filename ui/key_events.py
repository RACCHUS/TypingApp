import tkinter as tk

class KeyEventHandler:
    def __init__(self, app):
        self.app = app

    def on_key_press(self, event):
        if self.app.paused:
            return
        if self.app.session.is_complete() or (self.app.timer_running and self.app.timer_seconds_left <= 0):
            return
        key = event.keysym
        char = event.char
        if key in ("Shift_L", "Shift_R"):
            self.app.shift_pressed = True
            self.app.highlight_key("LSHIFT" if key == "Shift_L" else "RSHIFT")
            return
        if key in ("Control_L", "Control_R"):
            self.app.highlight_key("LCTRL" if key == "Control_L" else "RCTRL")
            return
        if key in ("Alt_L", "Alt_R"):
            self.app.highlight_key("LALT" if key == "Alt_L" else "RALT")
            return
        if key == "Caps_Lock":
            self.app.caps_lock_active = not self.app.caps_lock_active
            self.app.highlight_key("CAPS LOCK")
            return
        if key == "BackSpace":
            self.app.session.backspace()
            self.app.highlight_key("BACKSPACE")
            self.app.update_text_display()
            return
        if key == "Tab":
            self.app.highlight_key("TAB")
            return
        if key == "Return":
            char = "\n"
            self.app.highlight_key("ENTER")
        else:
            if char:
                self.app.highlight_key(char.upper() if char != " " else " ")
        if char:
            self.app.session.add_char(char)
        self.app.update_text_display()
        gross_wpm, accuracy = self.app.session.get_stats()
        correct_wpm = self.app.session.get_correct_only_wpm()
        self.app.update_stats(gross_wpm, correct_wpm, accuracy)
        if (self.app.session.is_complete() or (self.app.timer_running and self.app.timer_seconds_left <= 0)) and self.app.session.typed_text:
            last_char = self.app.session.typed_text[-1]
            self.app.unhighlight_key(last_char.upper() if last_char != " " else " ")
            if len(self.app.session.typed_text) > 1:
                prev_char = self.app.session.typed_text[-2]
                self.app.unhighlight_key(prev_char.upper() if prev_char != " " else " ")
            self.app.stats_panel.show_checkmark()
        else:
            self.app.stats_panel.hide_checkmark()

    def on_key_release(self, event):
        if self.app.paused:
            return
        if self.app.session.is_complete():
            return
        key = event.keysym
        # Always unhighlight both shift keys on any shift release
        if key in ("Shift_L", "Shift_R"):
            self.app.shift_pressed = False
            self.app.unhighlight_key("LSHIFT")
            self.app.unhighlight_key("RSHIFT")
        if key in ("Control_L", "Control_R"):
            self.app.unhighlight_key("LCTRL" if key == "Control_L" else "RCTRL")
        if key in ("Alt_L", "Alt_R"):
            self.app.unhighlight_key("LALT" if key == "Alt_L" else "RALT")
        if key == "Caps_Lock":
            self.app.unhighlight_key("CAPS LOCK")
        if key == "BackSpace":
            self.app.unhighlight_key("BACKSPACE")
        if key == "Tab":
            self.app.unhighlight_key("TAB")
        if key == "Return":
            self.app.unhighlight_key("ENTER")
        if event.char:
            self.app.unhighlight_key(event.char.upper() if event.char != " " else " ")
