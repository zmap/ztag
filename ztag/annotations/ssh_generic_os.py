import re
from ztag.annotation import Annotation
from ztag.annotation import OperatingSystem
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test

class SSHGenericOS(Annotation):

    protocol = protocols.SSH
    subprotocol = protocols.SSH.V2
    port = None

    tests = {
      "raspbian":{
        "global_metadata":{
          "os":OperatingSystem.RASPBIAN,
          "os_version":"5+deb8u3",
          "product":"Raspberry Pi",
        },
        "tags":["embedded","raspberry pi"]
      }
    }

    def process(self, obj, meta):
        software = obj["banner"]["software"].lower()
        comment = obj["banner"]["comment"].lower()
        # OS
        if "ubuntu" in comment:
            meta.global_metadata.os = OperatingSystem.UBUNTU
            # note: there's a real Ubuntu tag as well that will parse out Ubuntu
            # version and OpenSSH version
        elif "debian" in comment:
            meta.global_metadata.os = OperatingSystem.DEBIAN
        elif "freebsd" in comment:
            meta.global_metadata.os = OperatingSystem.FREEBSD
        elif "netbsd" in comment:
            meta.global_metadata.os = OperatingSystem.NETBSD
        elif "raspbian" in comment:
            meta.global_metadata.os = OperatingSystem.RASPBIAN
            meta.global_metadata.product = "Raspberry Pi"
            meta.tags.add("embedded")
            meta.tags.add("raspberry pi")
            if "-" in comment:
                meta.global_metadata.os_version = comment.split("-")[1]
        elif "bitvise" in comment:
            meta.global_metadata.os = OperatingSystem.WINDOWS
        elif "windows" in comment:
            meta.global_metadata.os = OperatingSystem.WINDOWS
        elif "centos" in comment:
            meta.global_metadata.os = OperatingSystem.CENTOS
        elif "rhel" in comment:
            meta.global_metadata.os = OperatingSystem.REDHAT
        #elif comment == "SSH server".lower():
            # this is xytel just ignore it. it'll get caught in GenericSoftware
        elif comment == "Microsoft FTP Service".lower():
            meta.global_metadata.os = OperatingSystem.WINDOWS
        return meta



class SSHGenericSoftware(Annotation):

    protocol = protocols.SSH
    subprotocol = protocols.SSH.V2
    port = None

    def process(self, obj, meta):
        s = obj["banner"]["software"].strip()
        s_l = s.lower()

        if s_l.startswith("openssh"):
            meta.local_metadata.product = "OpenSSH"
            if "_" in s:
                meta.local_metadata.version = s.split("_")[1]

        elif s_l.startswith("dropbear"):
            meta.local_metadata.product = "Dropbear SSH"
            meta.tags.add("embedded")
            if "_" in s:
                meta.local_metadata.version = s.split("_")[1]

        elif s == "ROSSSH":
            meta.local_metadata.product = "RouterOS SSH"
            meta.global_metadata.manufacturer = Manufacturer.MIKROTIK
            meta.global_metadata.device_type = Type.NETWORK
            meta.global_metadata.os = OperatingSystem.MIKROTIK_ROUTER_OS
            meta.tags.add("embedded")

        elif s_l.startswith("cisco"):
            meta.global_metadata.manufacturer = Manufacturer.CISCO
            meta.global_metadata.device_type = Type.INFRASTRUCTURE_ROUTER
            meta.global_metadata.os = OperatingSystem.CISCO_IOS
            meta.local_metadata.product = OperatingSystem.CISCO_IOS
            if "-" in s:
                meta.local_metadata.version = s.split("-")[1]
            meta.tags.add("embedded")

        elif s_l.startswith("huawei"):
            meta.local_metadata.product = "Huawei SSH"
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            if "-" in s:
                # handle HUAWEI-VRP-3.10
                meta.local_metadata.version = s.split("-")[-1]
            meta.tags.add("embedded")

        elif s_l.startswith("lancom"):
            meta.global_metadata.manufacturer = Manufacturer.LANCOM
            meta.global_metadata.device_type = Type.NETWORK
            meta.local_metadata.product = "Lancom SSH"
            meta.tags.add("embedded")

        elif s == "DOPRA-1.5":
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            meta.global_metadata.os = OperatingSystem.DOPRA
            meta.local_metadata.product = "DOPRA"
            meta.local_metadata.version = "1.5"
            meta.tags.add("embedded")

        elif s == "Zyxel":
            meta.global_metadata.manufacturer = "Zyxel"
            meta.local_metadata.product = "Zyxel"
            meta.tags.add("embedded")

        elif s_l.startswith("mod_sftp"):
            meta.local_metadata.product = "mod_sftp"
            if "/" in s:
                meta.local_metadata.version = s.split("/")[-1]

        elif s.startswith("RomSShell"):
            meta.local_metadata.product = "RomSShell"
            if "_" in s:
                meta.local_metadata.version = s.split("_")[-1]
            meta.global_metadata.manufacturer = "Allegro Software"
            meta.tags.add("embedded")

        elif s.startswith("mpSSH"):
            meta.local_metadata.manufacturer = Manufacturer.HP
            meta.local_metadata.product = "mpSSH"
            if "_" in s:
                meta.local_metadata.version = s.split("_")[-1]
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.product = "Integrated Lights Out (iLO)"
            meta.global_metadata.device_type = Type.SERVER_MANAGEMENT
            meta.tags.add("embedded")
            meta.tags.add("data center")

        elif "_" in s:
            # there are lots of semi-parsable things out there in the long tail
            # let's try to parse some of them out
            sp = s.split("_")
            v = sp[-1]
            p = " ".join(sp[:-1])
            meta.local_metadata.product = p
            meta.local_metadata.version = v

        return meta
