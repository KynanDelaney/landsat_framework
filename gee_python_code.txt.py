# Import packages

import ee
import geopandas as gpd
import json
import wxee

# Authorise access to Google Earth Engine

ee.Authenticate()
ee.Initialize()
wxee.Initialize()

# Read in shapefile to denote Region of Interest

shapefile = gpd.read_file('/content/anbg_boundary.shp')
js = json.loads(shapefile.to_json())
roi = ee.Geometry(ee.FeatureCollection(js).geometry())

# Import the entire Landsat C2 T1 collection
# filterDate based on duration of mission
# filterBounds by ROI
# Select to retain only optical bands

l5 = (ee.ImageCollection('LANDSAT/LT05/C02/T1_L2').filterDate('1984-01-01', '2012-05-31')
      .filterBounds(roi)
      .select(['SR_B.']))

l7 = (ee.ImageCollection('LANDSAT/LE07/C02/T1_L2').filterDate('1999-05-01', '2023-09-30')
      .filterBounds(roi)
      .select(['SR_B.']))

l8 = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterDate('2013-03-01', '2023-09-30')
      .filterBounds(roi)
      .select(['SR_B.']))

l9 = (ee.ImageCollection('LANDSAT/LC09/C02/T1_L2').filterDate('2021-10-31', '2023-09-30')
      .filterBounds(roi)
      .select(['SR_B.']))

# Merge the collections

merged_collection = l5.merge(l7).merge(l8).merge(l9)

# Transform merged_collection into an array

merged_collection.wx.to_xarray()