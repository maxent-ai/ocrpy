"""
Google OCR API
"""
import cv2
import attr
from .base import Document
from .base import LineSegmentation
from .base import BlockSegmentation

@attr.s
class GcpOCR:
    """
    Google OCR API
    """
    