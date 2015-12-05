from ztag.annotation import *


class FoxBrand(Annotation):

    port = 1911
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

    tests = {
        "vykon": {
            "global_metadata": {
                "manufacturer": Manufacturer.VYKON,
                "device_type": Type.SCADA_CONTROLLER,
            },
        },
        "wattstopper": {
            "global_metadata": {
                "manufacturer": Manufacturer.WATTSTOPPER,
                "device_type": Type.LIGHT_CONTROLLER,
            },
        },
        "thinksimple": {
            "global_metadata": {
                "manufacturer": Manufacturer.THINK_SIMPLE,
                "device_type": Type.SCADA_CONTROLLER,
            },
        },
    }


    def process(self, obj, meta):
        vendor = obj["brand_id"].lower().strip()
        m, dt = self._vendors[vendor]
        meta.global_metadata.manufacturer = m
        meta.global_metadata.device_type = dt
        return meta
