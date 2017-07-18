#!/usr/bin/env python3

import psutil

import helpers

class MountCheck(object):

	def __init__(self):
		pass

	def tmp(self):
		pass
		

if __name__ == "__main__":
    checker = MountCheck()
    config = helpers.Config("MOUNT", MountCheck)

    checkers = {}
    for m in helpers.getPublicMembers(MountCheck):
        name = m[0]
        if config.isEnabled(name):
            checkers[name] = m[1]

    for name in sorted(checkers):
        getattr(checker, name)()