from datetime import datetime

from ztag.transform import ZGrabTransform, ZMapTransformOutput, Transformable
from ztag import errors, protocols

class SSHBannerTransform(ZGrabTransform):
    """Transforms ZGrab SSH grabs for Censys.
    Works with output from both the new XSSH grabber and the older SSH grabber."""

    name = "ssh/banner"
    port = None
    protocol = protocols.SSH
    subprotocol = protocols.SSH.BANNER

    def _transform_object(self, obj):
        grab = Transformable(obj)

        # At first, assume we have an XSSH grab and output it in its entirety:
        transformed = grab['data']['xssh'].resolve()

        if transformed is not None:
            # If we have an XSSH grab, output certain fields as before for
            # backward compatibility:
            protocol_version = grab['data']['xssh']['server_id']['version'].resolve()
            if protocol_version is not None:
                transformed['protocol_version'] = protocol_version
            software_version = grab['data']['xssh']['server_id']['software'].resolve()
            if software_version is not None:
                transformed['software_version'] = software_version
            comment = grab['data']['xssh']['server_id']['comment'].resolve()
            if comment is not None:
                transformed['comment'] = comment

        else:
            # This might be an old-style SSH grab. Process it just like we
            # always have:
            sp = grab['data']['ssh']['server_protocol']
            if sp.resolve() is None:
                raise errors.IgnoreObject("No [X]SSH grab data")

            transformed = {}
            raw_banner = sp['raw_banner'].resolve()
            if raw_banner is not None:
                transformed['raw_banner'] = raw_banner
            protocol_version = sp['protocol_version'].resolve()
            if protocol_version is not None:
                transformed['protocol_version'] = protocol_version
            software_version = sp['software_version'].resolve()
            if software_version is not None:
                transformed['software_version'] = software_version
            comment = sp['comment'].resolve()
            if comment is not None:
                transformed['comment'] = comment

        if len(transformed) == 0:
            raise errors.IgnoreObject("Empty [X]SSH protocol output dict")

        zout = ZMapTransformOutput()
        zout.transformed = transformed
        return zout
