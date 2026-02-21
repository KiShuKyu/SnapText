class BaseOCREngine:
    def read_text(self, image):
        """
        :param image: preprocessed image (cv2 image)
        :return: text string
        """
        raise NotImplementedError("Subclasses must implement read_text()")