class BaseOCREngine:
    def __init__(self, languages: str):
        self.languages = languages

    def read_text(self, image) -> tuple[str, float]:
        raise NotImplementedError