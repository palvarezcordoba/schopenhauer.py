import logging
import os
import helpers

CHECKER_NAME = "USBGUARD"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class USBGuard:
    
    def __init__(self, args):
        pass

    def checkUSBGuardIsInstalled(self):
        try:
            os.stat("/usr/bin/usbguard")
        except FileNotFoundError:
            log.error("usbguard is not installed.")


def makes_sense() -> bool:
    return True


def run(args=None):
    checker = USBGuard(args)

    c = helpers.getCheckers(USBGuard, CHECKER_NAME, args)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
