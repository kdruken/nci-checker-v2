#!/usr/bin/env python
from checkers.check import Checker
from checkers.wrappers.cfwrapper import cfwrapper
import numpy as np


class CFChecker(Checker):
    #  This is the NCI cfchecks wrapper. The following script will call 'cfchecks.py'
    #  and then parse output to save as python dictionary for use with further checks.
    #
    #
    def __init__(self, path):
        Checker.__init__(self, path)
        self.type = "cfchecker {}".format('v2.0.9')

    def check(self):
        cfcheck = cfwrapper(self.path)
        cfcheck.check()
        self.result = cfcheck.cf
        if self.result == None:
            self.score = False
        else:
            self.score = 0
            for var, values in cfcheck.cf.items():
                self.score += values['score']
            self.score = self.score/len(cfcheck.cf.items())*100


        return self.dict