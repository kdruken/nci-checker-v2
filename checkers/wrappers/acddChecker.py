#!/usr/bin/env python
from netCDF4 import Dataset


class acddChecker:

    def __init__(self, path):
        self.path = path
        self.acdd = {'required': dict.fromkeys(req(), 0),
                     'recommended': dict.fromkeys(rec(), 0),
                     'suggested': dict.fromkeys(sug(), 0),
                     'additional_metadata': None,
                    }


    def check(self):
         with Dataset(self.path) as ds:
            ncattrs = ds.ncattrs()

            # Check for ACDD fields but record all global attributes even those not part of ACDD
            for item in req():
                if item in ncattrs:
                    self.acdd['required'][item] += 1
                    ncattrs.remove(item)

            for item in rec():
                if item in ncattrs:
                    self.acdd['recommended'][item] += 1
                    ncattrs.remove(item)

            for item in sug():
                if item in ncattrs:
                    self.acdd['suggested'][item] += 1
                    ncattrs.remove(item)

            self.acdd['additional_metadata'] = dict.fromkeys(ncattrs, 1)



'''_____________ ACDD Metadata Dictionary _____________'''

def req():
    return [
        'title',
        'summary',
        'source',
        'date_created',
        ]

def rec():
    return [
        'Conventions',
        'metadata_link',
        'history',
        'doi',
        'institution',
        'license',
        'processing_level',
        'project',
        'instrument',
        'platform',
        'product_version'
        ]

def sug():
    return [
        'date_modified',
        'date_issued',
        'references',
        'id',
        'keywords',
        'keywords_vocabulary',
        'geospatial_lat_min',
        'geospatial_lon_min',
        'geospatial_lat_max',
        'geospatial_lon_max',
        'geospatial_vertical_min',
        'geospatial_vertical_max',
        'geospatial_vertical_positive',
        'geospatial_bounds',
        'geospatial_bounds_crs',
        'geospatial_bounds_vertical_crs',
        'time_coverage_start',
        'time_coverage_end',
        'time_coverage_duration',
        'time_coverage_resolution',
        'geospatial_bounds',
        'geospatial_bounds_crs',
        'geospatial_bounds_vertical_crs',
        'geospatial_lat_units',
        'geospatial_lon_units',
        'geospatial_vertical_units',
        'geospatial_lat_resolution',
        'geospatial_lon_resolution',
        'geospatial_vertical_resolution',
        ]


