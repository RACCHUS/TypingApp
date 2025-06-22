# Key highlight logic for modular use

def highlight_key(key_buttons, keyboard_frame, key_id):
    if key_id in key_buttons:
        key_buttons[key_id].configure(bg="#00c853", fg="#ffffff")

def unhighlight_key(key_buttons, keyboard_frame, key_id):
    if key_id in key_buttons:
        color = keyboard_frame.key_colors.get(key_id, "#23272A")
        key_buttons[key_id].configure(bg=color, fg="#23272A" if color != "#23272A" else "#ffffff")
