import os
import json
from datetime import datetime

PROFILE_DIR = os.path.join(os.path.dirname(__file__), '..', 'profiles')

class ProfileManager:
    def __init__(self):
        os.makedirs(PROFILE_DIR, exist_ok=True)
        self.current_profile = None
        self.profile_data = None

    def list_profiles(self):
        return [f[:-5] for f in os.listdir(PROFILE_DIR) if f.endswith('.json')]

    def load_profile(self, name):
        path = os.path.join(PROFILE_DIR, f'{name}.json')
        if not os.path.exists(path):
            raise FileNotFoundError(f'Profile {name} does not exist.')
        with open(path, 'r', encoding='utf-8') as f:
            self.profile_data = json.load(f)
        self.current_profile = name

    def save_profile(self):
        if not self.current_profile or not self.profile_data:
            return
        path = os.path.join(PROFILE_DIR, f'{self.current_profile}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.profile_data, f, indent=2)

    def create_profile(self, name):
        if name in self.list_profiles():
            raise ValueError('Profile already exists.')
        self.profile_data = {
            'name': name,
            'history': [],  # list of dicts: {timestamp, text_id, wpm, correct_wpm, accuracy}
            'per_text': {}, # text_id: {history: [...], stats: {...}}
        }
        self.current_profile = name
        self.save_profile()

    def delete_profile(self, name):
        path = os.path.join(PROFILE_DIR, f'{name}.json')
        if os.path.exists(path):
            os.remove(path)
        if self.current_profile == name:
            self.current_profile = None
            self.profile_data = None

    def reset_profile(self, name):
        self.profile_data = {
            'name': name,
            'history': [],
            'per_text': {},
        }
        self.current_profile = name
        self.save_profile()

    def record_race(self, text_id, wpm, correct_wpm, accuracy):
        if not self.profile_data:
            return
        entry = {
            'timestamp': datetime.now().isoformat(),
            'text_id': text_id,
            'wpm': wpm,
            'correct_wpm': correct_wpm,
            'accuracy': accuracy
        }
        self.profile_data['history'].append(entry)
        # Per-text history
        if text_id not in self.profile_data['per_text']:
            self.profile_data['per_text'][text_id] = {'history': []}
        self.profile_data['per_text'][text_id]['history'].append(entry)
        self.save_profile()

    def get_stats(self):
        # Returns overall stats and last 10
        h = self.profile_data['history']
        n = len(h)
        last10 = h[-10:]
        def avg(key, data):
            return round(sum(e[key] for e in data)/len(data), 2) if data else 0
        return {
            'num_races': n,
            'avg_wpm': avg('wpm', h),
            'avg_correct_wpm': avg('correct_wpm', h),
            'avg_accuracy': avg('accuracy', h),
            'last10_wpm': avg('wpm', last10),
            'last10_correct_wpm': avg('correct_wpm', last10),
            'last10_accuracy': avg('accuracy', last10),
        }

    def get_text_stats(self, text_id):
        # Returns stats for a specific text
        if text_id not in self.profile_data['per_text']:
            return None
        h = self.profile_data['per_text'][text_id]['history']
        n = len(h)
        last10 = h[-10:]
        def avg(key, data):
            return round(sum(e[key] for e in data)/len(data), 2) if data else 0
        return {
            'num_races': n,
            'avg_wpm': avg('wpm', h),
            'avg_correct_wpm': avg('correct_wpm', h),
            'avg_accuracy': avg('accuracy', h),
            'last10_wpm': avg('wpm', last10),
            'last10_correct_wpm': avg('correct_wpm', last10),
            'last10_accuracy': avg('accuracy', last10),
        }
