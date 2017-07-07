Schopenhauer.py
===================
Python3 script to check if SSH server is hardened.

API
-------------
sshd_parser.py have a SSHConf class. It is the parser of the conf of sshd, that have to be str object. sshd configuration could be obtained by runin: "sshd -T".

class SSHConf(conf)
SSHConf.conf: A list with option-value key pairs. Example: ['port', '6544'] or ['rekeylimit', '0 0']. Note that if value of option is multiple words space separed, it will be a uniq string, containing spaces.
__getitem__(self, x): SSHConf object can be trated as dict. Example:
>>> a['port']
'22312'

