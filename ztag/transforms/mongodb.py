import copy
from ztag.transform import ZGrab2Transform
from ztag import protocols


class MongoDBTransform(ZGrab2Transform):

    name = "mongodb/banner"
    port = None
    protocol = protocols.MONGODB
    subprotocol = protocols.MONGODB.BANNER

    def __init__(self, *args, **kwargs):
        super(MongoDBTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = super(MongoDBTransform, self)._transform_object(obj)
        results = self.get_scan_results(obj)
        if not results:
            return zout

        zout.transformed.update(copy.deepcopy(results))

        return zout
