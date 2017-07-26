import logging
import os
import helpers

CHECKER_NAME = "USBGUARD"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class USBGuard:

    def checkUSBGuardIsInstalled(self):
        try:
            os.stat("/usr/bin/usbguard")
        except FileNotFoundError:
            log.error("usbguard is not installed.")


def makes_sense() -> bool:
    return True


def run():
    checker = USBGuard()

    c = helpers.getCheckers(USBGuard, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()

if __name__ == "__main__":
    run()
