import random
import time

class TypingSession:
    def __init__(self, sentences):
        self.sentences = sentences
        self.current_text = ""
        self.typed_text = ""
        self.start_time = None
        self.keystrokes = 0
        self.typing = False
        self.reset()

    def reset(self):
        s = random.choice(self.sentences)
        if isinstance(s, dict) and 'text' in s:
            self.current_text = s['text']
        else:
            self.current_text = s
        self.typed_text = ""
        self.start_time = None
        self.keystrokes = 0
        self.typing = False

    def add_char(self, char):
        self.typed_text += char
        self.keystrokes += 1
        if not self.typing:
            self.typing = True
            self.start_time = time.time()

    def backspace(self):
        self.typed_text = self.typed_text[:-1]
        self.keystrokes += 1

    def get_stats(self):
        # Method 1: Gross WPM (all keystrokes, including incorrect)
        correct_chars = sum(t == c for t, c in zip(self.typed_text, self.current_text))
        # Accuracy: correct chars / total keystrokes (including mistakes and corrections)
        accuracy = (correct_chars / self.keystrokes) * 100 if self.keystrokes else 100
        elapsed_time = time.time() - self.start_time if self.start_time else 1
        gross_wpm = (len(self.typed_text) / 5) / (elapsed_time / 60)
        return int(gross_wpm), int(accuracy)

    def get_correct_only_wpm(self):
        # Method 3: Only correct characters count toward WPM
        correct_chars = sum(t == c for t, c in zip(self.typed_text, self.current_text))
        elapsed_time = time.time() - self.start_time if self.start_time else 1
        correct_wpm = (correct_chars / 5) / (elapsed_time / 60)
        return int(correct_wpm)

    def is_complete(self):
        return len(self.typed_text) >= len(self.current_text)

    def is_correct(self):
        return self.typed_text == self.current_text
