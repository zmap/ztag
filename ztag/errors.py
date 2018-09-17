class InvalidTag(Exception):
    pass


class IgnoreObject(Exception):

    def __init__(self, original_exception=None, trback=None, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
        self.original_exception = original_exception
        self.trback = trback


class UnknownProtocol(Exception):
    pass


class MissingTransform(Exception):
    pass


class ExtraTransform(Exception):
    pass
