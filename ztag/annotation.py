import re
import pkgutil
import os
import os.path
import imp
import ztag.annotations

from ztag import protocols
from ztag.errors import InvalidTag


class MetadataBase(object):

    def __init__(self):
        self.manufacturer = None
        self.product = None
        self.version = None
        self.revision = None
        self._description = None

    @property
    def description(self):
        # Populate the description field
        desc_fields = [
            self.manufacturer,
            self.product,
            self.version,
            self.revision,
        ]
        populated_fields = [field for field in desc_fields if field]
        if populated_fields:
            return " ".join(populated_fields)
        return None

    def merge(self, other):
        if self.manufacturer is None:
            self.manufacturer = other.manufacturer
        if self.product is None:
            self.product = other.product
        if self.version is None:
            self.version = other.version
        if self.revision is None:
            self.revision = other.revision

    def to_dict(self, with_description=True):
        out = dict()
        if self.manufacturer is not None:
            out['manufacturer'] = self.manufacturer
        if self.product is not None:
            out['product'] = self.product
        if self.version is not None:
            out['version'] = self.version
        if self.revision is not None:
            out['revision'] = self.revision
        if len(out) > 0 and with_description:
            out['description'] = self.description
        return out


class LocalMetadata(MetadataBase):

    def __init__(self):
        super(LocalMetadata, self).__init__()


class GlobalMetadata(MetadataBase):

    def __init__(self):
        super(GlobalMetadata, self).__init__()
        self.os = None
        self.os_version = None
        self.device_type = None

    def merge(self, other):
        super(GlobalMetadata, self).merge(other)
        if self.os is None:
            self.os = other.os
        if self.os_version is None:
            self.os_version = other.os_version
        if self.device_type is None:
            self.device_type = other.device_type

    def to_dict(self, with_description=True):
        out = super(GlobalMetadata, self)\
                .to_dict(with_description=with_description)
        if self.os is not None:
            out['os'] = self.os
        if self.os_version is not None:
            out['os_version'] = self.os_version
        if self.device_type is not None:
            out['device_type'] = self.device_type
        return out


class Metadata(object):

    def __init__(self):
        self.local_metadata = LocalMetadata()
        self.global_metadata = GlobalMetadata()
        self.tags = set()

    def merge(self, other):
        self.local_metadata.merge(other.local_metadata)
        self.global_metadata.merge(other.global_metadata)
        self.tags |= other.tags


# types of devices, e.g., primary purpose of an embedded device
class Type(object):

    CABLE_MODEM = "cable modem"
    DSL_MODEM = "DSL modem"
    WIRELESS_MODEM = "wireless modem"
    MODEM = "DSL/cable modem"

    ALARM_SYSTEM = "alarm system"
    CAMERA = "camera"
    CINEMA = "cinema"
    DVR = "DVR"
    ENVIRONMENT_MONITOR = "environment monitor"
    GENERIC_PRINTER = "printer"
    PRINTER = "printer"
    INDUSTRIAL_CONTROL = "industrial control system"
    INFRASTRUCTURE_ROUTER = "infrastructure router"
    INKJET_PRINTER = "inkjet printer"

    IPMI = "IPMI"
    SERVER_MANAGEMENT = "IPMI"

    LASER_PRINTER = "laser printer"
    LIGHT_CONTROLLER = "light controller"
    MUTLIFUNCTION_PRINTER = "multifunction printer"
    NAS = "nas"
    NETWORK = "network"
    SWITCH = "switch"
    FIREWALL = "firewall"
    FIRE_ALARM = "fire alarm"
    NETWORK_ANALYZER = "network analyzer"
    PDU = "power distribution unit"
    PHASER_PRINTER = "phaser printer"
    PLC = "programmable logic controller"
    POWER_CONTROLLER = "power controller"
    POWER_MONITOR = "power monitor"
    PRINT_SERVER = "print server"

    SCADA_CONTROLLER = "scada controller"
    SCADA_GATEWAY = "scada gateway"
    SCADA_PROCESSOR = "scada processor"
    SCADA_ROUTER = "scada router"
    SCADA_FRONTEND = "scada frontend"
    SCADA_SERVER = "scada server"

    SOHO_ROUTER = "soho router"
    SOLAR_PANEL = "solar panel"
    STORAGE = "storage"
    TEMPERATURE_MONITOR = "temperature monitor"
    THERMOSTAT = "thermostat"
    TV_BOX = "set-top box"
    TV_TUNER = "TV tuner"
    UPS = "UPS"
    USB_HUB = "usb"
    VOIP = "VoIP phone"
    WATER_FLOW_CONTROLLER = "water flow controller"
    WIFI = "wifi"
    HVAC = "hvac"
    ACCESS_CONTROL = "access control"
    POWER_MONITOR = "power monitor"
    SIGN = "sign"
    KVM = "kvm"


