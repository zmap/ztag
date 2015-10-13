from datetime import datetime


class Logger(object):

    FATAL = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5

    def __init__(self, f, log_level=3):
        level = int(log_level)
        if level < 0 or level > Logger.TRACE:
            raise Exception("Invalid Log Level %d" % level)
        self.f = f
        self.level = level

    @staticmethod
    def make_time():
        return Logger.format_time(datetime.now())

    @staticmethod
    def format_time(ts):
        ms_str = str(ts.microsecond / 1000)
        t = ''.join([ts.strftime("%b %d %H:%M:%S."), ms_str])
        return t

    @staticmethod
    def rfc_time_from_utc(ts):
        return ts.strftime("%Y-%m-%dT%H:%M:%S+0000")

    def fatal(self, msg):
        t = self.make_time()
        out = "%s [ERROR] %s: %s\n" % (t, "ztag", msg)
        self.f.write(out)
        self.f.flush()
        raise Exception("Fatal!")

    def error(self, msg):
        if self.level < Logger.ERROR:
            return
        t = self.make_time()
        out = "%s [ERROR] %s: %s\n" % (t, "ztag", msg)
        self.f.write(out)
        self.f.flush()

    def warn(self, msg):
        if self.level < Logger.WARN:
            return
        t = self.make_time()
        out = "%s [WARN] %s: %s\n" % (t, "ztag", msg)
        self.f.write(out)
        self.f.flush()

    def info(self, msg):
        if self.level < Logger.INFO:
            return
        t = self.make_time()
        out = "%s [INFO] %s: %s\n" % (t, "ztag", msg)
        self.f.write(out)
        self.f.flush()

    def debug(self, msg):
        if self.level < Logger.DEBUG:
            return
        t = self.make_time()
        out = "%s [DEBUG] %s: %s\n" % (t, "ztag", msg)
        self.f.write(out)
        self.f.flush()

    def trace(self, msg):
        if self.level < Logger.TRACE:
            return
        t = self.make_time()
        out = "%s [DEBUG] %s: %s\n" % (t, "ztag", msg)
        self.f.write(out)
        self.f.flush()
