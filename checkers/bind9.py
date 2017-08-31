import os
import stat
import logging
import psutil
import grp

import helpers

CHECKER_NAME = "BIND9"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)

report = helpers.Report(CHECKER_NAME)


class Bind9:

    def checkUser(self):
        for process in psutil.process_iter():
            if process.name() == "named":
                if process.username() == "root":
                    report.new_issue("Run bind9 with non-root user.")

    def checkPerms(self):
        binddir = os.stat("/etc/bind")
        if binddir.st_uid != 0:
            report.new_issue("Owner of /etc/bind should be root.")
        if grp.getgrgid(binddir.st_gid).gr_name != "bind":
            report.new_issue("Group of /etc/bind should be bind.")
        perms = os.stat("/etc/bind")
        if stat.filemode(perms.st_mode)[-1] != "-":
            report.new_issue("Users should have not access to /etc/bind")

    def checkAllow(self):
        with open("/etc/bind/named.conf.options", 'r') as f:
            conf = f.read()
            if "allow-recursion" not in conf:
                report.new_issue(
                    "Use allow-recursion to restric recursive queries to trusted clients.")
            if "allow-query" not in conf:
                report.new_issue(
                    "Use allow-query to restric queries to trusted clients.")
            if "allow-transfer" not in conf:
                report.new_issue(
                    "Use allow-transfer to restirct zone transfer to trusted hosts.")


def makes_sense() -> bool:
    # We should extent the check to ensure that this is not another program
    # with the same name.
    for process in psutil.process_iter():
        if process.name() == "named":
            return True

    return False


def run():
    checker = Bind9()

    c = helpers.getCheckers(Bind9, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
