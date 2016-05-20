#!/usr/bin/env python
import StringIO
import sys
from contextlib import contextmanager
from netCDF4 import Dataset
import checkers.cfchecks


#
# Needed for CF Convention cfchecker:
#
STANDARDNAME = 'http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml'
AREATYPES = 'http://cfconventions.org/Data/area-type-table/current/src/area-type-table.xml'
UDUNITS = '/Users/kdruken/anaconda/pkgs/udunits2-2.2.20-0/share/udunits/udunits2.xml'
version = checkers.cfchecks.CFVersion()


#
# Needed for redirecting output from CF Convention cfchecker:
#
@contextmanager
def stdout_redirector(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


class cfwrapper:
    def __init__(self, path):
        self.path = path
        with Dataset(path) as ds:
            self.vars = ds.variables.keys()
            self.vars.append('(global)')
            self.format = ds.file_format
        self.cf = dict.fromkeys(self.vars)


    def check(self):
        #
        # This part executes the checker part of cfchecks.py and redirects output using StringIO.
        #
        #
        output = StringIO.StringIO()
        inst = checkers.cfchecks.CFChecker(cfStandardNamesXML=STANDARDNAME,
                                           cfAreaTypesXML=AREATYPES,
                                           udunitsDat=UDUNITS,
                                           version=version)


        try:
            with stdout_redirector(output):
                inst.checker(self.path)
            # Store result ignoring the last 3 lines
            result = output.getvalue().splitlines()[:-3]
        except:
            result = None

        if result:
            # First parse to find the scanned variables and corresponding line number
            tmpstr = 'Checking variable: '
            index = [(0, '(global)')]
            for i, line in enumerate(result):
                if line.find(tmpstr) != -1:
                    index.append((i, line[len(tmpstr):]))
            # add index for end of file
            index.append((i, ''))

            # Parse and store these messages
            for i,(lnum, var) in enumerate(index[:-1]):
                self.cf[var] = {'error':[], 'warning':[], 'info':[], 'score':0}
                for line in result[lnum:index[i+1][0]]:

                    # Checking error messages
                    if line.find('ERROR') != -1:
                        if line.find('(9.5)') != -1:
                            # This error can sometimes appear at beginning or end of output, need special catch
                            self.cf['(global)']['error'].append(line)
                        else:
                            self.cf[var]['error'].append(line)

                    # Checking warning messages
                    if line.find('WARNING') != -1:
                        if line.find('(9.5)') != -1:
                            # This error can sometimes appear at beginning or end of output, need special catch
                            self.cf['(global)']['warning'].append(line)
                        else:
                            self.cf[var]['warning'].append(line)

                    # Checking info messages
                    if line.find('INFO') != -1:
                        self.cf[var]['info'].append(line)

            # Calculate score
            for key, value in self.cf.items():
                if not value['error']:
                    self.cf[key]['score'] = 100

        else:
            self.cf = None



