import subprocess

from answer_bot.llama import get_answer_for_the_question
from answer_bot.utils import cleaning_text


def pronounce_text(sex_voice: str, text: str) -> None:
    sex_to_voice_name = {"man": "Daniel", "woman": "Samantha"}

    assert sex_voice in sex_to_voice_name
    subprocess.call(["say", "-v", sex_to_voice_name[sex_voice], "-r", "180", text])


if __name__ == "__main__":
    question = "What is your programming language preference?"
    sex = "woman"

    answer = get_answer_for_the_question(question)
    clean_text = cleaning_text(answer)
    print(clean_text)

    pronounce_text(sex, clean_text)
