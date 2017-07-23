#!/usr/bin/env python3

import platform

import psutil

import kernel_checker
import mounts_checker
import sshd_checker

if platform.system() == "Linux":
	kernel_checker.run();

mounts_checker.run();

for p in psutil.process_iter():
	if p.as_dict(attrs=["name"])["name"] == "sshd":
		sshd_checker.run();