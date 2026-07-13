# authors:
# David Hernandez Lopez, david.hernandez@uclm.es

import sys, os
from pathlib import Path

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, '..'))
# sys.path.append(os.path.join(current_path, '../..'))
# sys.path.insert(0, '..')

# from VolumeTimeSeries.lib.Project import Project
# from VolumeTimeSeries.defs import defs_project
# from VolumeTimeSeries.defs import defs_main
# from lib import gui_defines as gd
# from lib import qgis_gui_defines as qgd
# from pyCRSs import CRSsDefines as cd
# import json
# import Tools

from qgis.core import (QgsApplication, QgsDataSourceUri, QgsProject,
                       QgsCoordinateReferenceSystem, QgsCoordinateTransform)
from qgis.core import QgsProject, QgsVectorLayer, QgsSymbol, QgsRendererCategory, QgsCategorizedSymbolRenderer
from qgis.core import QgsField, QgsFeature, QgsPoint, QgsGeometry, QgsMapLayer, QgsRectangle, QgsLayerTreeLayer
from qgis import utils
from qgis.core import Qgis

from pyLibProject.defs import defs_project_definition
from pyLibQGIS import defs_qgis

class QGisIFace:
    def __init__(self, iface, plugin_path):
        self.iface = iface
        self.plugin_path = plugin_path
        self.project = None
        self.project_crs = None
        self.layerTreeProjectName = ''
        qgis_bin_path = Path(QgsApplication.prefixPath())
        self.qgis_prefix_path = os.path.realpath(str(qgis_bin_path.parent.parent))
        self.osge4w_bat_path = os.path.normpath(self.qgis_prefix_path + defs_qgis.OSGEO4W_BAT_SUFFIX_WINDOWS)
        self.osge4w_bin_path = os.path.normpath(self.qgis_prefix_path + defs_qgis.OSGEO4W_BIN_SUFFIX_WINDOWS)
        self.qgis_bin_path = os.path.normpath(self.qgis_prefix_path + defs_qgis.QGIS_BIN_SUFFIX_WINDOWS)
        self.qgis_plugins_path = os.path.normpath(self.qgis_prefix_path + defs_qgis.QGIS_PLUGINS_SUFFIX_WINDOWS)
        self.qgis_python_path = os.path.normpath(self.qgis_prefix_path + defs_qgis.QIGS_PYTHON_PATH_SUFFIX_WINDOWS)

    def close_project(self):
        if not self.project:
            return
        if self.layerTreeProjectName is not None:
            root = QgsProject.instance().layerTreeRoot()
            self.remove_group(root, self.layerTreeProjectName)
        self.layerTreeProjectName = None
        self.iface.mapCanvas().refresh()

    def get_map_canvas_wkb_geometry_in_project_crs(self):
        str_error = ''
        if not self.project_crs:
            str_project_crs_epsg_code = self.project.project_definition[
                defs_project_definition.PROJECT_DEFINITIONS_TAG_PROJECTED_CRS]
            epsg_code = -1
            try:
                epsg_code = int(str_project_crs_epsg_code.replace(defs_project_definition.EPSG_STRING_PREFIX, ''))
            except ValueError:
                str_error = ('Invalid integer value from: {}'.format(str_project_crs_epsg_code))
            self.project_crs = QgsCoordinateReferenceSystem(epsg_code)
        geometry = QgsGeometry.fromRect(self.iface.mapCanvas().extent())
        qgis_project_crs = QgsProject.instance().crs()
        tr = QgsCoordinateTransform(qgis_project_crs, self.project_crs, QgsProject.instance())
        geometry.transform(tr)
        wkb = geometry.asWkb()
        return str_error, wkb

    def get_qgis_prefix_path(self):
        return self.qgis_prefix_path

    def load_project(self, layers_group_prefix = None):
        str_error = ''
        if self.project is None:
            str_error = 'No project defined'
            return str_error
        if not defs_project_definition.PROJECT_DEFINITIONS_TAG_TAG in self.project.project_definition:
            str_error =('Not exists {} in project definition'.format(defs_project_definition.PROJECT_DEFINITIONS_TAG))
            return str_error
        if not defs_project_definition.PROJECT_DEFINITIONS_TAG_PROJECTED_CRS in self.project.project_definition:
            str_error =('Not exists {} in project definition'.format(
                defs_project_definition.PROJECT_DEFINITIONS_TAG_PROJECTED_CRS))
            return str_error
        project_tag = self.project.project_definition[defs_project_definition.PROJECT_DEFINITIONS_TAG_TAG]
        project_crs = self.project.project_definition[defs_project_definition.PROJECT_DEFINITIONS_TAG_PROJECTED_CRS]
        layerTreeProjectName = ''
        if not layers_group_prefix is None:
            layerTreeProjectName = layers_group_prefix + '_' + project_tag
        else:
            layerTreeProjectName = project_tag
        root = QgsProject.instance().layerTreeRoot()
        # if exists previous load
        layerTreeProject = root.findGroup(layerTreeProjectName)
        if layerTreeProject is not None:
            self.remove_group(root, layerTreeProject)
            layerTreeProject = None
        self.layerTreeProjectName = layerTreeProjectName
        layerTreeProject = root.insertGroup(0, self.layerTreeProjectName)
        qgisProjectCrsAsEpsg = QgsProject.instance().crs().authid()
        if qgisProjectCrsAsEpsg != project_crs:
            QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(project_crs))
        return str_error

    def open_project(self,
                     project):
        self.close_project()
        self.project = project
        # self.load_project()

    def reload_all_layers(self):
        str_error = ''
        QgsProject.instance().reloadAllLayers()
        return str_error

    def set_map_canvas_from_wkb_geometry_in_project_crs(self,
                                                        wkb_geometry):
        str_error = ''
        if not self.project_crs:
            str_project_crs_epsg_code = self.project.project_definition[
                defs_project_definition.PROJECT_DEFINITIONS_TAG_PROJECTED_CRS]
            epsg_code = -1
            try:
                epsg_code = int(str_project_crs_epsg_code.replace(defs_project_definition.EPSG_STRING_PREFIX, ''))
            except ValueError:
                str_error = ('Invalid integer value from: {}'.format(str_project_crs_epsg_code))
            self.project_crs = QgsCoordinateReferenceSystem(epsg_code)
        geometry = QgsGeometry()
        geometry.fromWkb(wkb_geometry)
        qgis_project_crs = QgsProject.instance().crs()
        tr = QgsCoordinateTransform(self.project_crs, qgis_project_crs, QgsProject.instance())
        geometry.transform(tr)
        self.iface.mapCanvas().setExtent(geometry.boundingBox())
        self.iface.mapCanvas().refresh()
        return str_error

    def remove_group(self, root, name):
        # root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(name)
        if not group is None:
            for child in group.children():
                dump = child.dump()
                id = dump.split("=")[-1].strip()
                QgsProject.instance().removeMapLayer(id)
            root.removeChildNode(group)
        return

    def set_layer_removable(self, layer_name, is_removable=False):
        layers = QgsProject.instance().mapLayersByName(layer_name)
        if layers:
            if len(layers) == 1:
                layer = layers[0]
                flags = layer.flags()
                if is_removable:
                    flags |= QgsMapLayer.LayerFlag(QgsMapLayer.Removable)
                else:
                    flags = flags & ~QgsMapLayer.LayerFlag(QgsMapLayer.Removable)
                layer.setFlags(QgsMapLayer.LayerFlag(flags))
        return

    def set_project(self,
                    project):
        self.project = project

    def zoom_to_project(self):
        if self.project is None:
            return
        if not self.layerTreeProjectName:
            return
        root = QgsProject.instance().layerTreeRoot()
        layerTreeProject = root.findGroup(self.layerTreeProjectName)
        if layerTreeProject is None:
            return
        extent = QgsRectangle()
        extent.setMinimal()
        for child in layerTreeProject.children():
            if isinstance(child, QgsLayerTreeLayer):
                extent.combineExtentWith(child.layer().extent())
        self.iface.mapCanvas().setExtent(extent)
        self.iface.mapCanvas().refresh()
