#!/usr/bin/env python3

import inspect

def notPrivate(func) -> bool:
    if inspect.isfunction(func):
        if func.__name__[0] != "_" :
            return True

    return False

def getPublicMembers(obj) -> tuple:
    return inspect.getmembers(obj, notPrivate)