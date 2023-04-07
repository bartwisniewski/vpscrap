def clean_text(text: str) -> str:
    clean_lines = []
    for line in text.split("\n"):
        if line:
            clean_lines.append(line.strip())
    return " ".join(clean_lines)
