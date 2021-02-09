import abc
import attr


@attr.s
class LineSegmentation:
    ocr = attr.ib()

    @abc.abstractproperty
    def lines(self):
        return NotImplementedError


@attr.s
class BlockSegmentation:
    ocr = attr.ib()

    @abc.abstractproperty
    def blocks(self):
        return NotImplementedError


@attr.s
class Document:
    image = attr.ib()

    @abc.abstractproperty
    def blocks(self):
        return NotImplementedError

    @abc.abstractproperty
    def lines(self):
        return NotImplementedError

    @abc.abstractproperty
    def tokens(self):
        return NotImplementedError

    @abc.abstractproperty
    def meta(self):
        return NotImplementedError
