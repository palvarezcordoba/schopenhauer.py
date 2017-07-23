#!/usr/bin/env python3

import logging
import os.path
import platform
import gzip

import helpers

CHECKER_NAME = "KERNEL"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class KernelCheck(object):

    def __init__(self):
        kernel_config_file = self._getConfigFile()
        if not kernel_config_file:
            log.error("Can not found kernel configuration file. These test will not run")
            return

        if kernel_config_file.endswith(".gz"):
            with gzip.open(kernel_config_file) as f:
                self._config_file = f.readlines()
        else:
            with open(kernel_config_file) as f:
                self._config_file = f.readlines()

    def _getConfigFile(self) -> str:
        # On some distros the config file can also be found on /usr/src/linux but as long as 
        # we can not ensure it is the current config file is better to avoid it.
        
        # In case that no config file is found we can try to dynamically test if some protections
        # are really enabled

        r = platform.release()
        m = platform.machine()
        f_list = ["/proc/config", "/proc/config.gz", "/boot/config-{}".format(r),
                  "/etc/kernels/kernel-config-{}-{}".format(m, r)]

        for f in f_list:
            if os.path.isfile(f):
                return f

    def _isYes(self, opt):
        for l in self._config_file:
            if l.strip() == "CONFIG_{}=y".format(opt):
                return True

        return False

    def heapRandomization(self):
        if self._isYes("COMPAT_BRK"):
            log.error("Heap randomization is disabled. Enable it")

    def stackProtector(self):
        if self._isYes("CC_STACKPROTECTOR_NONE"):
            log.error("Stack protector is completely disabled. Enable it")

    def legacyvsyscall(self):
        if not self._isYes("LEGACY_VSYSCALL_NONE"):
            log.error("Disable legacy vsyscall table")

    def modifyTLD(self):
        if self._isYes("MODIFY_LDT_SYSCALL"):
            log.error("Disable TLD modify feature")

    def restrictDmesg(self):
        if not self._isYes("SECURITY_DMESG_RESTRICT"):
            log.error("Restrict access to dmesg logs to avoid information leaks")

    def hardenedMemCopies(self):
        if not self._isYes("HARDENED_USERCOPY"):
            log.error("Enable hardened memory copies to/from the kernel")

    def staticUsermodeHelper(self):
        if not self._isYes("STATIC_USERMODEHELPER"):
            log.error("Enable static usermode helper.")

if __name__ == "__main__":
    checker = KernelCheck()

    c = helpers.getCheckers(KernelCheck, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()
