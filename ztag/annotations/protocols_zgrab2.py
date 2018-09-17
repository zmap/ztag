import sys

from ztag.annotation import Annotation

from ztag import protocols

# Category tags: add the key tag to anything with any of the tags in the value.
ZGRAB2_CATEGORY_TAGS = {
    "database": set(["mssql", "mysql", "oracle", "postgres", "mongodb"]),
}


def __process(self, obj, meta):
    tag = self.protocol.pretty_name
    if obj.get("supported"):
        meta.tags.add(tag)
    else:
        # If this host no longer has the protocol, remove it
        if tag in meta.tags:
            meta.tags.remove(tag)

    for category, protos in ZGRAB2_CATEGORY_TAGS.items():
        # If any of the tags associated with this category are present, add the
        # category tag
        if meta.tags & protos:
            meta.tags.add(category)
        else:
            # Otherwise, it is no longer in the category
            if category in meta.tags:
                meta.tags.remove(category)

    return meta

ZGRAB2_PROTOCOLS = [
    (protocols.MYSQL, protocols.MYSQL.BANNER, {"device_with_mysql": {"tags":["database", "mysql",]}}),
    (protocols.MSSQL, protocols.MSSQL.BANNER, {"device_with_mssql": {"tags":["database", "mssql",]}}),
    (protocols.POSTGRES, protocols.POSTGRES.BANNER, {"device_with_postgres": {"tags":["database", "postgres",]}}),
    (protocols.ORACLE, protocols.ORACLE.BANNER, {"device_with_oracle": {"tags":["database", "oracle",]}}),
    (protocols.IPP, protocols.IPP.BANNER, {"device_with_ipp": {"tags":["ipp"]}}),
    (protocols.MONGODB, protocols.MONGODB.BANNER, {"device_with_mongodb": {"tags":["database", "mongodb"]}}),
]

for proto, subproto, tests in ZGRAB2_PROTOCOLS:
    name = "%sAnnotation" % proto.pretty_name.upper()
    c = type(name, (Annotation,), {"process":__process})
    c.protocol = proto
    c.subprotocol = subproto
    c.tests = tests
    setattr(sys.modules[__name__], name, c)
