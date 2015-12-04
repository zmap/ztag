from ztag.annotation import *


class QNXFox(Annotation):

    port = None
    protocol = protocols.FOX
    subprotocol = protocols.FOX.DEVICE_ID

    tests = {
        "qnx_npm6": {
            "global_metadata": {
                "os": OperatingSystem.QNX,
            }
        }
    }

    def process(self, obj, meta):
        os_name = obj["os_name"]
        if os_name.lower().strip() == "qnx":
            meta.global_metadata.os = OperatingSystem.QNX
            return meta


class QNXNPMFox(Annotation):

    port = None
    protocol = protocols.FOX
    subprotocol = protocols.FOX.DEVICE_ID

    _prefixes = [
        ("qnx-npm2", "NPM2"),
        ("qnx-npm3", "NPM3"),
        ("qnx-npm6", "NPM6"),
    ]

    tests = {
        "qnx_npm6": {
            "global_metadata": {
                "os": OperatingSystem.QNX,
            },
            "tags": ["NPM", "NPM6"],
        }
    }

    def process(self, obj, meta):
        host_id = obj["host_id"].lower().strip()
        for prefix in self._prefixes:
            if host_id.lower().strip().startswith(prefix[0]):
                meta.global_metadata.os = OperatingSystem.QNX
                meta.tags.add("NPM")
                meta.tags.add(prefix[1])
                return meta


class QNXJACEFox(Annotation):

    port = None
    protocol = protocols.FOX
    subprotocol = protocols.FOX.DEVICE_ID

    _prefixes = [
        ("qnx-j402", "JACE-402"),
        ("qnx-j403", "JACE-403"),
        ("qnx-j404", "JACE-545"),
        ("qnx-jvln", "JACE-7"),
    ]

    tests = {
        "qnx_jace": {
            "global_metadata": {
                "os": OperatingSystem.QNX,
            },
            "tags": ["JACE", "JACE-7"],
        }
    }

    def process(self, obj, meta):
        host_id = obj["host_id"].lower().strip()
        for prefix in self._prefixes:
            if host_id.lower().strip().startswith(prefix[0]):
                meta.global_metadata.os = OperatingSystem.QNX
                meta.tags.add("JACE")
                meta.tags.add(prefix[1])
                return meta
