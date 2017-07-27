#!/usr/bin/env python3

import sys
import os
import logging
import traceback
import optparse

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(__name__)

parser = optparse.OptionParser()
parser.add_option("-c", default="/etc/schopenhauer.yaml", type="string")
parser.add_option("--ck", default="", type="string")
args = parser.parse_args()

sys.path.append("checkers")
checkers = []
for m in os.scandir("checkers"):
    if m.is_file() and m.name.endswith(".py"):
        checkers.append(__import__(m.name[:-3]))
for c in checkers:
    try:
        if c.makes_sense():
            c.run(args)
    except Exception as e:
        traceback.print_exc()
        log.error(e)
        break
