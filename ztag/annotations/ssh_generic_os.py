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

    def process(self, obj, meta):
        software = obj["banner"]["software"].lower()
        comment = obj["banner"]["comment"].lower()
        # OS
        if "ubuntu" in comment:
            meta.global_metadata.os = OperatingSystem.UBUNTU
        elif "debian" in comment:
            meta.global_metadata.os = OperatingSystem.DEBIAN
        elif "freebsd" in comment:
            meta.global_metadata.os = OperatingSystem.FREEBSD
        elif "netbsd" in comment:
            meta.global_metadata.os = OperatingSystem.NETBSD
        elif "raspbian" in comment:
            meta.global_metadata.os = OperatingSystem.RASPBIAN
        elif "bitvise" in comment:
            meta.global_metadata.os = OperatingSystem.WINDOWS
        elif "windows" in comment:
            meta.global_metadata.os = OperatingSystem.WINDOWS
        elif "centos" in comment:
            meta.global_metadata.os = OperatingSystem.CENTOS
        elif "rhel" in comment:
            meta.global_metadata.os = OperatingSystem.REDHAT

        # software package
        if "openssh" in software:
            meta.local_metadata.product = "OpenSSH"
        elif "roshssh" in software:
            meta.local_metadata.product = "RouterOS SSH"
            meta.global_metadata.manufacturer = Manufacturer.MIKROTIK
            meta.global_metadata.device_type = Type.NETWORK
            meta.global_metadata.os = OperatingSystem.MIKROTIK_ROUTER_OS
        elif "dropbear" in comment or "dropbear" in software:
            # dropbox versions are generally of the following form: dropbear_2013.59
            # however, we'll also see dropbear_0.46 and even just "dropbear"
            meta.local_metadata.product = "Dropbear SSH"
            if "-" in comment:
                _, version = comment.split("-")
                meta.local_metadata.version = version
            meta.tags.add("embedded")
        elif "cisco" in comment:
            meta.global_metadata.manufacturer = Manufacturer.CISCO
            meta.global_metadata.device_type = Type.INFRASTRUCTURE_ROUTER
            meta.global_metadata.os = OperatingSystem.CISCO_IOS
            meta.local_metadata.product = OperatingSystem.CISCO_IOS
            if "-" in comment:
                version = comment.split("-")[1]
                meta.global_metadata.os_version = version
        elif "lancom" in comment:
            meta.global_metadata.manufacturer = Manufacturer.LANCOM
            meta.global_metadata.device_type = Type.NETWORK
        elif "dopra" in software:
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            meta.global_metadata.os = OperatingSystem.DOPRA
        elif "cryptlib" in comment:
            meta.local_metadata.product = "cryptlib"
        elif "globalscape" in comment:
            meta.local_metadata.product = "GlobalSCAPE SSH"
        elif "bitvise" in comment:
            meta.local_metadata.product = "Bitvise SSH Server"

        return meta
