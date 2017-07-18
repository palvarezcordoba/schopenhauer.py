#!/usr/bin/env python3

import logging

import psutil

import helpers

CHECKER_NAME = "MOUNT"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class MountCheck(object):

    def __init__(self):
        self._partitions = psutil.disk_partitions(all=True)

    def tmp(self):
        for i in self._partitions:
            if i[1] == "/tmp":
                if not "noexec" in i[3]:
                    log.error("/tmp mountpoint should have *noexec* option")
                    return
 
        log.error("/tmp should be separated and have *noexec* option")

if __name__ == "__main__":
    checker = MountCheck()
    config = helpers.Config(CHECKER_NAME, MountCheck)

    checkers = {}
    for m in helpers.getPublicMembers(MountCheck):
        name = m[0]
        if config.isEnabled(name):
            checkers[name] = m[1]

    for name in sorted(checkers):
        getattr(checker, name)()
