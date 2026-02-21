class BaseOCREngine:
    def read_text(self, image):
        raise NotImplementedError("Subclasses must implement read_text()")