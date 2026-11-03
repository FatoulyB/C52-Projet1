import sys


# -----------------------------------------------------------------------------
import PySide6 
from __feature__ import snake_case, true_property # type: ignore[import-not-found]
# -----------------------------------------------------------------------------

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize, Signal,Slot
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import  (QApplication, QWidget, QListView, QTreeView,  
                                QGroupBox, QLabel, QCheckBox, QPlainTextEdit,
                                QGridLayout, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy,
                                QMessageBox, QComboBox,QFormLayout, QPushButton)
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)

# -----------------------------------------------------------------------------
from shibokensupport import feature # type: ignore[import-not-found]
feature.set_selection(feature.snake_case | feature.true_property)
assert "snake_case" in feature.info() and "true_property" in feature.info()
# -----------------------------------------------------------------------------

from scatter_3d_viewer import QScatter3dViewer



class DatasetInformation(QGroupBox):
    def __init__(self, parent=None):
        super().__init__('Inclded in dataset', parent)
        self.__category = QLabel()
        self.__training_image_count = QLabel()
        self.__test__image_count = QLabel()
        self.__total__image_count = QLabel()

        layout = QFormLayout(self)
        layout.add_row('Category count :', self.__category)
        layout.add_row('Training image count :', self.__training_image_count)
        layout.add_row('Test image count :', self.__test__image_count)
        layout.add_row('Total image count :', self.__total__image_count)

    @Slot()
    def update_info(self):
        pass

        # c'est quoi l'inpact sur le k question 

class DatasetInfoTransfirmation(QGroupBox):
    def __init__(self, parent=None):
        super().__init__('Transformation', parent)
        self.__translated = QLabel()
        self.__rotated = QLabel()
        self.__scaled = QLabel()

        layout = QFormLayout(self)
        layout.add_row('Translated', self.__translated)
        layout.add_row('Rotaded', self.__rotated)
        layout.add_row('Scaled', self.__scaled)
    
    @Slot()
    def update_info(self):
        pass   

class DatatsetBox(QGroupBox):
    eventTriggered = Signal() 

    def __init__(self, parent=None):
        super().__init__('Dataset', parent)
        self.__setup_data_set_box()

    def __setup_data_set_box(self):
        self.__dataset_list = QComboBox()
        self.__included_dataset = DatasetInformation()
        self.__transformation = DatasetInformation()


        main_layout = QVBoxLayout()
        layout = QHBoxLayout()

        layout.add_widget(self.__included_dataset)
        layout.add_widget(self.__transformation)

        main_layout.add_widget(self.__dataset_list)
        main_layout.add_layout(layout)

        self.set_layout(main_layout)



class SingleTestBox(QGroupBox):
    eventTriggered = Signal() 

    def __init__(self,parent=None):
        super().__init__('Single test', parent)
        self.__setup__single_test_box()
    
    def __setup__single_test_box(self):
        self.__img_list = QComboBox() 
        self.__image = QLabel() #transformer en Qpix comme dans GOL
        self.__button_classify = QPushButton()
        # self.__
        layout = QVBoxLayout()


        layout.add_widget(self.__img_list)
        layout.add_widget(self.__image)
        layout.add_widget(self.__button_classify)

        self.set_layout(layout)
        

class KNNParamBox(QGroupBox):
    eventTriggered = Signal() 

    def __init__(self,parent=None):
        super().__init__('Knn Parameters',parent)
        self.__k = QLabel('k = ')
        self.__max_dist = QLabel('Max dist = ')

        self.__k.alignment = Qt.AlignCenter
        self.__max_dist = Qt.AligCenter

        layout = QVBoxLayout()
        layout.add_widget(self.__k)
        layout.add_widget(self.__max_dist)
        self.set_layout(layout)


    
    def __setup__knn_param_box(self):
        pass



class KnnClassification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__data_set_box = DatatsetBox()
        self.__single_test_box = SingleTestBox()
        self.__knn_param_box = KNNParamBox()

        self.__data_set_box.set_layout(QVBoxLayout())
        self.__single_test_box.set_layout(QVBoxLayout())
        self.__knn_param_box.set_layout(QVBoxLayout())


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


                
