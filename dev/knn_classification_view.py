import sys


# -----------------------------------------------------------------------------
import PySide6 
from __feature__ import snake_case, true_property # type: ignore[import-not-found]
# -----------------------------------------------------------------------------

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import  (QApplication, QWidget, QListView, QTreeView,  
                                QGroupBox, QLabel, QCheckBox, QPlainTextEdit,
                                QGridLayout, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy,
                                QMessageBox)
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)

# -----------------------------------------------------------------------------
from shibokensupport import feature # type: ignore[import-not-found]
feature.set_selection(feature.snake_case | feature.true_property)
assert "snake_case" in feature.info() and "true_property" in feature.info()
# -----------------------------------------------------------------------------

from scatter_3d_viewer import QScatter3dViewer


class KnnClassification(QWidget):
    def __init__(self,dao, parent=None):
        super().__init__(parent)
        self.__dao = dao

        self.__data_set_box = QGroupBox('Dataset')
        self.__single_test_box = QGroupBox('Single test')
        self.__knn_param_box = QGroupBox('Knn Parameters')

        self.__data_set_box.set_layout(QVBoxLayout())
        self.__single_test_box.set_layout(QVBoxLayout())
        self.__knn_param_box.set_layout(QVBoxLayout())

        self.__data_set_box.layout().add_widget(QLabel("phase 1  a faire"))
        self.__single_test_box.layout().add_widget(QLabel("phase 1  a faire"))
        self.__knn_param_box.layout().add_widget(QLabel("phase 1  a faire"))

        left_layout = QVBoxLayout()
        left_layout.add_widget(self.__data_set_box)
        left_layout.add_widget(self.__single_test_box)
        left_layout.add_widget(self.__knn_param_box)
        left_layout.add_stretch()


        self.__scatter = QScatter3dViewer(auto_rotate=True)
        self.__scatter.title = 'KlustR KNN Classification'
        self.__scatter.axis_x.title = 'Axis 0'
        self.__scatter.axis_y.title = 'Axis 1'
        self.__scatter.axis_z.title = 'Axis 2'
        self.__scatter.axis_x.range = (0.0, 1.0)
        self.__scatter.axis_y.range = (0.0, 1.0)
        self.__scatter.axis_z.range = (0.0, 1.0)

        main_layout = QHBoxLayout(self)
        main_layout.add_layout(left_layout)
        main_layout.add_widget(self.__scatter, 1)



                
