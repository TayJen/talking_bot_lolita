import subprocess

from llama_cpp import Llama

MODEL = "./weights/codellama-7b.Q4_0.gguf"

llm = Llama(
    model_path=MODEL,
    n_gpu_layers=1,
    seed=13,
    n_ctx=512,
)


def get_answer_for_the_question(question: str, max_tokens: int = 100) -> str:
    output = llm(
        f"Q: {question}. A:",
        max_tokens=max_tokens,
        stop=["Q:", "\n", "A:", ":"],
        echo=False
    )
    answer_text = output['choices'][0]['text']
    return answer_text


def cleaning_text(text: str) -> str:
    new_text = ""
    i = 0
    quotes_flag = False
    while i < len(text):
        if text[i] == '<':
            quotes_flag = True

        if not quotes_flag:
            new_text += text[i]
        elif text[i] == '>':
            quotes_flag = False
        i += 1
    return new_text


def pronounce_text(sex_voice: str, text: str) -> None:
    sex_to_voice_name = {
        "man": "Daniel",
        "woman": "Samantha"
    }

    assert sex_voice in sex_to_voice_name
    subprocess.call(["say", "-v", sex_to_voice_name[sex_voice], "-r", "180", text])


if __name__ == "__main__":
    question = "What is your programming language preference?"
    sex = "woman"

    answer = get_answer_for_the_question(question)
    clean_text = cleaning_text(answer)
    print(clean_text)

    pronounce_text(sex, clean_text)
