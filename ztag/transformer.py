from ztag.transform import ZMapTransform

import errors

# pylint: disable=W0401,W0614
from ztag.transforms import *


class ZMapTransformer(object):

    @classmethod
    def find_transform(cls, port, protocol, subprotocol, scan_id):
        if port is None or protocol is None or subprotocol is None or\
                scan_id is None:
            raise Exception

        ztransforms = list()

        for klass in ZMapTransform.iter():
            t = klass(port, protocol, subprotocol, scan_id)
            if t.check_port(port) and t.check_protocol(protocol) and\
                    t.check_subprotocol(subprotocol):
                ztransforms.append(t)

        if len(ztransforms) == 0:
            raise errors.MissingTransform
        if len(ztransforms) > 1:
            raise errors.ExtraTransform(ztransforms)
        return ztransforms[0]
