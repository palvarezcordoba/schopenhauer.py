#!/usr/bin/env python3

import optparse
import inspect
import yaml

class Parser(optparse.OptionParser):
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                optparse.OptionParser._process_args(self,largs,rargs,values)
            except (optparse.BadOptionError, optparse.AmbiguousOptionError) as e:
                largs.append(e.opt_str)

def notPrivate(func) -> bool:
    if inspect.isfunction(func):
        if func.__name__[0] != "_" :
            return True

    return False

def getPublicMembers(obj) -> tuple:
    return inspect.getmembers(obj, notPrivate)

def getCheckers(class_obj, name) -> dict:
    config = Config(name, class_obj)

    checkers = {}
    for m in getPublicMembers(class_obj):
        name = m[0]
        if config.isEnabled(name):
            checkers[name] = m[1]

    return checkers


class Config:
    def __init__(self, name, obj):
        self.parser = Parser()
        self.parser.add_option("-c", default="/etc/schopenhauer.yaml", type="string")
        #self.parser.add_option("--ck")
        self.options = self.parser.parse_args()[0]
        self._config_file = self.options.c
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
        except:
            return True
