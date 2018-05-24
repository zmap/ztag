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
                 scan_id=None, *args, **kwargs):
        super(ZMapTransform, self).__init__(port=port, protocol=protocol,
                                            subprotocol=subprotocol,
                                            scan_id=scan_id, *args, **kwargs)
        if not self.name:
            raise Exception

    def check_port(self, port):
        return self.port is None or self.port == port

    def check_protocol(self, protocol):
        try:
            for p in self.protocol:
                if p.value == protocol.value:
                    return True
        except TypeError:
            return self.protocol is None or \
                self.protocol.value == protocol.value
        else:
            return False

    def check_subprotocol(self, subprotocol):
        return self.subprotocol is None or \
            self.subprotocol.value == subprotocol.value

    def transform(self, obj):
        out = super(ZMapTransform, self).transform(obj)
        out.transformed['ip_address'] = obj['saddr']
        out.transformed['timestamp'] = obj['timestamp_str']
        return out

    @classmethod
    def clean_banner(cls, banner):
        b1 = cls._hostname_regex.sub("CLIENT_HOSTNAME", banner)
        b2 = cls._ip_regex.sub("CLIENT_IP", b1)
        b2 = b2.lstrip().rstrip()
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

    def __init__(self, *args, **kwargs):
        self.strip_domain_prefix = kwargs.get('strip_domain_prefix', '')
        super(ZGrabTransform, self).__init__(*args, **kwargs)

    def transform(self, obj):
        # Intentionally skipping ZMapTransform.transform
        # But...why is this a ZMapTransform in the first place?
        out = super(ZMapTransform, self).transform(obj)
        if "ip" in obj:
            out.transformed['ip_address'] = obj['ip']
        if "domain" in obj:
            domain = obj['domain']
            if self.strip_domain_prefix:
                if domain.startswith(self.strip_domain_prefix):
                    domain = domain[len(self.strip_domain_prefix):]
            out.transformed['domain'] = domain
        out.transformed['timestamp'] = obj['timestamp']
        return out


class ZGrab2Transform(ZMapTransform):
    """
    This is registered in zschema as "zgrab2".
    The generic format is
    {
        "ip": IPv4Address(),
        "domain": String(),
        "data": {
            [scan-id]: {
                "status": Enum(values=["success",
                  "connection-refused",
                  "connection-timeout",
                  "connection-closed",
                  "io-timeout",
                  "protocol-error",
                  "application-error",
                  "unknown-error"
                ]),
                "protocol": [scan-protocol-name],
                "timestamp": DateTime(),
                "result": { [protocol-specific] },
                "error": String(),
            }
        }
    }
    There are some standardized fields in result:
        "tls" is a standard TLS structure (see https.make_tls_obj)
        ...
    """

    # TODO -- pull from zgrab2_schemas.zgrab2.zgrab2.STATUS_VALUES?
    STATUSES = {
        "success",
        "connection-refused",
        "connection-timeout",
        "connection-closed",
        "io-timeout",
        "protocol-error",
        "application-error",
        "unknown-error",
    }

    def __init__(self, *args, **kwargs):
        """
        Same as old ZGrabTransform.
        :param args: Nothing new (forwarded to ZMapTransform)
        :param kwargs: strip_domain_prefix -- optional domain prefix to strip
                       (as with ZGrabTransform)
        """
        self.strip_domain_prefix = kwargs.get('strip_domain_prefix', '')
        super(ZGrab2Transform, self).__init__(*args, **kwargs)

    def invalid_result(self, obj, fmt=None, *args):
        """
        Throw an error indicating that this is not a valid ZGrab2 scan result.
        :param obj: The noncompliant input JSON object
        :param fmt: optional format string for the error message
        :param args: optional format string arguments for the error message
        :raises Exception:
        """
        if fmt is not None:
            suffix = ": %s" % (fmt % args)
        else:
            suffix = ""
        raise Exception("Not a valid ZGrab2 result" + suffix)

    def get(self, obj, *keys):
        """
        Get nested keys from obj, or throw.
        :param obj: the dict to index into
        :param keys: zero or more keys to index into obj
        :return: obj[keys[0]][keys[1]][...][keys[-1]]
        :raises Exception: If any of the keys is absent, or a non-terminal
                            value is not indexable
        """
        temp = obj
        path = []
        for key in keys:
            path.append(key)
            if key not in temp:
                missing = ".".join(path)
                full = ".".join(keys)
                if missing != full:
                    missing = " (of %s)" % full
                self.invalid_result(obj, "field %s is not present.", missing)
            temp = temp[key]
        return temp

    def optget(self, obj, *keys):
        """
        Get nested keys from obj, or return None.
        :param obj:  the dict to index into
        :param keys: zero or more keys to index into obj
        :return: obj[keys[0]][keys[1]][...][keys[-1]], or None.
        """

        try:
            return self.get(obj, *keys)
        except Exception as e:
            return None

    def get_scan_data(self, obj):
        """
        Get the scan data value for this protocol, i.e. obj["data"][scan_id],
        where scan_id is self.scan_id, if present, or self.protocol.pretty_name
        if not.
        :param obj: The input JSON object.
        :return: The scan data (i.e. obj["data"][scan_id])
        :raises Exception: if not present, or if no scan_id can be found.
        """
        scan_id = getattr(self, "scan_id", None) or self.protocol.pretty_name
        if scan_id is not None:
            return self.get(obj, "data", scan_id)
        else:
            data = self.get(obj, "data")
            for k, v in data.items():
                if "protocol" in v:
                    self.scan_id = k
                    self.protocol = v["protocol"]
                    return v
            self.invalid_result(obj)

    def get_scan_results(self, obj):
        """
        Get the protocol-specific scan results for this scan,
        i.e. self.get_scan_data()["result"], or None if not present.
        :param obj: The input JSON object.
        :return: the protocol-specific scan results.
        """

        try:
            data = self.get_scan_data(obj)
            if "result" in data:
                return data["result"]
            return None
        except Exception:
            return None

    def _transform_object(self, obj, tls=True):
        # Child classes should call this first, then fill out the result.
        out = ZMapTransformOutput()
        if "ip" in obj:
            out.transformed["ip_address"] = obj["ip"]
        if "domain" in obj:
            domain = obj["domain"]
            if self.strip_domain_prefix:
                if domain.startswith(self.strip_domain_prefix):
                    domain = domain[len(self.strip_domain_prefix):]
            out.transformed["domain"] = domain

        scan_data = self.get_scan_data(obj)
        status = self.get(scan_data, "status")
        if status not in self.STATUSES:
            self.invalid_result(obj, "%s is not a valid status", status)
        # TODO: Store status?

        out.transformed["timestamp"] = scan_data["timestamp"]

        # By definition, the the service is detected iff the result field is
        # present in the response.
        if self.optget(scan_data, "result") is not None:
            out.transformed["supported"] = True
        else:
            raise IgnoreObject("no zgrab2.result")

        # TODO: Do anything with scan_data["error"]?
        if tls:
            tls_record = self.optget(scan_data, "result", "tls",
                                     "handshake_log")
            if tls_record is not None:
                from ztag.transforms import HTTPSTransform
                tls_out, tls_certs = HTTPSTransform.make_tls_obj(tls_record)
                out.transformed["tls"] = tls_out
                out.certificates = out.certificates + tls_certs

        return out

    def transform(self, obj):
        # Following ZGrabTransform, intentionally skips ZMapTransform.transform
        # But...why is it a ZMapTransform in the first place?
        return super(ZMapTransform, self).transform(obj)
