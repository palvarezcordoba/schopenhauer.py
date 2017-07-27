import os
import logging

import helpers

CHECKER_NAME = "COREDUMP"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class CoreDump:

    def check_core_dump(self):
        if os.popen("ulimit -c").read() != "0\n":
            log.error(
                "It's recomended to disable core dumps to avoid information leakeage")


def makes_sense() -> bool:
    return True


def run():
    checker = CoreDump()
    c = helpers.getCheckers(CoreDump, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
