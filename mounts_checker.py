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
                if not "noexec" in i[3]:
                    log.error("/tmp mountpoint should have *noexec* option")
                    return
 
        log.error("/tmp should be separated and have *noexec* option")


def run():
    checker = MountCheck()
    
    c = helpers.getCheckers(MountCheck, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()

if __name__ == "__main__":
	run()
