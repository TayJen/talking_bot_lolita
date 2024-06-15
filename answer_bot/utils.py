def cleaning_text(text: str) -> str:
    new_text = ""
    i = 0
    quotes_flag = False
    while i < len(text):
        if text[i] == "<":
            quotes_flag = True

        if not quotes_flag:
            new_text += text[i]
        elif text[i] == ">":
            quotes_flag = False
        i += 1
    return new_text
