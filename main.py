#!/usr/bin/env python3

import sys
import os
import logging

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger("MAIN")

sys.path.append("checkers")
checkers = []
for m in os.scandir("checkers"):
	if m.is_file():
		checkers.append(__import__(m.name[:-3]))
for c in checkers:
	try:
		c.run()
	except BaseException as e:
		log.name = c.CHECKER_NAME
		log.error(e)