from ztag.annotation import *


class FoxBrand(Annotation):

    port = 20000
    protocol = protocols.FOX
    subprotocol = protocols.FOX.DEVICE_ID

    _vendors = {
        "vykon": (Manufacturer.VYKON, Type.SCADA_CONTROLLER),
        "facexp": (Manufacturer.FACEXP, Type.SCADA_CONTROLLER),
        "websopen": (Manufacturer.HONEYWELL, Type.SCADA_CONTROLLER),
        "webs": (Manufacturer.HONEYWELL, Type.SCADA_CONTROLLER),
        "distech": (Manufacturer.DISTECH, Type.SCADA_CONTROLLER),
        "centraline": (Manufacturer.HONEYWELL, Type.SCADA_CONTROLLER),
        "staefa": (Manufacturer.SIEMENS, Type.SCADA_CONTROLLER),
        "tac": (Manufacturer.SCHNEIDER, Type.SCADA_CONTROLLER),
        "webeasy": (Manufacturer.WEBEASY, Type.SCADA_CONTROLLER),
        "alerton": (Manufacturer.ALERTON, Type.HVAC),
        "nexrev": (Manufacturer.NEXREV, Type.HVAC),
        "comfortpoint": (Manufacturer.HONEYWELL, Type.SCADA_CONTROLLER),
        "novar.opus": (Manufacturer.NOVAR, Type.HVAC),
        "trend": (Manufacturer.TREND, Type.SCADA_CONTROLLER),
        "tridium": (Manufacturer.TRIDIUM, Type.SCADA_CONTROLLER),
        "bactalk": (Manufacturer.ALERTON, Type.SCADA_CONTROLLER),
        "webvision": (Manufacturer.HONEYWELL, Type.HVAC),
        "trane": (Manufacturer.TRANE, Type.HVAC),
        "integra": (Manufacturer.INTEGRA, Type.CINEMA),
        "wattstopper": (Manufacturer.WATTSTOPPER, Type.LIGHT_CONTROLLER),
        "vyko": (Manufacturer.VYKON, Type.SCADA_CONTROLLER),
        "eiq": (Manufacturer.EIQ, Type.SOLAR_PANEL),
        "thinksimple": (Manufacturer.THINK_SIMPLE, Type.SCADA_CONTROLLER),
    }

    _tests = {
        "vykon": {
            "global_metadata": {
                "manufacturer": Manufacturer.VYKON,
                "type": Type.SCADA_CONTROLLER,
            },
        },
        "wattstopper": {
            "global_metadata": {
                "manufacturer": Manufacturer.WATTSTOPPER,
                "type": Type.LIGHT_CONTROLLER,
            },
        },
        "thinksimple": {
            "global_metadata": {
                "manufacturer": Manufacturer.THINK_SIMPLE,
                "type": Type.SCADA_CONTROLLER,
            },
        },
    }


    def process(self, obj, meta):
        vendor = obj["vendor_id"].lower().strip()
        v = _vendors[vendor]
        meta.global_metadata.manufacturer = v[1]
        meta.global_metadata.device_type = v[2]
        return meta
