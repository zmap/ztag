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
        if "encrypt_mode" in prelogin:
            zout.transformed["encrypt_mode"] = prelogin["encrypt_mode"]

    def _transform_object(self, obj):
        zout = super(MSSQLTransform, self)._transform_object(obj)
        results = self.get_scan_results(obj)
        if not results:
            return zout

        # Version is required, ignore this record if it isn't present.
        zout.transformed["version"] = results["version"]

        if "instance_name" in results:
            zout.transformed["instance_name"] = results["instance_name"]
        if "prelogin_options" in results:
            self.load_prelogin_options(results["prelogin_options"], zout)

        return zout
