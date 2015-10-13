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

    def __init__(self, *args, **kwargs):
        super(CWMPTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        http = Transformable(obj)
        http_response = http['data']['http']['response']
        zout = ZMapTransformOutput()
        out = dict()
        error_component = http['error_component'].resolve()
        if error_component is not None and error_component == 'connect':
            raise errors.IgnoreObject("connection error")


        if http_response is not None:
            status_line = http_response['status_line'].resolve()
            status_code = http_response['status_code'].resolve()
            body = http_response['body'].resolve()
            headers = http_response['headers'].resolve()
            if status_line is not None:
                out['status_line'] = status_line
            if status_code is not None:
                out['status_code'] = status_code
            if body is not None:
                out['body'] = body
            if headers is not None:
                out['headers'] = headers

        if len(out) == 0:
            raise errors.IgnoreObject("Empty output dict")

        zout.transformed = out
        return zout
