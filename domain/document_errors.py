class UnsupportedDocumentTypeError(ValueError):
    pass


class MalformedDocumentError(ValueError):
    pass


class DocumentExtractionError(RuntimeError):
    pass


class KnowledgeBaseUnavailableError(RuntimeError):
    pass
