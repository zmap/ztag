from ztag.transform import ZGrab2Transform
from ztag import protocols


class MSSQLTransform(ZGrab2Transform):

    name = "mssql/banner"
    port = None
    protocol = protocols.MSSQL
    subprotocol = protocols.MSSQL.BANNER

    def __init__(self, *args, **kwargs):
        super(MSSQLTransform, self).__init__(*args, **kwargs)

    def load_prelogin_options(self, prelogin, zout):
        if prelogin.get("encrypt_mode") is not None:
            zout.transformed["encrypt_mode"] = prelogin["encrypt_mode"]

    def _transform_object(self, obj):
        zout = super(MSSQLTransform, self)._transform_object(obj)
        results = self.get_scan_results(obj)
        if not results:
            return zout

        to_copy = ["version", "instance_name", "encrypt_mode"]

        for f in to_copy:
            if results.get(f) is not None:
                zout.transformed[f] = results[f]

        # If we don't have a root encrypt_mode, fall back to prelogin_options
        if zout.transformed.get("encrypt_mode") is None:
            if results.get("prelogin_options") is not None:
                self.load_prelogin_options(results["prelogin_options"], zout)

        return zout
