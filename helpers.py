#!/usr/bin/env python3

import inspect

import yaml

def notPrivate(func) -> bool:
    if inspect.isfunction(func):
        if func.__name__[0] != "_" :
            return True

    return False

def getPublicMembers(obj) -> tuple:
    return inspect.getmembers(obj, notPrivate)


class Config(object):

    def __init__(self, name, obj):
        self._config_file = "/etc/schopenhauer.yaml"

        self._configuration = {}
        try:
            with open(self._config_file, "r") as f:
                self._configuration = yaml.load(f.read())
                self._configuration = self._configuration[name]
        except:
            with open(self._config_file, "w+") as f:
                self._configuration[name] = {}
                for m in getPublicMembers(obj):
                    self._configuration[name][m[0]] = True

                yaml.dump(self._configuration, f, default_flow_style=False)
                self._configuration = yaml.load(str(self._configuration))[name]

    def isEnabled(self, checker_str) -> bool:
        try:
            return self._configuration[checker_str]
        except Exception as ex:
            return True