#!/usr/bin/env python3

#!/usr/bin/env python3

import pwd
import spwd
import os
import stat

import logging
import helpers

CHECKER_NAME = "USERS"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)

report = helpers.Report(CHECKER_NAME)


# TODO: Check non-root users
class UsersCheck(object):
    def __init__(self):
        pass

    def checkUid(self):
        for u in pwd.getpwall():
            if u.pw_uid == 0 and u.pw_name != "root":
                report.new_issue("There is a user with uid = 0 which is not root")

    def checkExpiration(self):
        d = spwd.getspnam("root")
        if d.sp_expire == -1:
            report.new_issue("Enable expiration of users")

    def umask(self):
        with os.popen("umask") as p:
            val = p.read()
        if val[1:] != "77":
            report.new_issue("umask should be more restrictive (ie: 077)")

    def check_home(self):
        root_home = os.stat("/root")
        users_homes = os.scandir("/home")
        if stat.filemode(root_home.st_mode)[-6:] != '------':
            report.new_issue("Wrong permissions of /root")
        for user_home in users_homes:
            if user_home.is_dir() and stat.filemode(os.stat(user_home.path).st_mode)[-6:] != "------":
                report.new_issue("Wrong permissions of {}".format(user_home.path))


def makes_sense() -> bool:
    return True


def run():
    #    if os.geteuid() != 0:

    #        log.error("UsersCheck will not executed."
    #        " It should be executed as root.")
    #        return
    checker = UsersCheck()
    c = helpers.getCheckers(UsersCheck, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()
