from ztag.transform import ZGrab2Transform
from ztag import protocols


class PostgresTransform(ZGrab2Transform):

    name = "postgres/banner"
    port = None
    protocol = protocols.POSTGRES
    subprotocol = protocols.POSTGRES.BANNER

    def __init__(self, *args, **kwargs):
        super(PostgresTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = super(PostgresTransform, self)._transform_object(obj)
        results = self.get_scan_results(obj)
        if not results:
            return zout

        if "supported_versions" in results:
            zout.transformed["supported_versions"] = results["supported_versions"]
        if "protocol_error" in results:
            zout.transformed["protocol_error"] = results["protocol_error"]
        if "startup_error" in results:
            zout.transformed["startup_error"] = results["startup_error"]
        if "is_ssl" in results:
            zout.transformed["is_ssl"] = bool(results.get("is_ssl", False))
        if "authentication_mode" in results:
            zout.transformed["authentication_mode"] = [
                x["mode"] for x in results["authentication_mode"]
            ]
        if "backend_key_data" in results:
            zout.transformed["backend_key_data"] = results["backend_key_data"]
        return zout
