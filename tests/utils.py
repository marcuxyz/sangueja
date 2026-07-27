def load_fixture(filename: str, encoding="utf-8"):
    with open(f"tests/fixtures/{filename}", mode="r", encoding=encoding) as file:
        return file.read()