class Manufacturer(object):

    ABB_STOTZ_KONTAKT = "ABB Stotz Kontakt"
    ACTL = "ACTL"
    ADTRAN = "ADTRAN"
    AGRANAT = "Agranat"
    ALCATEL = "Alcatel"
    ALERTON = "Alerton"
    ALLEGRO = "Allegro"
    ALLWORKS = "allworx"
    AMERICANMEGATRENDS = "American Megatrends Inc."
    APPLE = "Apple"
    APACHE = "Apache"
    APC = "APC"
    ARUBA = "Aruba Networks"
    ASUS = "ASUS"
    AVM = "AVM"
    AVTECH = "AVTech"
    AXIS = "Axis"
    BELKIN = "Belkin"
    BIGIP = "BigIP"
    BOMGAR = "Bomgar"
    BROTHER = "Brother"
    CANON = "Canon"
    CHEROKEE = "Cherokee"
    CISCO = "Cisco"
    CLARIION = "Clariion"
    COMPUTEC = "Computec OY"
    COMTROL = "Comtrol Corporation"
    CROUZET = "Crouzet"
    DAHUA = "Dahua Technology"
    DEDICATED_MICROS = "Dedicated Micros"
    DELL = "Dell"
    DIGI = "Digi"
    DISTECH = "Distech Controls"
    DLINK = "DLink"
    DRAYTEK = "DrayTek"
    DREAMBOX = "DreamBox"
    ECONET = "EcoNet"
    ECOSENSE = "EcoSense"
    EDGEWATER = "Edgewater Networks"
    EIQ = "eIQ"
    EMC = "EMC"
    EMERSON = "Emerson"
    ENTES = "Entes"
    ENTROLINK = "Entrolink"
    EPSON = "Epson"
    FACEXP = "FacExp"
    FIBERCOM = "Fiberhome Telecom Tech"
    FLEXIM = "Flexim"
    FULLRATE = "FullRate"
    HUAWEI = "Huwawei"
    HIKVISION = "Hikvision"
    HONEYWELL = "Honeywell"
    HP = "HP"
    IBM = "IBM"
    INTEG = "INTEG"
    INTEGRA = "Integra"
    INTELBRAS = "Intelbras"
    INTERCON = "Intercon"
    IPTIME = "IPTime"
    IQEYE = "IQeye"
    IXSYSTEM = "Ixsystem"
    JUNGO = "Jungo"
    KONICA_MINOLTA = "Konica Minolta"
    LAB_EL = "LAB-EL"
    LACIE = "LaCie"
    LANCOM = "Lancom Systems"
    LANTRONIX = "Lantronix"
    LEIGHTRONIX = "Leightronix"
    LENOVO = "Lenovo"
    LEXMARK = "Lexmark"
    LINKSYS = "Linksys"
    LIFESIZE = "LifeSize"
    LUTRON = "Lutron"
    MAYGION = "Maygion"
    MICROSOFT = "Microsoft"
    MIKROTIK = "MikroTik"
    MOTOROLA = "Motorola"
    MULTITECH = "Multitech"
    NATIONAL_INSTRUMENTS = "National Instruments"
    NETAPP = "Net App"
    NETGEAR = "NetGear"
    NETKLASS = "NetKlass"
    NEXREV = "NexRev"
    NGINX = "Nginx"
    NIVUS = "Nivus"
    NOVAR = "Novar"
    OPTO22 = "Opto22"
    OSNEXUS = "Osnexus"
    OVERLAND_STORAGE = "Overland Storage"
    PANABIT = "Panabit"
    PANASONIC = "Panasonic"
    PANO_LOGIC = "Pano Logic"
    POLABS = "PoLabs"
    POLABS = "PoLabs"
    POLYCOM = "Polycom"
    QNAP = "QNAP"
    RARITAN = "Raritan"
    REALTEK = "Realtek"
    RICOH = "Ricoh"
    ROCKWELL = "Rockwell Automation"
    ROUTER_BOARD = "routerboard"
    SANGFOR = "Sangfor"
    SCANNEX = "Scannex"
    SCHNEIDER = "Schneider Electric"
    SE_ELECTRONIC = "SE Electronic"
    SEAGATE = "Seagate"
    SENSATRONICS = "Sensatronics"
    SERCOMM = "Sercomm"
    SHARP = "Sharp"
    SIEMENS = "Siemens"
    SOFT_AT_HOME = "SoftAtHome"
    SOLAR_LOG = "Solar Log"
    SOMFY = "Somfy Systems"
    SONUS = "SONUS"
    SONY = "Sony"
    SPEEDPORT = "SpeedPort"
    SUN_MICROSYSTEMS = "Sun Microsystems"
    SUPERMICRO = "Super Micro Computer"
    SUPERMICROCOMPUTER = "Super Micro Computer"
    SYNOLOGY = "Synology"
    SYNCHRONIC = "Synchronic"
    TANDBERG_DATA = "Tandberg Data"
    TECHNICOLOR = "Technicolor"
    TELEMECANIQUE = "Telemecanique"
    TELRAD = "Telrad"
    THECUS = "Thecus"
    THINK_SIMPLE = "Think Simple"
    TIVO = "TiVo"
    TPLINK = "TP-LINK"
    TRANE = "Trane"
    TREND = "Trend"
    TRENDCHIP = "TrendChip"
    TRIDIUM = "Tridium"
    UBIQUITI = "Ubiquiti Networks"
    VARNISH = "Varnish"
    VERIS = "Veris Industries"
    VIA = "Via"
    VIRITA = "Virata"
    VODAPHONE = "VodaPhone"
    VYKON = "Vykon"
    WATTSTOPPER = "WattStopper"
    WD = "Western Digital"
    WEBEASY = "Webeasy"
    WEG = "WEG"
    WESTERN_DIGITAL = "Western Digital"
    WIND_RIVER = "Wind River"
    WURM = "Wurm"
    XEROX = "Xerox"
    ZTE = "ZTE"
    ZYXEL = "ZyXEL"
    ROOMWIZARD = "RoomWizard"


