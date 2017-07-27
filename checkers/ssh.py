#!/usr/bin/env python3

import re
import logging
from os import popen, path
from sys import stderr

import helpers

CHECKER_NAME = "SSH"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class SSHConf(object):

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


class SSHCheck(object):

    def __init__(self):
        with popen("/usr/sbin/sshd -T 2>/dev/null") as p:
            sshd_config = p.read()
        self._sshd = SSHConf(sshd_config)

    def root(self):
        if self._sshd["permitrootlogin"] != "no":
            log.error("Disable root login.")

    def port(self):
        if self._sshd['port'] == '22':
            log.error("Port number should not be the default (22).")

    def logingracetime(self):
        if int(self._sshd["logingracetime"]) > 25:
            log.error(
                "LoginGraceTime is very high.")

    def passauthentication(self):
        if self._sshd["passwordauthentication"] == 'yes' or self._sshd["challengeresponseauthentication"] == 'yes':
            log.error("Disable keyboard-interactive and use ssh keys instead (or combine it, for example ssh keys + OTP codes). Make sure than PasswordAuthentication and ChallengeResponseAuthentication is both disabled.")

    def TFA(self):
        with open("/etc/pam.d/sshd", 'r') as f:
            sshd_pam = f.read()
        if not re.match("\s*auth\s*required\s*pam_google_authenticator.so*", sshd_pam):
            log.error("It is recommended use 2FA.")
            return 0
        opt_or_suff = re.match(
            "\s*auth\s*(optional|sufficient)\s*pam_google_authenticator.so*", sshd_pam)
        if opt_or_suff is not None:
            log.error(
                "Not use {} option in /etc/pam.d/sshd.".format(opt_or_suff.group()))

    def login_filter(self):
        if not ("allowusers" in self._sshd.getOptions()) or ("allowgroups" in self._sshd.getOptions()):
            log.error(
                "Filter users/groups with AllowUSers, and/or, AllowGroups.")

    def subsystem(self):
        if "subsystem" in self._sshd.getOptions():
            log.error("If you do not really need {} disable it.".format(
                self._sshd["subsystem"]))

    def algorithm(self):
        with open("algorithm_blacklist", 'r') as f:
            blacklist = f.readlines()
        for item in blacklist:
            item_cleared = item.split(' ', 1)
            for x in self._sshd.conf:
                if len(x) > 1:
                    if item_cleared[0] in x[1]:
                        log.error(
                            "{} - {}".format(item_cleared[0], item_cleared[1][:-1]))
                        break

    def fail2ban(self):
        if not path.exists("/usr/bin/fail2ban-server"):
            log.error("Fail2ban not installed.")


def makes_sense() -> bool:
    # TODO: Check if ssh is running
    return True


def run():
    checker = SSHCheck()

    c = helpers.getCheckers(SSHCheck, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
