#!/usr/bin/env python3

#!/usr/bin/env python3

import pwd
import logging

import helpers

CHECKER_NAME = "USERS"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class UsersCheck(object):

    def __init__(self):
        pass

    def checkUid(self):
        for u in pwd.getpwall():
            if u.pw_uid == 0 and u.pw_name != "root":
                log.error("There is a user with uid = 0 which is not root")



def run():
    checker = UsersCheck()
    
    c = helpers.getCheckers(UsersCheck, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()


if __name__ == "__main__":
    run()