class OperatingSystem(object):
    # Linuxes
    ARCH = "Arch Linux"
    DEBIAN = "Debian"
    FEDORA = "Fedora"
    GENTOO = "Gentoo"
    KALI = "Kali Linux"
    MANDRIVE = "Mandriva"
    REDHAT = "RedHat"
    CENTOS = "CentOS"
    SUNOS = "SunOS"
    SUSE = "openSUSE"
    UBUNTU = "Ubuntu"
    UCLINUX = "uClinux"
    RASPBIAN = "Raspbian"
    # BSDs
    FREEBSD = "FreeBSD"
    NETBSD = "NetBSD"
    OPENBSD = "OpenBSD"
    SLACKWARE = "Slackware"
    # Other Unixes
    HPUX = "HP-UX"
    VXWORKS = "VXWORKS"
    # Windows
    WINDOWS = "Windows"
    WINDOWS_SERVER = "Windows Server"
    UCLINUX = "uClinux"
    TIMOS = "TiMOS"
    # RTOS's
    QNX = "QNX"
    # Router OSes
    CISCO_IOS = "Cisco IOS"
    MIKROTIK_ROUTER_OS = "MikroTik RouterOS"
    DOPRA = "Dopra Linux OS" # Huawei

class Annotation(object):

    LOCAL_METADATA_KEYS = [
        "manufacturer",
        "product",
        "version",
        "revision",
        "description"
    ]

    GLOBAL_METADATA_KEYS = [
        "manufacturer",
        "product",
        "version",
        "revision",
        "os",
        "os_version",
        "device_type",
        "description"
    ]

    port = None
    protocol = None
    subprotocol = None

    name = None

    tests = {}

    # some simple checks
    def check_port(self, port):
        return self.port is None or self.port == port

    def check_protocol(self, protocol):
        return self.protocol is None or self.protocol.value == protocol.value

    def check_subprotocol(self, subprotocol):
        return self.subprotocol is None or self.subprotocol.value == subprotocol.value

    @classmethod
    def iter(cls):
        for klass in cls.find_subclasses():
            if hasattr(klass, "process"):
                yield klass

    @classmethod
    def find_subclasses(cls):
        return set(cls.__subclasses__() + [g for s in cls.__subclasses__()
                                           for g in s.find_subclasses()])

    _annotation_annotations_total = 0
    _annotation_annotations_fail = 0
    @classmethod
    def load_annotations(cls, safe=False):
        def recursive_add(paths, prefix):
            for i, modname, ispkg in pkgutil.iter_modules(paths, prefix):
                if ispkg:
                    inner_paths = [os.path.join(paths[0], modname.split(".")[-1]),]
                    recursive_add(inner_paths, modname+".")
                else:
                    cls._annotation_annotations_total += 1
                    if safe:
                        try:
                            __import__(modname)
                        except:
                            cls._annotation_annotations_fail += 1
                            print "WARNING: unable to import %s" % modname
                    else:
                        __import__(modname)
        recursive_add(ztag.annotations.__path__, "ztag.annotations.")

    def simple_banner_version(self, b, server, meta):
        if b.lower().startswith(server.lower()):
           meta.local_metadata.product = server
           if "/" in b:
               meta.local_metadata.version = b.split("/", 1)[1].strip()
           return meta

    banner_re = re.compile(r"([\w\d_\.-]+)(?:/([\w\d_\.-]+))?(?: \(([\w\d_\.-]+)\))?")
    def http_banner_parse(self, b, meta):
        g = self.banner_re.search(b).groups()
        if g[0]:
           meta.local_metadata.product = g[0]
           meta.local_metadata.version = g[1]
           meta.global_metadata.os = g[2]
           return meta


class TLSTag(Annotation):

    @staticmethod
    def get_subject(d):
        return d["certificate"]["parsed"]["subject"]

    @staticmethod
    def get_sha256p(self, d):
        return d["certificate"]["parsed"]["fingerprint_sha256"]
