import logging

__all__ = ["LOGGER"]

LOGGER = logging.getLogger("ocrpy")
fhandler = logging.FileHandler(filename="ocrpy.log", mode="a")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fhandler.setFormatter(formatter)
LOGGER.addHandler(fhandler)
LOGGER.setLevel(logging.DEBUG)
