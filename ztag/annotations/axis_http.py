from ztag.annotation import *

class AXISHTTP(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "axis_2120_network_camera":{
        "global_metadata":{
          "manufacturer":Manufacturer.AXIS,
          "device_type":Type.CAMERA,
          "product":"2120 Network Camera",
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        if obj["title"] == "AXIS 2120 Network Camera":
            meta.global_metadata.manufacturer = Manufacturer.AXIS
            meta.global_metadata.product = "2120 Network Camera"
            meta.global_metadata.device_type = Type.CAMERA
            meta.tags.add("embedded")
            return meta

        if obj["title"] == "AXIS 2100 Network Camera":
            meta.global_metadata.manufacturer = Manufacturer.AXIS
            meta.global_metadata.product = "2100 Network Camera"
            meta.global_metadata.device_type = Type.CAMERA
            meta.tags.add("embedded")
            return meta

        if obj["title"].startswith("Live view / - AXIS 205 Network Camera"):
            meta.global_metadata.manufacturer = Manufacturer.AXIS
            meta.global_metadata.product = "205 Network Camera"
            meta.global_metadata.device_type = Type.CAMERA
            meta.tags.add("embedded")
            return meta

