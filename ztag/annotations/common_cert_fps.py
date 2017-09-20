from ztag.annotation import *


class CommonCertificateFingerprints(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "huawei_38e5":{
        "global_metadata":{
          "manufacturer":Manufacturer.HUAWEI,
          "device_type":Type.MODEM,
          "product":"Home Gateway HG658d",
        },
        "tags":["embedded",]
      }
    }


    def process(self, obj, meta):
        fp = obj["certificate"]["parsed"]["fingerprint_sha256"]
        if fp == "6343022d4995a8d96f50a737e77fd5c0ab2efd842b5e05b1fd7109df426a38e5":
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            meta.global_metadata.product = "Home Gateway HG658d"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "d86ac7ac292a9bf702b90c0a6396df047d961e549331d802db22079f7a4d8b8e"
            meta.global_metadata.manufacturer = Manufacturer.DAHUA
            meta.tags.add("embedded")
            return meta
        elif fp == "96421eda0168df9a44c9eadc7451cae578f3c42456bbef5c5b33e1791b88d20c":
            meta.global_metadata.manufacturer = Manufacturer.MOTOROLA
            meta.global_metadata.product = "Cable Modem"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "1b9a783965a0fa8e5cee8b8e3d3f499b8163fe3a44bbcec3a52bbc0ecc1151d1":
            meta.global_metadata.manufacturer = Manufacturer.TECHNICOLOR
            meta.global_metadata.product = "Modem"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "ec3ae70631c7c30378189c73eef80aaaea6ca1d07793cc878422a77a656086e4":
            meta.tags.add("embedded")
            return meta
        elif fp == "cb36482dc97fe9dfafb4cc75d8f6bf2571a7c6d8bcc0716e6072c79576261f8a":
            # clearly some embedded device. not really sure what it is though
            # seeing a whole bunch of different devices showing up
            meta.tags.add("embedded")
            return meta
        elif fp == "464f4fcd90934c66b83509dffaa8993922520a7a14422853060a6a2c289d3ecb":
            meta.tags.add("embedded")
            return meta
        elif fp == "ef512d0ab19e9b91a5c519c634a4f2fcbbf65c45ef87e01aabd25939fe903594":
            meta.global_metadata.manufacturer = "T&W"
            meta.global_metadata.product = "GPON Home Gateway"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "949f373d9f1cf4d31cf2be16f67850795629b74f8b39c4622d6461326b4eaaa2":
            return
        elif fp == "d86ac7ac292a9bf702b90c0a6396df047d961e549331d802db22079f7a4d8b8e":
            meta.tags.add("embedded")
            return meta
        elif fp == "816735d1fd53b8747aa3a61e277dd8fd5dd303475bc9730ead8ad67155518e33":
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "e4d09f84810efa9ad8541b7a820f094408ef760744ffe44d397f88d28b441995":
            meta.global_metadata.manufacturer = Manufacturer.UBIQUITI
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta
        elif fp == "d6f2349d74e603c1713ea8ea6d998cbe0d0b972bd799521006c3f463ecd02abb"\
                or fp == "167390050a67bb785bb01b0934bcc57b4865593ae98b2f09a002e496a69cebde":
            meta.global_metadata.manufacturer = Manufacturer.ZYXEL
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "182034cb65b46a7a8563262995120630392b1f5d626133d961503056c1c72c1a"\
                or fp == "cdf555315a8ba0139e721d5b17cbee6599c42b52e4b8eb52f9237825b1e74f64"\
                or fp == "f617e883351ed4e69f23d155205d627808b4270948acf3012865104e726a2b1d ":
            meta.global_metadata.manufacturer = Manufacturer.DRAYTEK
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.global_metadata.product = "Vigor Router"
            meta.tags.add("embedded")
            return meta
        elif fp == "1f2f8b736aa3886fee322ad5ab96e8adcfb7cdfbcb61e4bfbab140fbdaedf666":
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            meta.global_metadata.product = "Home Gateway"
            meta.global_metadata.device_type = Type.DSL_MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "6cf53ed14fe53f7321940911dc93ff8dbe9d4b4116a6ed95b41fb60d834c8780":
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            meta.global_metadata.device_type = Type.MODEM
            meta.global_metadata.product = "Home Gateway"
            meta.tags.add("embedded")
            return meta
        elif fp == "6cf53ed14fe53f7321940911dc93ff8dbe9d4b4116a6ed95b41fb60d834c8780":
            meta.global_metadata.manufacturer = Manufacturer.TECHNICOLOR
            meta.global_metadata.product = "DPC3848 DOCSIS 3.0 Gateway"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "5da28495a5dfebf36ef25af9a6eb1a59faecdffbf7c6070c83cb91b7b3b2ced9":
            meta.global_metadata.device_type = Type.DVR
            meta.tags.add("embedded")
            return meta
        elif fp == "d5c0101d5ac007024e50477188b03d76f28112472edf56c5e19a76cf069008e7":
            meta.global_metadata.manufacturer = Manufacturer.MULTITECH
            meta.tags.add("embedded")
            return meta
        elif fp == "1ae9d62f5d127f9a361a1a04a75157e5a6d5cac36ed9d46e17c87ca641786d35":
            meta.global_metadata.manufacturer = "T&W"
            meta.global_metadata.product = "GPON Home Gateway"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "ef1fd069e6f4fa81e139cb39d0bb049cca48e49808a04193e4674667089d1343"\
                or fp == "d2a928e4d35aabd7f066cfcd93dd54c675ef3e0de8162708fc7adb6a7f161d88":
            meta.global_metadata.manufacturer = Manufacturer.QNAP
            meta.global_metadata.product = "Turbo NAS"
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta
        elif fp == "4f07b356d72f17774a8ae6ca9750a668e6f1ccf0d02d3fcb773eabff52daa349":
            meta.global_metadata.manufacturer = Manufacturer.QNAP
            meta.global_metadata.product = "TS Series NAS"
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta
        elif fp == "43f84ee7516b0f4e06e1186f498f4840ab832efd9ca6165b0b3c195756c85532":
            meta.global_metadata.manufacturer = Manufacturer.SERCOMM
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "298196fe226e52eae246c5a4c5943f2db3b6d931b1a16b2104d90c1dae3f0dad" or \
                fp == "339fc27ee4d32665424ce84d7f97b9ddc3059d5af9d1b6a47d041ac79f8af968" or \
                fp == "f3f519150cab4a01e9948435070e02baacc9d41b478c23ac1a5a884f1d7d06da" or \
                fp == "1b4da61347a18ff56290e547882c18c45e9da80d16f70b6af0b09cc4235b392a" or \
                fp == "059d6bdee15a6898c0e6f6d225327d6731796c189b9afdca445bf1122e1adc1b" or \
                fp == "be589d2ddff654b51de7024bc619f9bde5f4275300ec91d97b030a576b121c84":
            meta.global_metadata.manufacturer = Manufacturer.JUNGO
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "13657bfa2c9cdba7591f97675f203a8bad4ecbe3f70fbaccad43646dec3b600d":
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            meta.global_metadata.device_type = Type.MODEM
            meta.global_metadata.product = "Home Gateway"
            meta.tags.add("embedded")
            return meta
        elif fp == "3910dbb918c41fe7d5658214f034cb1d96fc35ba758c7bd7da97693326aeb308":
            meta.global_metadata.manufacturer = Manufacturer.INTELBRAS
            meta.global_metadata.product = "WOM 5000"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "0f1b486c96d6f1db6e5004a19482071ece5b8669069c8dd7f2239d8f732b6b72":
            meta.local_metadata.product = "Axentraserver"
            # NASes from a bunch of companies (at least seagate and netgear) seem
            # to use this server
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta
        elif fp == "738523c7102fdd44124bb4a36075adfcb35dceb1f947ea56ea2366192d9e6482":
            meta.global_metadata.manufacturer = Manufacturer.TELRAD
            meta.global_metadata.device_type = Type.WIRELESS_MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "577461369dbdebc7daea9701ecdd03297bc74d4ce3eece23ee3feb63613ab031":
            meta.global_metadata.manufacturer = Manufacturer.DELL
            meta.global_metadata.product = "Dell Integrated Remote Access"
            meta.global_metadata.vesion = "7"
            meta.global_metadata.device_type = Type.SERVER_MANAGEMENT
            meta.tags.add("embedded")
            meta.tags.add("idrac")
            return meta
        elif fp == "91c3d9de766dc7803dc6d90e5cc4e238ac2016fbfe7da105bcf2198ba2cee36b":
            meta.global_metadata.manufacturer = Manufacturer.ENTROLINK
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "016973380c0f1df00bd9593ed8d5efa3706cd6df7993f6141272b80522acdd23":
            meta.global_metadata.manufacturer = Manufacturer.ENTROLINK
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "04f527c0f12939feef1e5fa567d45115d4f856b9b5bd78bdc6698ef0b11dfa54":
            meta.global_metadata.manufacturer = Manufacturer.SOMFY
            meta.global_metadata.device_type = Type.ALARM_SYSTEM
            meta.tags.add("embedded")
            return meta
        elif fp == "59c2ba7edab4fbda1ad76801679f1d9f4d13aef4a5cc2499690436bab3f49776":
            meta.global_metadata.manufacturer = Manufacturer.TRENDCHIP
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "78fd13c7325a78b9600b589eef1cbca79d91fb93a50aa1e6339535aeb7c1c300":
            meta.global_metadata.manufacturer = Manufacturer.LINKSYS
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.tags.add("embedded")
            return meta
        elif fp == "d8fdf1ec100c1d5dd137ab579dafba0b58ccba5282652df5701877515b730041":
            meta.global_metadata.manufacturer = Manufacturer.SUPERMICRO
            meta.global_metadata.product = "Intelligent Management"
            meta.global_metadata.device_type = Type.IPMI
            meta.tags.add("embedded")
            meta.tags.add("data center")
            return meta
        elif fp == "5d1fc439c0625fa9333561907a6de4f53b058031224654407ff28a79fb8e75b6":
            meta.global_metadata.manufacturer = "Bouygues Telecom"
            meta.global_metadata.product = "Bbox"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "9de541b039cfdb96c7810df49efd958b28cc2df73e314f67c1a91469a2b19796":
            # apache default
            return
        elif fp == "50e98b5062bc67eee5e774c9d206495ca58ebbf8a879e092e7b4869dfa97721b":
            meta.global_metadata.manufacturer = Manufacturer.FIBERCOM
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "7299baad93d5da7ce2fb8c430fa88715b0799a302dbb84da1a803c5e0db1beb1":
            meta.global_metadata.manufacturer = Manufacturer.EDGEWATER
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta
        elif fp == "ef1798cfbf4e41e99381a31759173bdc412947b6dc9da4f69d0ccc9b1a16a9e9":
            meta.global_metadata.manufacturer = Manufacturer.REALTEK
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta
        elif fp == "d76133e1986c5aca8b45a2b99fd53c0045ccbc476e5971ea287644825a104688":
            meta.global_metadata.manufacturer = Manufacturer.ECONET
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "f42e36dae397d500ed6471fadfc0dab9571665ea53d058459c71a9154651a638":
            meta.global_metadata.manufacturer = Manufacturer.PANABIT
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta
        elif fp == "78a403d79d7f03fbf57aa6881787d1ebbc2121eb47fb56ae1a0c7cbedbf6b3a9":
            meta.global_metadata.manufacturer = Manufacturer.ZTE
            meta.global_metadata.product = "ZXV10"
            meta.global_metadata.device_type = Type.MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "47fa89956f2aa349e8814b21a7bbd64c9b597f0f192bfe073559945a7a846534":
            meta.global_metadata.manufacturer = Manufacturer.ARUBA
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta
        elif fp == "17f0fc61d684f8493f306b64aa913edfe68bc118f59534bba7d544799768783e":
            # I can't figure out what this is. I need someone who speaks Mandarin
            return
        elif fp == "5b9ab766e1b5dc504cfde9345294b99196b0b729e060e50162237c2daf0080bc":
            # always a camera, but tons of differnt manufacturers. must be some rebranding program
            meta.global_metadata.device_type = Type.CAMERA
            meta.tags.add("embedded")
            return meta
        elif fp == "94d4b664af7846fe3f715691f475fbcbb11c5a2b3762ee43b25edbdb86fc3c7f":
            meta.global_metadata.manufacturer = Manufacturer.NETGEAR
            meta.global_metadata.device_type = Type.FIREWALL
            meta.global_metadata.product = "ProSafe VPN Firewall"
            meta.tags.add("embedded")
            return meta
        elif fp == "96197cd06e4fc5ea57764cb79e85f34a5655f2e3426f70d06bebaa9f1093f407":
            meta.global_metadata.manufacturer = Manufacturer.HUAWEI
            meta.global_metadata.product = "Mobile Broadband"
            meta.global_metadata.device_type = Type.WIRELESS_MODEM
            meta.tags.add("embedded")
            return meta
        elif fp == "4403880b9cba3f740154a274418dc3435a5c1b57ca728b3387da568bacc803f1":
            meta.global_metadata.manufacturer = Manufacturer.ADTRAN
            meta.global_metadata.product = "NetVanta"
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta
        elif fp == "ce35990416909c04aafb7dfdb494dcdcc0a3757a4978ca04da41ce4c01567026":
            # can't figure out what this is. It supports SNMP though, so seems unlikely
            # that it's a home device
            meta.global_metadata.manufacturer = Manufacturer.MANUFACTURER
            meta.tags.add("data center")
            meta.tags.add("embedded")
        elif fp == "5b9ab766e1b5dc504cfde9345294b99196b0b729e060e50162237c2daf0080bc":
            # can't figure out what this is
            return
        elif fp == "d828f96059933ae11b895163742b35af7cda6d267f081b18e1e4157678a443dc":
            meta.global_metadata.manufacturer = Manufacturer.SANGFOR
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta
        elif fp == "2c773cea359829eec0cf172e1ac8a9219c94eddd5241ca7a4a9b07e0cabb010f":
            meta.global_metadata.manufacturer = Manufacturer.NETKLASS
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta

