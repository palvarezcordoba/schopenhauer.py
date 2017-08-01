#!/usr/bin/env python3

import sys
import os
import logging
import traceback

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(__name__)


sys.path.append("checkers")

def run():
    name = sys.argv[0].replace(".", " ").split()
    if len(name) > 1 and  name[1] != "py":
        c = __import__(name[1])
        if c.makes_sense():
            c.run()
    else:
        checkers = []
        for m in os.scandir("checkers"):
            if m.is_file() and m.name.endswith(".py"):
                checkers.append(__import__(m.name[:-3]))
        for c in checkers:
            try:
                if c.makes_sense():
                    c.run()
            except Exception as e:
                traceback.print_exc()
                log.error(e)
                break

if os.geteuid() != 0:
    log.error("I need to run as root")
else:
    run()
