#!/usr/bin/env python

'''

Usage: python nci-checker.py <file> [--check <options>]

Options:

--help 		Print this usage message and exit
--check     Specify specific checkers (optional, default is all)


'''

import checkers
import sys, os
from datetime import datetime
import output



def main():
    start_time = datetime.now()

    path = []
    for item in sys.argv[1:]:
        if item in ['--help', '-help', '-h', '--h']:
            print __doc__
            sys.exit()
        if os.path.exists(item):
            path = item

    if not path:
        sys.exit('No file specified or path does not exist.')


    print 'Checking: ', path, '\n'

    checks = {
                'cf': checkers.CFChecker(path),
                'acdd': checkers.ACDDChecker(path),
                'gdal': checkers.GDALChecker(path),
                'h5': checkers.HDF5Checker(path),
                'meta': checkers.NetCDF4Checker(path),
                }

    for item in checks.keys():
        checks[item] = checks[item].check()

    out = output.Output(path, checks)

    if os.path.isfile(path):
        out.simple_report()
        out.single_file()
        out.to_screen()

    elif os.path.isdir(path):
        # launch batch script result = batch(xxxx)
        # print xxx

        pass




    # Display total duration for compliance check
    end_time = datetime.now()
    print "\n"*3
    print "Duration: {}".format(end_time - start_time)



if __name__ == "__main__":
    main()



