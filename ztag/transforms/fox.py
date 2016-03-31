from ztag.transform import *
from ztag import protocols, errors

class NiagaraFoxTransform(ZGrabTransform):

    name = "fox/device_id"
    port = 1911
    protocol = protocols.FOX
    subprotocol = protocols.FOX.DEVICE_ID

    def _transform_object(self, obj):
        zout = ZMapTransformOutput()
        wrapped = Transformable(obj)
        fox = wrapped['data']['fox']
        if not fox['is_fox'].resolve():
            raise errors.IgnoreObject()

        instance_number = fox['instance_number'].resolve()
        version = fox['version'].resolve()
        id_ = fox['id'].resolve()
        hostname = fox['hostname'].resolve()
        host_address = fox['host_address'].resolve()
        app_name = fox['app_name'].resolve()
        app_version = fox['app_version'].resolve()
        vm_name = fox['vm_name'].resolve()
        vm_version = fox['vm_version'].resolve()
        os_name = fox['os_name'].resolve()
        os_version = fox['os_version'].resolve()
        station_name = fox['station_name'].resolve()
        language = fox['language'].resolve()
        time_zone = fox['time_zone'].resolve()
        host_id = fox['host_id'].resolve()
        vm_uuid = fox['vm_uuid'].resolve()
        brand_id = fox['brand_id'].resolve()
        sys_info = fox['sys_info'].resolve()
        auth_agent_type = fox['auth_agent_type'].resolve()

        out = dict()
        out["is_fox"] = True
        if instance_number:
            out["instance_number"] = instance_number
        if version:
            out["version"] = version
        if id_:
            out["id"] = id_
        if hostname:
            out["hostname"] = hostname
        if host_address:
            out["host_address"] = host_address
        if app_name:
            out["app_name"] = app_name
        if app_version:
            out["app_version"] = app_version
        if vm_name:
            out["vm_name"] = vm_name
        if vm_version:
            out["vm_version"] = vm_version
        if os_name:
            out["os_name"] = os_name
        if os_version:
            out["os_version"] = os_version
        if station_name:
            out["station_name"] = station_name
        if language:
            out["language"] = language
        if time_zone:
            out["time_zone"] = time_zone
        if host_id:
            out["host_id"] = host_id
        if vm_uuid:
            out["vm_uuid"] = vm_uuid
        if brand_id:
            out["brand_id"] = brand_id
        if sys_info:
            out["sys_info"] = sys_info
        if auth_agent_type:
            out["auth_agent_type"] = auth_agent_type

        if not bool(out):
            raise errors.IgnoreObject("Empty output dict")
        zout.transformed = out
        return zout

