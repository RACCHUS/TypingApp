# Stats update logic for modular use

def update_stats(app, wpm, correct_wpm, accuracy):
    app.wpm_var.set(f"WPM Gross: {wpm}")
    app.correct_wpm_var.set(f"WPM Correct: {correct_wpm}")
    app.accuracy_var.set(f"Accuracy: {accuracy}%")
    app.keystrokes_var.set(f"Keystrokes: {app.session.keystrokes}")
