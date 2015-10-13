import json
import base64
import socket

from ztag.transform import Encoder, ZMapTransformOutput
from encoders import HexEncoder, _SequenceEncoder

import re

strip_regex = re.compile(r'[^\w\. \-\#!\(\)%\[\]\{\}~@\*$^&=|/<>,?`:;]')

def simple_strip(s):
    return strip_regex.sub('', s)


class ProtobufObjectEncoder(Encoder):

    import zsearch_definitions.anonstore_pb2
    from zsearch_definitions.hoststore import ProtocolAtom, Metadatum, Record

    DROP_KEYS = {'ip_address', 'timestamp', 'domain'}

    def __init__(self, port, protocol, subprotocol, scan_id, *args, **kwargs):
        super(ProtobufObjectEncoder, self).__init__(*args, **kwargs)
        self.port = socket.htons(port)
        self.protocol = protocol
        self.subprotocol = subprotocol
        self.scan_id = scan_id

    def encode(self, zout):
        out = ZMapTransformOutput()

        obj = zout.transformed
        ip = obj['ip_address']
        ts = obj['timestamp']
        domain = obj.get('domain', None)
        if zout.metadata.local_metadata is not None:
            obj['metadata'] = zout.metadata.local_metadata.to_dict()

        m = zout.metadata.global_metadata.to_dict()
        tags = list(zout.metadata.tags)

        data = {x: obj[x] for x in obj if x not in self.DROP_KEYS}

        m = {k: simple_strip(v) for k, v in m.iteritems()}

        metadata = self.Metadatum.from_dict(m)
        atom = self.ProtocolAtom(tags=tags, metadata=metadata, data=data)
        record = self.Record(ip, self.port, self.protocol.value, self.subprotocol.value,
                        protocol_atom=atom, domain=domain,
                        timestamp=ts, scan_id=self.scan_id)
        out.transformed = record.protobuf

        out.certificates = []
        for cert_dict in zout.certificates:
            ar = self.zsearch_definitions.anonstore_pb2.AnonymousRecord()
            c = ar.certificate
            c.parsed = json.dumps(cert_dict["parsed"], sort_keys=True)
            c.raw = base64.b64decode(cert_dict["raw"])
            c.sha1fp = cert_dict["parsed"]["fingerprint_sha1"].decode("hex")
            c.sha256fp = cert_dict["parsed"]["fingerprint_sha256"].decode("hex")
            valid_nss = cert_dict.get("nss_trusted", None)
            if valid_nss is not None:
                c.valid_nss = valid_nss
                c.validation_timestamp = record.timestamp
            parents_sha256 = cert_dict.get("parents", None)
            if parents_sha256 is not None:
                c.parents.extend([
                    sha_value.decode("hex") for sha_value in parents_sha256
                ])
            ar.sha256fp = c.sha256fp
            ar.scan_id = self.scan_id
            out.certificates.append(ar)
        return out


class RecordEncoder(ProtobufObjectEncoder):

        def __init__(self, *args, **kwargs):
            super(RecordEncoder, self).__init__(*args, **kwargs)

        def encode(self, obj):
            pb_out = super(RecordEncoder, self).encode(obj)
            out = ZMapTransformOutput()
            out.transformed = pb_out.transformed.SerializeToString()
            out.certificates = [c.SerializeToString() for c in pb_out.certificates]
            out.public_keys = [pk.SerializeToString() for pk in pb_out.public_keys]
            return out


class HexRecordEncoder(_SequenceEncoder):

    def __init__(self, port, protocol, subprotocol, scan_id, *args, **kwargs):
        encs = [
            RecordEncoder(port, protocol, subprotocol, scan_id,
                          *args, **kwargs),
            HexEncoder(*args, **kwargs),
        ]
        super(HexRecordEncoder, self).__init__(encs, *args, **kwargs)
