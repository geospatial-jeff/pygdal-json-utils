import unittest
import os
import gdaljson
from osgeo import gdal

import gdaljson_utils as util
from tests.validate_cog import validate

from contextlib import contextmanager

class UtilTests(unittest.TestCase):

    def setUp(self):
        self.warpedvrt = os.path.join(os.path.split(__file__)[0], "templates/warped.vrt")
        self.translatevrt = os.path.join(os.path.split(__file__)[0], "templates/translate.vrt")

    @contextmanager
    def open_vrt(self, fpath):
        """Method to open a VRT with context"""
        vrtfile = open(fpath)
        if "warped" in fpath:
            vrt = gdaljson.VRTWarpedDataset(vrtfile.read())
        else:
            vrt = gdaljson.VRTDataset(vrtfile.read())
        vrt.filename = os.path.join(
            os.path.split(__file__)[0], "templates", vrt.filename)
        yield vrt
        vrtfile.close()

    def test_to_gdal(self):
        with self.open_vrt(self.translatevrt) as vrt:
            out_ds = util.to_gdal(vrt)
            self.assertEqual(type(out_ds), gdal.Dataset)
            self.assertEqual(out_ds.GetDriver().ShortName, 'VRT')

    def test_to_file(self):
        with self.open_vrt(self.warpedvrt) as vrt:
            util.to_file(vrt, '/vsimem/output.tif')
            out_ds = gdal.Open('/vsimem/output.tif')
            self.assertEqual(type(out_ds), gdal.Dataset)
            self.assertEqual(out_ds.GetDriver().ShortName, 'GTiff')

    def test_to_cog(self):
        with self.open_vrt(self.translatevrt) as vrt:
            util.to_file(vrt, '/vsimem/cog.tif', profile=util.COG)
            cog_ds = gdal.Open('/vsimem/cog.tif')
            self.assertEqual(type(cog_ds), gdal.Dataset)
            res = validate(cog_ds)
            self.assertEqual(len(res[0]), 0)