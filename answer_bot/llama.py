from llama_cpp import Llama

MODEL = "./weights/codellama-7b.Q4_0.gguf"
SEED = 13
CONTEXT_LENGTH = 512

LLM = Llama(
    model_path=MODEL,
    n_gpu_layers=1,
    seed=SEED,
    n_ctx=CONTEXT_LENGTH,
)


def get_answer_for_the_question(question: str, max_tokens: int = 100) -> str:
    output = LLM(f"Q: {question}. A:", max_tokens=max_tokens, stop=["Q:", "\n", "A:", ":"], echo=False)
    answer_text = output["choices"][0]["text"]
    return answer_text
