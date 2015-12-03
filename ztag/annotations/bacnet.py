from ztag.annotation import *

class GenericBACNET(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        manufacturer = obj["vendor"]["reported_name"]
        model = obj["model_name"]
        meta.global_metadata.manufacturer = manufacturer
        meta.global_metadata.product = model
        meta.tags.add("scada")
        meta.tags.add("building control")
        return meta



class GenericBACNETController(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    MODELS = set([
        "LGE",
        "pCOWeb@",
        "eBMGR-TCH",
        "Excel Web",
        "DSC_1212E",
        "DSC_606E",
        "DSC_1146E",
        "ETHER-Link",
        "Eagle",
        "Kieback&Peter DDC4000",
        "BCM-Eth Controller",
        "bCX1-CR",
        "PXC64-U + PXA30-W0 / HW=V2.02",
        "ME812u-LGR",
        "ME-LGR25",
        "BAC-A1616BC",
        "EY-RC500F001",
        "PXC100ED / HW=V1.00",
        "FG-32/20",
        "PXC100ED + PXA40-W0 / HW=V1.00",
        "I/O Pro 812u",
        "PMC BACnet Building Controller"

    ])

    def process(self, obj, meta):
        manufacturer = obj["vendor"]["reported_name"]
        model = obj["model_name"]
        if model in self.MODELS:
            meta.global_metadata.device_type = Type.SCADA_CONTROLLER
            return meta



class GenericHVAC(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None


    MODELS = set([
        "Tracer SC",
        "i-Vu CCN Router",
        "BM ADAPTER"
    ])

    def process(self, obj, meta):
        manufacturer = obj["vendor"]["reported_name"]
        model = obj["model_name"]
        if model in self.MODELS:
            meta.global_metadata.device_type = Type.HVAC
            return meta


class BACNETGenericServer(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    MODELS = set([
        "NiagaraAX Station",
        "ENS-1",
        "Building Operation Automation Server",
        "WebAccess Bacnet Server",
        "Insight",
        "INSIGHT",
        "Compass",
        "SmartStruxure",
        "BACnet Direct",
        "SCADA Engine Server for Windows V1.0",
        "Building Operation Enterprise Server",
        "NiagaraAX BACnet Workstation",
        "Eagle",
        "Phoenix Controls MicroServer"
    ])

    def process(self, obj, meta):
        manufacturer = obj["vendor"]["reported_name"]
        model = obj["model_name"]
        if model in self.MODELS:
            meta.global_metadata.device_type = Type.SCADA_SERVER
            return meta


class MachProWeb(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    DEVICES = set([
        "MACH-ProWebSys",
        "MACH-ProWebCom",
        "MACH-ProCom",
        "MACH-ProSys",
    ])

    def process(self, obj, meta):
        model = obj["model_name"]
        if model in self.DEVICES:
            meta.global_metadata.device_type = Type.SCADA_CONTROLLER
            return meta


class MELGR(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model.startswith("LGR") or models.startwith("ME-LGR"):
            meta.global_metadata.device_type = Type.SCADA_CONTROLLER
            return meta



class DeltaDSMRTR(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        manufacturer = obj["vendor"]["reported_name"]
        model = obj["model_name"]
        if model == "DSM_RTR" or model == "DSM-RTR":
            meta.global_metadata.device_type = Type.SCADA_ROUTER
            return meta


class WebCTRL(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model in ("WC17", "WC18"):
            meta.global_metadata.device_type = Type.SCADA_FRONTEND
            return meta


class SAUTERAS525(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model == "EY-AS525F001":
            meta.global_metadata.device_type = Type.HVAC
            return meta


class DSC1616E(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model == "DSC_1616E":
            meta.global_metadata.device_type = Type.HVAC
            return meta


class GenericBACNETRouter(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    MODELS = set([
        "BASRT-B",
        "iVu Open Router",
        "ivuccnrouter",
        "PXG3.L",
        "iVu Open Link"
    ])

    def process(self, obj, meta):
        model = obj["model_name"]
        if model in self.MODELS:
            meta.global_metadata.device_type = Type.SCADA_ROUTER
            return meta


class EBCON(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model == "eBCON":
            meta.global_metadata.device_type = Type.HVAC
            return meta


class PCO1000WB0(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model == "PCO1000WB0":
            meta.global_metadata.device_type = Type.HVAC
            return meta


class MSNA(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model.startswith("MS-NAE") or model.startswith("MS-NCE"):
            meta.global_metadata.device_type = Type.SCADA_CONTROLLER
            return meta


class SiemensFieldPanel(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model == "Siemens BACnet Field Panel":
            meta.global_metadata.device_type = Type.SCADA_FRONTEND
            return meta


class AAMRouter(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model == "AAM-Router":
            meta.global_metadata.device_type = Type.SCADA_ROUTER
            return meta



class PowerHawk(Annotation):

    protocol = protocols.BACNET
    subprotocol = protocols.BACNET.DEVICE_ID
    port = None

    def process(self, obj, meta):
        model = obj["model_name"]
        if model.startswith("Powerhawk"):
            meta.global_metadata.device_type = Type.POWER_MONITOR
            return meta


