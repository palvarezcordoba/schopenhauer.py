#!/usr/bin/env python3

import re
import logging
from os import popen
from sys import stderr

logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname)s::%(name)s] %(message)s")


class SSHConf:

    def __init__(self, conf):
        self.conf = [x.split(' ', 1) for x in conf.rsplit('\n')]
        self.confdict = dict()
        for x in self.conf:
            try:
                if x[0] in self.confdict.keys():
                    self.confdict[x[0]] = (self.confdict[x[0]], x[1])
                else:
                    self.confdict.update({x[0]: x[1]})
            except:
                pass

    def __getitem__(self, x):
        return self.confdict[x]

    def getOptions(self):
        return self.confdict.keys()


class SSHCheck:

    def __init__(self):
        with popen("/usr/sbin/sshd -T") as p:
            sshd_config = p.read()
        self._sshd = SSHConf(sshd_config)
        self._log = logging.getLogger(self.__class__.__name__)

    def root(self):
        if self._sshd["permitrootlogin"] != "no":
            self._log.error(
                "No use root account.")

    def port(self):
        if self._sshd['port'] == '22':
            self._log.error("Port number should not be the default (22).")

    def logingracetime(self):
        if int(self._sshd["logingracetime"]) > 25:
            self._log.error(
                "LoginGraceTime is very high.")

    def passauthentication(self):
        if self._sshd["passwordauthentication"] == 'yes' or self._sshd["challengeresponseauthentication"] == 'yes':
            self._log.error("Disable keyboard-interactive and use ssh keys instead (or convine it, for example ssh keys + OTP codes). Make sure than PasswordAuthentication and ChallengeResponseAuthentication is both disabled.")

    def TFA(self):
        with open("/etc/pam.d/sshd", 'r') as f:
            sshd_pam = f.read()
        if re.match("\s*auth\s*required\s*pam_google_authenticator.so*", sshd_pam):
            self._log.error("It is recommended use 2FA.")
            return 0
        opt_or_suff = re.match(
            "\s*auth\s*(optional|sufficient)\s*pam_google_authenticator.so*", sshd_pam)
        if opt_or_suff is not None:
            self._log.error(
                "Not use {} option in /etc/pam.d/sshd.".format(opt_or_suff.group()))

    def login_filter(self):
        if (not "allowusers" in self._sshd.getOptions()) or (not "allowgroups" in self._sshd.getOptions()):
            self._log.error(
                "Filter users/groups with AllowUSers, and/or, AllowGroups.")

    def subsystem(self):
        if "subsystem" in self._sshd.getOptions():
            self._log.error("If you not really need {} disable it.".format(
                self._sshd["subsystem"]))


checker = SSHCheck()
__all__ = [checker.root, checker.port, checker.logingracetime,
           checker.passauthentication, checker.TFA, checker.login_filter,
           checker.subsystem]

[x() for x in __all__]
