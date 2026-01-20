import random
from collections import defaultdict

class MiniMarkovLLM:
    """
    Mini modèle Markov pour génération de texte token par token.
    Usage pédagogique uniquement.
    """
    def __init__(self, corpus: str):
        self.transitions = defaultdict(list)
        self.build_model(corpus)

    def build_model(self, corpus: str):
        words = corpus.split()
        for i in range(len(words) - 1):
            self.transitions[words[i]].append(words[i + 1])
        self.transitions[words[-1]].append("")  # fin de séquence

    def generate(self, prompt: str, max_tokens: int = 50):
        """Générateur de mots pour le streaming"""
        words = prompt.split()
        current = words[-1] if words else random.choice(list(self.transitions.keys()))
        for _ in range(max_tokens):
            next_words = self.transitions.get(current, [""])
            if not next_words or next_words == [""]:
                break
            next_word = random.choice(next_words)
            yield next_word
            current = next_word