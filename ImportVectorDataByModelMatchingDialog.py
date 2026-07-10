# authors:
# David Hernandez Lopez, david.hernandez@uclm.es

import os
import sys
import math
import json

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, '..'))

from qgis.PyQt import QtCore, QtWidgets
from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtWidgets import (QApplication, QMessageBox, QDialog, QInputDialog, QHBoxLayout, QDoubleSpinBox,
                             QFileDialog, QPushButton, QComboBox, QPlainTextEdit, QLineEdit, QDateEdit,
                             QDialogButtonBox, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView)
from qgis.PyQt.QtCore import QDir, QFileInfo, QFile, QSize, Qt, QDate

from qgis.core import (QgsApplication, QgsDataSourceUri, QgsProject,
                       QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProviderRegistry)
from qgis.core import (QgsProject, QgsVectorLayer, QgsRasterLayer, QgsSymbol, QgsRendererCategory,
                       QgsCategorizedSymbolRenderer, QgsWkbTypes)
from qgis.core import QgsField, QgsFeature, QgsPoint, QgsGeometry
from qgis import utils
from qgis.core import Qgis

from pyLibCRSs import CRSsDefines as defs_crs
from pyLibCRSs.CRSsTools import CRSsTools
from pyLibGDAL import defs_gdal
from pyLibGDAL.GDALTools import GDALTools

from pyLibCRSs import CRSsDefines as defs_crs
from pyLibCRSs.CRSsTools import CRSsTools
from pyLibQGIS import defs_qgis


class ImportVectorDataByModelMatchingDialog(QDialog):

    def __init__(self,
                 title,
                 label,
                 qgis_iface,
                 settings,
                 parent=None):
        super().__init__(parent)
        loadUi(os.path.join(os.path.dirname(__file__), 'ImportVectorDataByModelMatchingDialog.ui'), self)
        self.qgis_iface = qgis_iface
        self.initialize()

    def initialize(self):
        yo = 1
