#!/usr/bin/env python3

import os
import logging

import iptc

import helpers


CHECKER_NAME = "IPTABLES"
logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class IptablesCheck:

    def __init__(self):
        count = 0
        t = iptc.Table(iptc.Table.FILTER)
        for c in t.chains:
            count += len(c.rules)

        if count == 0:
            self._used = False
        else:
            self._used = True

    def used(self):
        if not self._used:        
            log.error("Iptables are not used")


# return True if it the service/platform are found and it makes sense to run
def makes_sense() -> bool:
    try:
        os.stat("/sbin/iptables")
        return True
    except:
        return False


def run():
    checker = IptablesCheck()

    c = helpers.getCheckers(IptablesCheck, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
