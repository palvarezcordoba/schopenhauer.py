#!/usr/bin/env python3

import logging
import psutil
import helpers


CHECKER_NAME = "MOUNT"
logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class MountCheck:

    def __init__(self):
        self._partitions = psutil.disk_partitions(all=True)

    def tmp(self):
        for i in self._partitions:
            if i[1] == "/tmp":
                if not "noexec" in i[3] or "nosuid" not in i[3] \
                        or "nodev" not in i[3]:
                    log.error("/tmp mountpoint should have noexec, nosuid and"
                              " nodev options.")
                    return
        log.error(
            "/tmp should be separated and have noexec, nosuid and nodev options.")

    def home(self):
        for i in self._partitions:
            if i[1] == "/home":
                return
        log.error("/home should be separated.")

    def tmpfs(self):
        for i in self._partitions:
            if i[0] == "tmpfs":
                if "nosuid" not in i[3] or "nodev" not in i[3]:
                    log.error(
                        "{} should have nosuid and nodev options.".format(i[1]))

    def usage(self):
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition[1])[-1]
            if usage >= 90:
                log.error("Usage of {}: {}%".format(partition[1], usage))


def run():
    checker = MountCheck()

    c = helpers.getCheckers(MountCheck, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
