#!/usr/bin/env python3

import logging
import optparse
import os.path
import platform
import gzip

import helpers


CHECKER_NAME = "KERNEL"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)

report = helpers.Report(CHECKER_NAME)

parser = helpers.Parser()
parser.add_option("--ck", default="", type="string")
args = parser.parse_args()[0]


class KernelCheck:

    def __init__(self, config):
        if not config:
            raise Exception("Kernel configuration not found.")

        if config.endswith(".gz"):
            with gzip.open(config) as f:
                self._config_file = f.readlines()
        else:
            with open(config) as f:
                self._config_file = f.readlines()

    def _isYes(self, opt):
        for l in self._config_file:
            if l.strip() == "CONFIG_{}=y".format(opt):
                return True

        return False
    
    def heapRandomization(self):
        if self._isYes("COMPAT_BRK"):
            report.new_issue("Heap randomization is disabled. Enable it")

    def stackProtector(self):
        if self._isYes("CC_STACKPROTECTOR_NONE"):
            report.new_issue("Stack protector is completely disabled. Enable it")

    def legacyvsyscall(self):
        if not self._isYes("LEGACY_VSYSCALL_NONE"):
            report.new_issue("Disable legacy vsyscall table")

    def modifyTLD(self):
        if self._isYes("MODIFY_LDT_SYSCALL"):
            report.new_issue("Disable TLD modify feature")

    def dmesgRestricted(self):
        if not self._isYes("SECURITY_DMESG_RESTRICT"):
            report.new_issue("Restrict access to dmesg logs to avoid information leaks")

    def hardenedMemCopies(self):
        if not self._isYes("HARDENED_USERCOPY"):
            report.new_issue("Enable hardened memory copies to/from the kernel")

    def staticUsermodeHelper(self):
        if not self._isYes("STATIC_USERMODEHELPER"):
            report.new_issue("Enable static usermode helper.")

    def refcount(self):
        if not self._isYes("REFCOUNT_FULL"):
            report.new_issue("Enable full refcounting");


def get_config_file() -> str:
    # On some distros the config file can also be found on /usr/src/linux but as long as
    # we can not ensure it is the current config file is better to avoid
    # it.

    # In case that no config file is found we can try to dynamically test if some protections
    # are really enabled

    r = platform.release()
    m = platform.machine()
    f_list = ["/proc/config", "/proc/config.gz", "/boot/config-{}".format(r),
              "/etc/kernels/kernel-config-{}-{}".format(m, r)]

    if args:
        f_list.insert(0, args.ck)

    for f in f_list:
        if os.path.isfile(f):
            return f
        
def makes_sense() -> bool:
    return platform.system() == "Linux" and get_config_file() != None


def run():
    try:
        checker = KernelCheck(get_config_file())

        c = helpers.getCheckers(KernelCheck, CHECKER_NAME)
        for name in sorted(c):
            getattr(checker, name)()
    except Exception as ex:
        log.exception(ex)


if __name__ == "__main__":
    run()
