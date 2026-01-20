from ..mini_markov_llm import MiniMarkovLLM

class LLMWrapper:
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct"):
        try:
            from vllm import LLM
            self.model = LLM(model=model_name)
            self.has_vllm = True
        except ImportError:
            # Utilise MiniMarkovLLM comme mock pédagogique
            corpus = "hello world this is a test hello AI world"
            self.model = MiniMarkovLLM(corpus)
            self.has_vllm = False

    def generate_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 100) -> str:
        if self.has_vllm and self.model:
            # vLLM API example (may need adjustment depending on vLLM version)
            outputs = self.model.generate(prompt, temperature=temperature, max_tokens=max_tokens)
            return outputs[0].text if outputs else ""
        else:
            # Utilise MiniMarkovLLM pour la génération complète
            return " ".join(self.model.generate(prompt, max_tokens=max_tokens))

    def stream_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 100):
        if self.has_vllm and self.model:
            # À adapter si vLLM supporte le streaming
            outputs = self.model.generate(prompt, temperature=temperature, max_tokens=max_tokens)
            if outputs:
                for word in outputs[0].text.split():
                    yield word + " "
        else:
            # Streaming mot par mot avec MiniMarkovLLM
            for word in self.model.generate(prompt, max_tokens=max_tokens):
                yield word + " "