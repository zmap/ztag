import json
import re

from ztag.errors import IgnoreObject


class Transformable(object):
    """A wrapper for objects accessed with [] notation (e.g objects
    who internally call __getitem__) that replaces any method call with
    a no-op after the first accessor error, resulting in an empty
    object that serializes to null when used with the custom encoder"""

    class Empty(object):
        """Internal object representing failure / empty"""

        def __getitem__(self, key):
            return self

        def resolve(self):
            return None

        def to_json(self):
            return None

    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, key):
        try:
            val = self.obj[key]
        except (KeyError, TypeError, IndexError):
            return self.Empty()
        if val is None:
            return self.Empty()
        return Transformable(val)

    def to_json(self):
        return self.obj

    def resolve(self):
        return self.obj


class TransformableEncoder(json.JSONEncoder):
    """Use when encoding objects wrapped in Transformable to JSON."""

    def default(self, o):
        try:
            out = o.to_json()
        except AttributeError:
            pass
        else:
            return out
        return json.JSONEncoder.default(self, o)


class Transform(object):

    def __init__(self, *args, **kwargs):
        pass

    def transform(self, obj):
        try:
            return self._transform_object(obj)
        except (KeyError, TypeError, IndexError) as e:
            raise IgnoreObject(original_exception=e)

    def _transform_object(self, obj):
        raise NotImplementedError


class Encoder(Transform):

    def __init__(self, *args, **kwargs):
        super(Encoder, self).__init__(*args, **kwargs)

    def encode(self, obj):
        raise NotImplementedError

    def _transform_object(self, obj):
        return self.encode(obj)


class Decoder(Transform):

    def __init__(self, *args, **kwargs):
        super(Decoder, self).__init__(*args, **kwargs)

    def decode(self, s):
        raise NotImplementedError

    def _transform_object(self, obj):
        return self.decode(obj)


class ZMapTransformOutput(object):

    def __init__(self):
        self.transformed = dict()
        self.certificates = list()
        self.public_keys = list()
        self.metadata = None

    def __str__(self):
        parts = [
            '-----BEGIN RESULT-----',
            str(self.transformed),
            str(self.certificates),
            str(self.public_keys),
            str(self.metadata),
            '-----END RESULT-----',
        ]
        return '\n'.join(parts)

class ZMapTransform(Transform):

    name = None
    port = None
    protocol = None
    subprotocol = None
    incoming = None
    decoder = None

    _hostname_regex = re.compile(r"researchscan[0-9]+\.eecs\.umich\.edu")
    _ip_regex = re.compile(r"141\.212\.12[1-2]\.[0-9]+")

    def __init__(self, port=None, protocol=None, subprotocol=None,
                 scan_id=None):
        super(ZMapTransform, self).__init__(port=port, protocol=protocol,
                                            subprotocol=subprotocol,
                                            scan_id=scan_id)
        if not self.name:
            raise Exception

    def check_port(self, port):
        return self.port is None or self.port == port

    def check_protocol(self, protocol):
        return self.protocol is None or self.protocol.value == protocol.value

    def check_subprotocol(self, subprotocol):
        return self.subprotocol is None or \
                self.subprotocol.value == subprotocol.value

    def transform(self, obj):
        out = super(ZMapTransform, self).transform(obj)
        out.transformed['ip_address'] = obj['saddr']
        out.transformed['timestamp'] = obj['timestamp-str']
        return out

    @classmethod
    def clean_banner(cls, banner):
        b1 = cls._hostname_regex.sub("CLIENT_HOSTNAME", banner)
        b2 = cls._ip_regex.sub("CLIENT_IP", b1)
        return b2

    @classmethod
    def iter(cls):
        for klass in cls.find_subclasses():
            if klass.name:
                yield klass

    @classmethod
    def find_subclasses(cls):
        return set(cls.__subclasses__() + [g for s in cls.__subclasses__()
                                           for g in s.find_subclasses()])


class ZGrabTransform(ZMapTransform):

    def transform(self, obj):
        out = super(ZMapTransform, self).transform(obj)
        out.transformed['ip_address'] = obj['ip']
        out.transformed['timestamp'] = obj['timestamp']
        domain = obj.get('domain', None)
        if domain:
            out.transformed['domain'] = domain
        return out
