from ztag.transform import ZMapTransform

from ztag import protocols, errors


class NTPTransform(ZMapTransform):

    name = "ntp/generic"
    port = None
    protocol = protocols.NTP
    subprotocol = protocols.NTP.TIME

    def __init__(self, *args, **kwargs):
        super(NTPTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        classification = obj['classification']
        if classification != "ntp":
            raise errors.IgnoreObject(classification)
        success = int(obj['success'])
        if success != 1:
            raise errors.IgnoreObject("unsuccessful zmap")
        out = dict()
        out['ip_address'] = obj['saddr']
        out['timestamp'] = obj['timestamp-str']
        return out
