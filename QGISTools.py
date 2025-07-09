# authors:
# David Hernandez Lopez, david.hernandez@uclm.es

import os, sys
from osgeo import gdal, osr, ogr

current_path = os.path.dirname(__file__)
sys.path.append(os.path.join(current_path, '..'))

from qgis.core import (QgsApplication, QgsDataSourceUri, QgsProject,
                       QgsCoordinateReferenceSystem, QgsCoordinateTransform)
from qgis.core import (QgsProject, QgsVectorLayer, QgsRasterLayer, QgsSymbol, QgsRendererCategory,
                       QgsCategorizedSymbolRenderer, QgsWkbTypes)
from qgis.core import QgsField, QgsFeature, QgsPoint, QgsGeometry
from qgis import utils
from qgis.core import Qgis

from . import defs_qgis

from pyLibCRSs import CRSsDefines as defs_crs
from pyLibCRSs.CRSsTools import CRSsTools
from pyLibGDAL import defs_gdal
from pyLibGDAL.GDALTools import GDALTools


class QGISTools(object):
    is_initialized = False

    @classmethod
    def get_vector_layers(self, layer_geometry_ogr_wkb_type):
        str_error = ''
        layers_by_name = {}
        if not isinstance(layer_geometry_ogr_wkb_type, list):
            str_error = ('Parameter layer_geometry_ogr_wkb_type must be a list and is: {}'
                         .format(str(type(layer_geometry_ogr_wkb_type))))
            return str_error, layers_by_name
        for layer in QgsProject.instance().mapLayers().values():
            layer_name = layer.name()
            if isinstance(layer, QgsVectorLayer):
                layer_geometry_qgs_wkb_type = layer.wkbType()
                if layer_geometry_qgs_wkb_type in layer_geometry_ogr_wkb_type:
                    layers_by_name[layer_name] = layer
                # layer_geometry_qgs_wkb_type_ = layer.geometryType()
                # layer_geometry_qgs_string = QgsWkbTypes.displayString(layer_geometry_qgs_wkb_type).lower()
                # geometry_is_valid = False
                # for i in range(len(layer_geometry_ogr_wkb_type)):
                #     ogr_wkb_type = layer_geometry_ogr_wkb_type[i]
                #     ogr_wkb_type_string = (ogr.Geometry(ogr_wkb_type)).GetGeometryName().lower()
                #     if layer_geometry_qgs_string in ogr_wkb_type_string:
                #         geometry_is_valid = True
                #         break
                # if geometry_is_valid:
                #     layers_by_name[layer_name] = layer
            if isinstance(layer, QgsRasterLayer):
                yo = 1
        return str_error, layers_by_name

    @classmethod
    def get_vector_layer_field_names(self, layer):
        str_error = ''
        field_names = layer.fields().names()
        return str_error, field_names

    @classmethod
    def initialize(self, iface):
        is_initalized = True
