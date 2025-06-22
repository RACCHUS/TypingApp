# Session control logic for modular use

def reset_session(session):
    session.reset()
    session.typed_text = ""
    session.start_time = None
    session.keystrokes = 0
    session.typing = False

def pause_session(app):
    app.paused = True

def resume_session(app):
    app.paused = False
