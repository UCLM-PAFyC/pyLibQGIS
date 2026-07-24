# authors:
# David Hernandez Lopez, david.hernandez@uclm.es

from qgis.core import (QgsProviderRegistry)
from qgis.core import (QgsProject, QgsVectorLayer, QgsRasterLayer)

class QGISTools(object):
    is_initialized = False

    @classmethod
    def get_layer_name(self, layer_name):
        str_error = ''
        uri_layer_name = ''
        layers = QgsProject.instance().mapLayersByName(layer_name)
        if layers:
            layer = layers[0]
            uri_components = QgsProviderRegistry.instance().decodeUri(layer.dataProvider().name(),
                                                                      layer.publicSource())
            if 'layerName' in uri_components:
                uri_layer_name = uri_components['layerName'] # no for raster wfs?, ...
            # file_path = layer.dataProvider().dataSourceUri()
        else:
            str_error = ('Not exists layer: {}'.format(layer_name))
            return str_error, uri_layer_name
        return str_error, uri_layer_name

    @classmethod
    def get_file_path(self, layer_name):
        str_error = ''
        file_path = ''
        layers = QgsProject.instance().mapLayersByName(layer_name)
        if layers:
            layer = layers[0]
            uri_components = QgsProviderRegistry.instance().decodeUri(layer.dataProvider().name(),
                                                                      layer.publicSource())
            if 'path' in uri_components: # no for raster wms, ...
                file_path = uri_components['path']
            # file_path = layer.dataProvider().dataSourceUri()
        else:
            str_error = ('Not exists layer: {}'.format(layer_name))
            return str_error, file_path
        return str_error, file_path

    @classmethod
    def get_raster_band_count(self, layer_name):
        str_error = ''
        raster_count = -1
        layers = QgsProject.instance().mapLayersByName(layer_name)
        if layers:
            layer = layers[0]
            if isinstance(layer, QgsRasterLayer):
                raster_count = layer.bandCount()
            else:
                str_error = ('Not is a raster layer: {}'.format(layer_name))
                return str_error, raster_count
        else:
            str_error = ('Not exists raster layer: {}'.format(layer_name))
            return str_error, raster_count
        return str_error, raster_count

    @classmethod
    def get_raster_layers(self):
        str_error = ''
        layers_by_name = {}
        for layer in QgsProject.instance().mapLayers().values():
            layer_name = layer.name()
            if isinstance(layer, QgsRasterLayer):
                uri_components = QgsProviderRegistry.instance().decodeUri(layer.dataProvider().name(),
                                                                          layer.publicSource())
                if 'path' in uri_components:  # no for raster wms, ...
                    layers_by_name[layer_name] = layer
        return str_error, layers_by_name

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
                    uri_components = QgsProviderRegistry.instance().decodeUri(layer.dataProvider().name(),
                                                                              layer.publicSource())
                    if 'layerName' in uri_components: # not for wfs?, ...
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
        return str_error, layers_by_name

    @classmethod
    def get_vector_layer_field_names(self, layer):
        str_error = ''
        field_names = layer.fields().names()
        return str_error, field_names

    @classmethod
    def initialize(self, iface):
        is_initalized = True
