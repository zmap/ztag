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

        to_copy = ["protocol_version", "server_version", "capability_flags",
                   "status_flags", "error_code", "error_message", "error_id"]
        for f in to_copy:
            if results.get(f) is not None:
                zout.transformed[f] = results[f]

        to_clean = ["error_message"]
        for f in to_clean:
            if f in zout.transformed:
                zout.transformed[f] = self.clean_banner(zout.transformed[f])

        return zout
