
class sysctl:
    def read(self, key):
        with open("/proc/sys/%s" % key.replace(".", "/")) as f:
        	value = f.readline().strip()
        return value
