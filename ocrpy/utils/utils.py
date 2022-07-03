from cloudpathlib import AnyPath, GSPath, S3Path


__all__ = ["guess_extension", "guess_storage"]


def guess_extension(file_path: str) -> str:
    """
    Guesses the file extension of the file.
    """
    suffix = AnyPath(file_path).suffix
    extension_types = {".png": "IMAGE", ".jpg": "IMAGE", ".pdf": "PDF"}
    return extension_types[suffix] if suffix in extension_types else "UNKNOWN"


def guess_storage(file_path: str) -> str:
    """
    Guesses the storage type of the file.
    """
    path = AnyPath(file_path)
    storage_types = {isinstance(path, GSPath): "GS", isinstance(path, S3Path): "S3"}
    return storage_types[True] if True in storage_types else "LOCAL"
