# Responsive UI logic for modular use

def setup_responsive_ui(root, stats_panel, key_buttons, heading):
    def hide_heading_on_resize(event=None):
        min_height_for_heading = 520
        if root.winfo_height() < min_height_for_heading:
            heading.grid_remove()
        else:
            heading.grid()
    root.bind('<Configure>', hide_heading_on_resize)
    hide_heading_on_resize()

    def responsive_shrink(event=None):
        width = root.winfo_width()
        stats_font = max(10, int(14 * width / 1000))
        for label in [stats_panel.wpm_label, stats_panel.correct_wpm_label, stats_panel.accuracy_label, stats_panel.keystrokes_label]:
            label.config(font=("Segoe UI", stats_font, "bold"))
        for btn in key_buttons.values():
            btn_font = btn.cget("font")
            base_size = 14 if isinstance(btn_font, tuple) and len(btn_font) > 1 else 12
            new_size = max(8, int(base_size * width / 1000))
            btn.config(font=("Segoe UI", new_size, "bold"))
    root.bind('<Configure>', responsive_shrink)
    responsive_shrink()
