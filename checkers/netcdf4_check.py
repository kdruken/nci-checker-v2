#!/usr/bin/env python
from checkers.check import Checker
from checkers.wrappers.netcdf4Checker import netcdf4Checker
import netCDF4


class NetCDF4Checker(Checker):
    #
    #
    def __init__(self, path):
        Checker.__init__(self, path)
        self.type = "netCDF4-python {}".format(netCDF4.__version__)

    def check(self):
        try:
            meta = netcdf4Checker(self.path)
            meta.check()
            self.result = meta.meta
            self.score = True
        except:
            self.score = False

        return self.dict