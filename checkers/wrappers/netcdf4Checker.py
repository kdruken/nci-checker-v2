#!/usr/bin/env python
from netCDF4 import Dataset


class netcdf4Checker:

    def __init__(self, path):
        self.path = path
        self.meta = {'format': None,
                     'conventions': None,
                     'coord_vars_defined': None,
                     'multiple_stdnames': None}


    def check(self):
        with Dataset(self.path) as ds:
            ncattrs = ds.ncattrs()

            # Read/output any conventions used (if any)
            for attr in ncattrs:
                if attr.lower() in ['convention', 'conventions']:
                    self.meta['conventions'] = ds.__dict__[attr]
                else:
                    self.meta['conventions'] = '(No conventions used)'


            # Record file format (i.e., netcdf3, netcdf4)
            self.meta['format'] = ds.file_format


            # Record whether coordinate variables defined
            i = 0
            for dim in ds.dimensions.keys():
                if dim in ds.variables.keys():
                    i += 1
            if i == len(ds.dimensions):
                self.meta['coord_vars_defined'] = True
            else:
                self.meta['coord_vars_defined'] = False


            # Record whether more than 1 standard name used (this causes WMS issues)
            stdnames = {}
            for variable in ds.variables.keys():
                if 'standard_name' in ds[variable].__dict__.keys():
                    value = ds[variable].__dict__['standard_name']
                    if value not in stdnames.keys():
                        stdnames[value] = 1
                        self.meta['multiple_stdnames'] = False
                    else:
                        self.meta['multiple_stdnames'] = True
                        break


if __name__ == "__main__":
    path = '/Users/kdruken/Downloads/IR_gravity_anomaly_Australia_V1.nc'
    meta = netcdf4Checker(path)
    meta.check()
    print meta.meta