from ztag.transform import ZGrabTransform, ZMapTransformOutput
from ztag.transform import Transformable
from ztag import protocols, errors


class ModbusTransform(ZGrabTransform):

    name = "modbus/mei-device-id"
    port = 502
    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID

    def __init__(self, *args, **kwargs):
        super(ModbusTransform, self).__init__(*args, **kwargs)

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        wrapped = Transformable(obj)
        modbus = wrapped['data']['modbus']
        if not modbus['raw_response'].resolve():
            raise errors.IgnoreObject()

        out = dict()
        out["support"] = True
        function_code = modbus['function_code'].resolve()
        if function_code:
            out['function_code'] = function_code
        mei_response = modbus['mei_response']
        if mei_response:
            conformity_level = mei_response['conformity_level'].resolve()
            objects = mei_response['objects']
            vendor = objects['vendor'].resolve()
            product_code = objects['product_code'].resolve()
            revision = objects['revision'].resolve()
            vendor_url = objects['vendor_url'].resolve()
            product_name = objects['product_name'].resolve()
            model_name = objects['model_name'].resolve()
            user_application_name = objects['user_application_name'].resolve()

            if conformity_level or vendor or product_code or revision or \
            vendor_url or product_name or model_name or user_application_name:
                out['mei_response'] = dict()

            if vendor or product_code or revision or vendor_url or product_name \
            or model_name or user_application_name:
                out['mei_response']['objects'] = dict()

            if conformity_level:
                out['mei_response']['conformity_level'] = conformity_level
            if vendor:
                out['mei_response']['objects']['vendor'] = vendor
            if product_code:
                out['mei_response']['objects']['product_code'] = product_code
            if revision:
                out['mei_response']['objects']['revision'] = revision
            if vendor_url:
                out['mei_response']['objects']['vendor_url'] = vendor_url
            if product_name:
                out['mei_response']['objects']['product_name'] = product_name
            if model_name:
                out['mei_response']['objects']['model_name'] = model_name
            if user_application_name:
                    out['mei_response']['objects']['user_application_name'] = \
                        user_application_name

        zout.transformed = out
        return zout
