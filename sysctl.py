
class sysctl:
    def read(self, key):
        try:
            f = open("/proc/sys/%s" % key.replace(".", "/"))
        except:
            return None
        value = f.readline().strip()
        f.close()
        return value
