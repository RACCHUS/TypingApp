import tkinter as tk

class TimerController:
    def __init__(self, root, timer_var, on_timer_end):
        self.root = root
        self.timer_var = timer_var
        self.on_timer_end = on_timer_end
        self.timer_running = False
        self.timer_seconds_left = 0
        self.timer_id = None

    def start(self, seconds):
        self.timer_seconds_left = seconds
        self.timer_running = True
        self._update_timer()

    def stop(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def _update_timer(self):
        if not self.timer_running:
            return
        if self.timer_seconds_left <= 0:
            self.timer_var.set("Time's up!")
            self.timer_running = False
            self.on_timer_end()
            return
        self.timer_var.set(self.format_time(self.timer_seconds_left))
        self.timer_seconds_left -= 1
        self.timer_id = self.root.after(1000, self._update_timer)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m}:{s:02d}"
