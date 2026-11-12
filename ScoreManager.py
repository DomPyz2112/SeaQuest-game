import os

class ScoreManager:
    def __init__(self, filename="highscore.txt"):
        self.filename = filename
        self.high_score = self._load_from_file()

    def _load_from_file(self):
        # --- Prywatna metoda wczytująca wynik przy starcie ---
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    return int(file.read().split(":")[1])
            except (ValueError, FileNotFoundError):
                return 0
        return 0

    def check_and_save(self, current_score):
        # --- Sprawdza czy wynik jest rekordem i zapisuje go ---
        if current_score > self.high_score:
            self.high_score = current_score
            with open(self.filename, "w") as file:
                file.write(str(f"Osiagnieto najwyzszy wyniki: {self.high_score}"))
            return True
        return False

    def get_high_score(self, current_score):
        # --- Wypisuje najlepszy wynik ---
        try:
            with open(self.filename, "r") as file:
                content = file.read()
                if ":" in content:
                    return int(content.split(":")[1])
                return int(content)
        except (ValueError, FileNotFoundError, IndexError):
            return 0
