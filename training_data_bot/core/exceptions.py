class TrainingDataBotError(Exception):
    """Base exception for all Training Data Bot related errors."""

    def __init__(self, message: str = "An error occurred in the Training Data Bot."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"TrainingDataBotError: {self.message}"


class DocumentLoadError(TrainingDataBotError):
    """Raised when there is an issue loading or parsing a document."""

    def __init__(self, document_path: str = None, details: str = None):
        base_message = "Failed to load document"
        if document_path:
            base_message += f" at '{document_path}'"
        if details:
            base_message += f": {details}"
        super().__init__(base_message)

    def __str__(self):
        return f"DocumentLoadError: {self.message}"
