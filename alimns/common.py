import sys
import os
import time

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser


class MNSSampleCommon:

    @staticmethod
    def LoadConfig():
        cfg_fn = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/../mns.cfg")
        required_ops = [("Base", "AccessKeyId"), ("Base", "AccessKeySecret"), ("Base", "Endpoint")]
        optional_ops = [("Optional", "SecurityToken")]

        parser = ConfigParser.ConfigParser()
        parser.read(cfg_fn)
        for sec, op in required_ops:
            if not parser.has_option(sec, op):
                sys.stderr.write("ERROR: need (%s, %s) in %s.\n" % (sec, op, cfg_fn))
                sys.stderr.write("Read README to get help inforamtion.\n")
                sys.exit(1)

        accessKeyId = parser.get("Base", "AccessKeyId")
        accessKeySecret = parser.get("Base", "AccessKeySecret")
        endpoint = parser.get("Base", "Endpoint")
        securityToken = ""
        if parser.has_option("Optional", "SecurityToken") and parser.get("Optional",
                                                                         "SecurityToken") != "$SecurityToken":
            securityToken = parser.get("Optional", "SecurityToken")
            return accessKeyId, accessKeySecret, endpoint, securityToken

        return accessKeyId, accessKeySecret, endpoint, ""

    @staticmethod
    def LoadParam(params_num):
        if params_num < len(sys.argv):
            params = list()
            hasdecode = hasattr(sys.argv[1], 'decode')

            for p in sys.argv[1:params_num + 1]:
                if hasdecode:
                    params.append(p.decode('utf-8'))
                else:
                    params.append(p)

            return params_num, params
        else:
            return 0, None

    @staticmethod
    def LoadIndexParam(index):
        if index < len(sys.argv):
            if hasattr(sys.argv[1], 'decode'):
                return sys.argv[index].decode('utf-8')
            else:
                return sys.argv[index]
        else:
            return None
