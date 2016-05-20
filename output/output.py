#!/usr/bin/env python

'''
-------------------------------------------------
@author: K. Druken- NCI (kelsey.druken@anu.edu.au


Prints all output from 'nci-checker.py'
-------------------------------------------------
'''

import os
import time
from operator import itemgetter

lw = 90 	# line width for printed dashed lines


class Output:

    def __init__(self, path, results):
        # Print results and logfiles into one output log
        workdir = os.path.dirname(os.path.abspath(__file__))
        timestr = time.strftime("%Y-%m-%d-%H%M%S")

        # # Output log
        # if os.path.isdir(path):
        #     name = path.split("/")
        #     fn_out = workdir+'/NCI-QC-Report_'+name[3]+'_'+name[-2]+'_'+timestr+'.log'
        # else:
        #     fn_out = workdir+'/NCI-QC-Report_'+timestr+'.log'

        self.fn_out = 'testlog.log'
        self.log = open(self.fn_out,'w')
        self.path = path
        self.results = results


        ## Print header
        print >>self.log, '_'*lw
        print >>self.log, 'NCI-CHECKER \n', 'v20160518 \n'
        print >>self.log, ''
        print >>self.log, 'PATH: ', self.path
        print >>self.log, 'Date: ', timestr
        print >>self.log, '\n'*2
        print >>self.log, 'The following report provides an overview of data compliance and functionality '
        print >>self.log, 'with Climate and Forecast (CF) Convention and Attribute Convention for Data'
        print >>self.log, 'Discovery (ACDD) standards as well as core tools/libraries (e.g., GDAL, netCDF4,'
        print >>self.log, 'python APIs).'
        print >>self.log, ''
        print >>self.log, 'For help with data compliance, refer to the following CF and ACDD guides:'
        print >>self.log, '\t http://cfconventions.org/documents.html '
        print >>self.log, '\t http://wiki.esipfed.org/index.php/Attribute_Convention_for_Data_Discovery_1-3 '
        print >>self.log, ' '
        print >>self.log, ' '
        print >>self.log, '_'*lw
        print >>self.log, '\n'*2




    def simple_report(self):

        print >>self.log, "-"*lw
        print >>self.log, "{:^{n}}".format("Results Overview", n=lw)
        print >>self.log, "-"*lw
        print >>self.log, " "

        print >>self.log, "{:^{n}}{:^{n}}".format("::CHECK::", "::SCORE::", n=lw/2)
        print >>self.log, ""
        for value in self.results.values():
            print >>self.log, "{:^{n}}{:^{n}}".format(value['type'], value['score'], n=lw/2)

        print >>self.log, "\n"*5



    def single_file(self):

            # CF Results
            print >>self.log, "-"*lw
            print >>self.log, "{:^{n}}".format("CF Checker Results", n=lw)
            print >>self.log, "-"*lw
            print >>self.log, ""
            print >>self.log, "{:^{m}}{:^{n}}{:^{p}}".format("::Variable::", "::Messages::", "::Score::", m=lw*2/6, n=lw*3/6, p=lw/6)
            print >>self.log, ""

            if isinstance(self.results['cf']['result'], dict):
                for var, items in self.results['cf']['result'].items():
                    print >>self.log, "{:^{m}}{:^{n}}{:^{p}.0%}".format(var, "", items['score'], m=lw*2/6, n=lw*3/6, p=lw/6)
                    if items['error']:
                        # print >>self.log, "{:^{m}}{:^{n}}{:^{p}.0%}".format(var, "", 0, m=lw*2/6, n=lw*3/6, p=lw/6)
                        for message in items['error']:
                            print >>self.log, "{:<{m}}{:<{n}}{:^{p}}".format("", message, "", m=lw*2/6, n=lw*3/6, p=lw/6)

                    if items['warning']:
                        # print >>self.log, "{:^{m}}{:^{n}}{:^{p}}".format(var, "", "-", m=lw*2/6, n=lw*3/6, p=lw/6)
                        for message in items['warning']:
                            print >>self.log, "{:<{m}}{:<{n}}{:^{p}}".format("", message, "", m=lw*2/6, n=lw*3/6, p=lw/6)

                    if items['info']:
                        # print >>self.log, "{:^{m}}{:^{n}}{:^{p}}".format(var, "", "-", m=lw*2/6, n=lw*3/6, p=lw/6)
                        for message in items['info']:
                            print >>self.log, "{:<{m}}{:<{n}}{:^{p}}".format("", message, "", m=lw*2/6, n=lw*3/6, p=lw/6)
                    print >>self.log, " "

            else:
                print >>self.log, "[Could not complete test.]"
                print >>self.log, "\n"*2



            ## ACDD Results
            print >>self.log, "-"*lw
            print >>self.log, "{:^{n}}".format("ACDD Results (NCI Modified)", n=lw)
            print >>self.log, "-"*lw
            print >>self.log, "{:{m}}{:<{n}}{:^{p}}".format("", "::Attribute::", "::Score::", m=10, n=lw/2, p=lw/3)

            # Required
            print >>self.log, "REQUIRED"
            for attr, count in sorted(self.results['acdd']['result']['required'].items(), key=itemgetter(1, 0), reverse=True):
                print >>self.log, "{:{m}}{:<{n}}{:^{p}.0%}".format("", attr, count, m=10, n=lw/2, p=lw/3)
            print >>self.log, ""

            # Recommended
            print >>self.log, "RECOMMENDED"
            for attr, count in sorted(self.results['acdd']['result']['recommended'].items(), key=itemgetter(1, 0), reverse=True):
                print >>self.log, "{:{m}}{:<{n}}{:^{p}.0%}".format("", attr, count, m=10, n=lw/2, p=lw/3)
            print >>self.log, ""

            # Suggested
            print >>self.log, "SUGGESTED"
            for attr, count in sorted(self.results['acdd']['result']['suggested'].items(), key=itemgetter(1, 0), reverse=True):
                print >>self.log, "{:{m}}{:<{n}}{:^{p}.0%}".format("", attr, count, m=10, n=lw/2, p=lw/3)
            print >>self.log, ""
            print >>self.log, "\n"*3

            ## Additional checks
            print >>self.log, "-"*lw
            print >>self.log, "{:^{n}}".format("Additional Metadata)", n=lw)
            print >>self.log, "-"*lw
            print >>self.log, "{:{m}}{:<{n}}{:^{p}}".format("", "::Attribute::", "::Score::", m=10, n=lw/2, p=lw/3)
            print >>self.log, ""
            for attr, count in sorted(self.results['acdd']['result']['additional_metadata'].items(), key=itemgetter(1, 0), reverse=True):
                print >>self.log, "{:{m}}{:<{n}}{:^{p}}".format("", attr, '-', m=10, n=lw/2, p=lw/3)
            print >>self.log, ""
            print >>self.log, "\n"*3


            ## NCI Additional NetCDF Info/Checks
            if isinstance(self.results['meta']['result'], dict):
                print >>self.log, "-"*lw
                print >>self.log, "{:^{n}}".format("Additional NetCDF Information)", n=lw)
                print >>self.log, "-"*lw
                print >>self.log, "{:{m}}{:<{n}}{:^{p}}".format("", "::Check::", "::Result::", m=10, n=lw/2, p=lw/3)
                print >>self.log, " "

                for check, value in self.results['meta']['result'].items():
                    print >>self.log, "{:{m}}{:<{n}}{:^{p}}".format("", check.capitalize(), value, m=10, n=lw/2, p=lw/3)


    def to_screen(self):
        self.log.close()
        os.system('cat '+ self.fn_out)



    ## batch checks, list distinct errors? use set to reduce?
    ## display similar list/score per section?




    # def new_section(self, check_name, version):
    #     print >>self.log, '-'*lw
    #     print >>self.log, 'CHECK NAME:: ', check_name
    #     print >>self.log, 'Version: ', version
