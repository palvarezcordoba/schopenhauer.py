#!/usr/bin/env python3

import logging
import psutil
import helpers


CHECKER_NAME = "MOUNT"
logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)

report = helpers.Report(CHECKER_NAME)


class MountCheck:

    def __init__(self):
        self._partitions = psutil.disk_partitions(all=True)

    def tmp(self):
        for i in self._partitions:
            if i[1] == "/tmp":
                if not "noexec" in i[3] or "nosuid" not in i[3] \
                        or "nodev" not in i[3]:
                    report.new_issue("/tmp mountpoint should have noexec and nosuid options.")
                    return
        report.new_issue(
            "/tmp should be separated and have noexec, nosuid and nodev options.")

    def home(self):
        for i in self._partitions:
            if i[1] == "/home":
                return
        report.new_issue("/home should be separated.")

    def tmpfs(self):
        for i in self._partitions:
            if i[0] == "tmpfs" and i[0] != "/tmp":
                if "nosuid" not in i[3] or "nodev" not in i[3]:
                    report.new_issue(
                        "{} should have nosuid and nodev options.".format(i[1]))

    def usage(self):
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition[1])[-1]
            if usage >= 90:
                report.new_issue("Usage of {}: {}%".format(partition[1], usage))


def makes_sense() -> bool:
    return True


def run():
    checker = MountCheck()

    c = helpers.getCheckers(MountCheck, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
