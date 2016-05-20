#!/usr/bin/env python
import numpy as np

from checkers.check import Checker
from checkers.wrappers.acddChecker import acddChecker


class ACDDChecker(Checker):
    #  This is the NCI ACDD checker. It checks a subset of the full ACDD guide
    #  for 3 categories: (1) Required, (2) Recommended, and (3) Suggested
    #  attributes. The priority of some attributes have been modified to ensure
    #  optimal usage with NCI data services.
    #
    def __init__(self, path):
        Checker.__init__(self, path)
        self.type = "ACDD {}".format('v1.3')

    def check(self):
        try:
            acdd = acddChecker(self.path)
            acdd.check()
            self.result = acdd.acdd
            self.score = np.mean(acdd.acdd['required'].values())*100
        except:
            self.score = None

        return self.dict