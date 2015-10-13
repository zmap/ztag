from datetime import datetime

from ztag.transform import ZGrabTransform, ZMapTransformOutput, Transformable
from ztag import errors, protocols

class SSHBannerTransform(ZGrabTransform):

    name = "ssh/banner"
    port = None
    protocol = protocols.SSH
    subprotocol = protocols.SSH.BANNER

    def _transform_object(self, obj):
        ssh = Transformable(obj)
        server_protocol = dict()
        sp = ssh['data']['ssh']['server_protocol']
        if sp.resolve() is None:
            raise errors.IgnoreObject("no ssh server protocol")
        raw_banner = sp['raw_banner'].resolve()
        if raw_banner is not None:
            server_protocol['raw_banner'] = raw_banner
        protocol_version = sp['protocol_version'].resolve()
        if protocol_version is not None:
            server_protocol['protocol_version'] = protocol_version
        software_version = sp['software_version'].resolve()
        if software_version is not None:
            server_protocol['software_version'] = software_version
        comment = sp['comment'].resolve()
        if comment is not None:
            server_protocol['comment'] = comment
        if len(server_protocol) == 0:
            raise errors.IgnoreObject("Empty server protocol output dict")
        zout = ZMapTransformOutput()
        zout.transformed = server_protocol
        return zout
