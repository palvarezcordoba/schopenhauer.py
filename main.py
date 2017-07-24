#!/usr/bin/env python3

import platform

import psutil

import mounts_checker
import users_checker
import kernel_checker
import sshd_checker

mounts_checker.run();
users_checker.run()

if platform.system() == "Linux":
	kernel_checker.run();


for p in psutil.process_iter():
	if p.as_dict(attrs=["name"])["name"] == "sshd":
		sshd_checker.run();