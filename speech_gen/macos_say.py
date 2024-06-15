import subprocess

sex_to_voice_name = {"man": "Daniel", "woman": "Samantha"}


def pronounce_text(sex_voice: str, text: str) -> None:
    assert sex_voice in sex_to_voice_name
    subprocess.call(["say", "-v", sex_to_voice_name[sex_voice], "-r", "180", text])
