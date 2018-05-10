from ztag.transform import ZGrab2Transform
from ztag import protocols


class MySQLTransform(ZGrab2Transform):

    name = "mysql/banner"
    port = None
    protocol = protocols.MYSQL
    subprotocol = protocols.MYSQL.BANNER

    def __init__(self, *args, **kwargs):
        super(MySQLTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = super(MySQLTransform, self)._transform_object(obj)
        results = self.get_scan_results(obj)
        if not results:
            return zout

        if "protocol_version" in results:
            zout.transformed["protocol_version"] = results["protocol_version"]
        if "server_version" in results:
            zout.transformed["server_version"] = results["server_version"]
        if "capability_flags" in results:
            zout.transformed["capability_flags"] = results["capability_flags"]
        if "status_flags" in results:
            zout.transformed["status_flags"] = results["status_flags"]
        if "error_code" in results:
            zout.transformed["error_code"] = results["error_code"]
        if "error_message" in results:
            zout.transformed["error_message"] = results["error_message"]

        return zout
