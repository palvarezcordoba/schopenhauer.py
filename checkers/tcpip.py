import logging
import helpers
from sysctl import sysctl

CHECKER_NAME = "TCP/IP"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class TCPIP:

    def __init__(self):
        self.sysctl = sysctl()

    def syncCookies(self):
        if not int(self.sysctl.read("net.ipv4.tcp_syncookies")):
            log.error("Enable net.ipv4.tcp_syncookies.")

    def rfc1337(self):
        if not int(self.sysctl.read("net.ipv4.tcp_rfc1337")):
            log.error("Enable net.ipv4.tcp_rfc1337.")

    def rpFilter(self):
        if not int(self.sysctl.read("net.ipv4.conf.default.rp_filter")) \
                or not int(self.sysctl.read("net.ipv4.conf.all.rp_filter")):
            log.error(
                "Enable net.ipv4.conf.default.rp_filter and net.ipv4.conf.all.rp_filter.")

    def tcpTimestamps(self):
        if int(self.sysctl.read("net.ipv4.tcp_timestamps")):
            log.error("Disable net.ipv4.tcp_timestamps.")

    def logMartianPackets(self):
        if not int(self.sysctl.read("net.ipv4.conf.default.log_martians")) \
                or not int(self.sysctl.read("net.ipv4.conf.all.log_martians")):
            log.error(
                "Enable net.ipv4.conf.default.log_martians and net.ipv4.conf.all.log_martians.")

    def icmpIgnoreBroadcast(self):
        if not int(self.sysctl.read("net.ipv4.icmp_echo_ignore_broadcasts")):
            log.error("Enable net.ipv4.icmp_echo_ignore_broadcasts.")

    def ignoreBogus(self):
        if not int(self.sysctl.read("net.ipv4.icmp_ignore_bogus_error_responses")):
            log.error("Enable net.ipv4.icmp_ignore_bogus_error_responses.")


def makes_sense() -> bool:
    return True


def run():
    checker = TCPIP()

    c = helpers.getCheckers(TCPIP, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
