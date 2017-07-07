#!/usr/bin/env python3

import sshd_parser
import re
from os import popen
from random import randint
from sys import stderr

with popen("/usr/sbin/sshd -T") as p:
    sshd_config = p.read()
sshd = sshd_parser.SSHConf(sshd_config)

def check_root():
    if sshd["permitrootlogin"] in ("yes", "prohibit-password", "without-password"):
        print("You should not use root account.", "Set PermitRootLogin to no please.", sep=' ')

def check_port():
    if sshd['port'] == '22':
        print("Port number should not be the default (22)", "Set Port to other please. For example: {}".format(randint(5000, 65535), sep=' '))

def check_logingracetime():
    if int(sshd["logingracetime"]) > 25:
        print("LoginGraceTime is very high, if you do not need so much, reduce the value of this variable.")

def check_passauthentication():
    if sshd["passwordauthentication"] == 'yes' or sshd["challengeresponseauthentication"] == 'yes':
        print("You should disable keyboard-interactive and use ssh keys instead (or convine it, for example ssh keys + OTP codes). Make sure than PasswordAuthentication and ChallengeResponseAuthentication is both disabled.")

def check_2fa():
    with open("/etc/pam.d/sshd", 'r') as f:
        sshd_pam = f.read()
    if re.match("\s*auth\s*required\s*pam_google_authenticator.so*", sshd_pam):
        print("It is recommended use 2FA.")
        return 0
    opt_or_suff = re.match("\s*auth\s*(optional|sufficient)\s*pam_google_authenticator.so*", sshd_pam)
    if opt_or_suff is not None:
        print("You should not use {} option in /etc/pam.d/sshd.".format(opt_or_suff.group()))

def login_filter():
    if (not "allowusers" in sshd.getOptions()) or (not "allowgroups" in sshd.getOptions()):
        print("Filter users/groups with AllowUSers, AllowGroups.")

def check_privilege_separation():
    if sshd["useprivilegeseparation"] != "sandbox":
        print("Please, use \"UsePrivilegeSeperation sandbox\" option.")

def check_subsystem():
    if "subsystem" in sshd.getOptions():
        print("If you not really need {} disable it.".format(sshd["subsystem"]))


__all__ = [check_root, check_port, check_logingracetime, check_passauthentication, check_2fa, login_filter, check_privilege_separation, check_subsystem]

[ x() for x in __all__]
