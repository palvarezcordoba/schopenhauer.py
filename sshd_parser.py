#!/usr/bin/env python3

class SSHConf:
    def __init__(self, conf):
        self.conf = [ x.split(' ', 1) for x in conf.rsplit('\n')]
        self.confdict = dict()
        for x in self.conf:
            try:
                if x[0] in self.confdict.keys():
                    self.confdict[x[0]] =  (self.confdict[x[0]], x[1])
                else:
                    self.confdict.update({x[0]: x[1]})
            except:
                pass
    def __getitem__(self, x):
        return self.confdict[x]
