from ztag.transform import ZMapTransform, ZMapTransformOutput, Transformable

from ztag import protocols, errors


class UPnPTransform(ZMapTransform):

    name = "UPnP/generic"
    port = None
    protocol = protocols.UPNP
    subprotocol = protocols.UPNP.DISCOVERY

    KEYS = [
        "server",
        "location",
        "usn",
        "st",
        "ext",
        "cache-control",
        "x-user-agent",
        "agent"
    ]

    def _transform_object(self, obj):
        classification = obj['classification']
        if classification != "upnp":
            raise errors.IgnoreObject(classification)
        success = int(obj['success'])
        if success != 1:
            raise errors.IgnoreObject("unsuccessful zmap")

        wrapped = Transformable(obj)
        transformed = {}
        for key in self.KEYS:
            transformed[key] = wrapped[key].resolve()
        out = ZMapTransformOutput()
        out.transformed = transformed
        return out
