#!/usr/bin/env python3

#!/usr/bin/env python3

import os
import pwd
import spwd
import logging
import helpers

CHECKER_NAME = "USERS"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


# TODO: Check non-root users
class UsersCheck(object):
    def __init__(self):
        pass

    def checkUid(self):
        for u in pwd.getpwall():
            if u.pw_uid == 0 and u.pw_name != "root":
                log.error("There is a user with uid = 0 which is not root")

    def checkExpiration(self):
        d = spwd.getspnam("root")
        if d.sp_expire == -1:
            log.error("Enable expiration of users")


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
