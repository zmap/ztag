from ztag.transform import ZMapTransform, ZMapTransformOutput
from ztag import protocols, errors
from ztag.transform import Transformable
import re
import http

class CWMPTransform(http.HTTPTransform):

    name = "cwmp/generic"
    port = None
    protocol = protocols.CWMP
    subprotocol = protocols.CWMP.GET

