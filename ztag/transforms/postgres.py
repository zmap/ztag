from ztag.transform import ZGrab2Transform
from ztag import protocols


class PostgresTransform(ZGrab2Transform):

    name = "postgres/banner"
    port = None
    protocol = protocols.POSTGRES
    subprotocol = protocols.POSTGRES.BANNER

    def __init__(self, *args, **kwargs):
        super(PostgresTransform, self).__init__(*args, **kwargs)

    def clean_error(self, err):
        return {k: self.clean_banner(v) for k, v in err.items()}

    def _transform_object(self, obj):
        zout = super(PostgresTransform, self)._transform_object(obj)
        results = self.get_scan_results(obj)
        if not results:
            return zout

        to_copy = ["supported_versions", "protocol_error", "startup_error",
                   "backend_key_data"]

        for f in to_copy:
            if results.get(f) is not None:
                zout.transformed[f] = results[f]

        to_clean_error = ["protocol_error", "startup_error"]
        for f in to_clean_error:
            if f in zout.transformed:
                zout.transformed[f] = self.clean_error(zout.transformed[f])

        to_clean_banner = ["supported_versions"]
        for f in to_clean_banner:
            if f in zout.transformed:
                zout.transformed[f] = self.clean_banner(zout.transformed[f])

        if "is_ssl" in results:
            zout.transformed["is_ssl"] = bool(results.get("is_ssl", False))

        if results.get("authentication_mode") is not None:
            zout.transformed["authentication_mode"] = [
                x["mode"] for x in results["authentication_mode"]
            ]

        if results.get("backend_key_data") is not None:
            zout.transformed["backend_key_data"] = results["backend_key_data"]

        return zout
