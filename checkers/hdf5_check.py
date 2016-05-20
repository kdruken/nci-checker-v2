#!/usr/bin/env python
from checkers.check import Checker
import h5py


class HDF5Checker(Checker):

    def __init__(self, path):
        Checker.__init__(self, path)
        self.type = "h5py {}".format(h5py.__version__)

    def check(self):

        try:
            with h5py.File(self.path, 'r') as h5f:
                if h5f != None:
                    self.result = True
                    self.score = "PASS"
                else:
                    self.score = "FAIL"

        except:
            self.score = "FAIL"


        # return self.to_json()
        return self.dict