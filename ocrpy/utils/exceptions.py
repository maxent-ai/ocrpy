__all__ = ["FileTypeNotSupported", "AttributeNotSupported", "BackendNotSupported"]


class FileTypeNotSupported(Exception):
    """Raise when processing a file type is not supported by the backends."""

    pass


class AttributeNotSupported(Exception):
    """Raise when an Attribute like block or line extraction is not supported by the backends."""

    pass


class BackendNotSupported(Exception):
    pass
