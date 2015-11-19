import json

from ztag.transform import Encoder


class JSONEncoder(Encoder):

    def encode(self, zobj):
        obj = zobj.transformed or dict()
        if zobj.metadata is not None:
            obj['local_metadata'] = zobj.metadata.local_metadata.to_dict()
            obj['global_metadata'] = zobj.metadata.global_metadata.to_dict()
            obj['tags'] = list(zobj.metadata.tags)
        return json.dumps(obj, sort_keys=True)


class LocalJSONEncoder(Encoder):

    def encode(self, zobj):
        obj = zobj.transformed or dict()
        if zobj.metadata is not None:
            obj['metadata'] = zobj.metadata.local_metadata.to_dict()
        return json.dumps(obj, sort_keys=True)



class HexEncoder(Encoder):

    def encode(self, obj):
        return obj.encode("hex")


class IdentityEncoder(Encoder):

    def encode(self, obj):
        return obj


class _SequenceEncoder(Encoder):

    def __init__(self, encoders, *args, **kwargs):
        super(_SequenceEncoder, self).__init__(self, *args, **kwargs)
        self.encoders = encoders

    def encode(self, obj):
        out = obj
        for encoder in self.encoders:
            out = encoder.encode(out)
        return out


def encoder_sequence(encoders):
    return _SequenceEncoder(encoders)
