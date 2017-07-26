#!/usr/bin/env python3

import sys
import os
import platform

sys.path.append("checkers")
checkers = []
for m in os.scandir("checkers"):
	if m.is_file():
		checkers.append(__import__(m.name[:-3]))
for c in checkers:
	c.run()