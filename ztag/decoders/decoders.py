import json
import sys

from ztag.transform import Decoder
from ztag import errors


class JSONDecoder(Decoder):

    def __init__(self, logger=None, *args, **kwargs):
        super(JSONDecoder, self).__init__(*args, **kwargs)
        self.logger = logger

    def decode(self, s):
        try:
            return json.loads(s)
        except ValueError as e:
            self.logger.error(str(e))
            self.logger.error(s.strip())
            raise errors.IgnoreObject(e)


class TSVDecoder(Decoder):

    def __init__(self, *args, **kwargs):
        super(TSVDecoder, self).__init__(*args, **kwargs)

    def decode(self, s):
        return s.rstrip().split("\t")


class NullDecoder(Decoder):

    def __init__(self, *args, **kwargs):
        super(NullDecoder, self).__init__(*args, **kwargs)

    def decode(self, s):
        return s
