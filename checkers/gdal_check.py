#!/usr/bin/env python
from checkers.check import Checker
from osgeo import gdal


class GDALChecker(Checker):

    def __init__(self, path):
        Checker.__init__(self, path)
        self.type = "GDAL {}".format(gdal.__version__)

    def check(self):
        try:
            ds = gdal.Open(self.path)
            if ds == None or ds.GetProjection() == "" or ds.GetGeoTransform() == "":
                self.score = "FAIL"
            else:
                self.result = True
                self.score = "PASS"

        except:
            self.score = "FAIL"

        return self.dict





