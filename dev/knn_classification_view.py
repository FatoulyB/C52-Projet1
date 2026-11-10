import sys
from color_sequence import QColorSequence

# -----------------------------------------------------------------------------
import PySide6 
from __feature__ import snake_case, true_property # type: ignore[import-not-found]
# -----------------------------------------------------------------------------

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize, Signal,Slot
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import  (QSlider, QWidget, QListView, QTreeView,  
                                QGroupBox, QLabel, QCheckBox, QPlainTextEdit,
                                QGridLayout, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy,
                                QMessageBox, QComboBox,QFormLayout, QPushButton, QScrollBar)
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)

# -----------------------------------------------------------------------------
from shibokensupport import feature # type: ignore[import-not-found]
feature.set_selection(feature.snake_case | feature.true_property)
assert "snake_case" in feature.info() and "true_property" in feature.info()
# -----------------------------------------------------------------------------

from scatter_3d_viewer import QScatter3dViewer
from about import ABOUT_TEXT

from db_dao import get_all_dataset_titles, get_dataset_infos, get_test_image,get_test_image_names
selected_dataset = get_dataset_infos("ABC")

class DatasetInformation(QGroupBox):
    def __init__(self, parent=None):
        super().__init__('Inculded in dataset', parent)
        self.__category = QLabel()
        self.__training_image_count = QLabel()
        self.__test__image_count = QLabel()
        self.__total__image_count = QLabel()

        layout = QFormLayout(self)
        layout.add_row(f'Category count : ', self.__category)
        layout.add_row(f'Training image count : ', self.__training_image_count)
        layout.add_row(f'Test image count : ', self.__test__image_count)
        layout.add_row(f'Total image count : ', self.__total__image_count)

    @Slot(str)
    def update_info(self, dataset_name):
        dataset = get_dataset_infos(dataset_name)
        if dataset is None:
            dataset = get_dataset_infos("ABC")
            return

        self.__category.text = (str(dataset[5]))
        self.__training_image_count.text = (str(dataset[6]))
        self.__test__image_count.text = (str(dataset[7]))
        self.__total__image_count.text = (str(dataset[8]))


class DatasetInfoTransformation(QGroupBox):
    def __init__(self, parent=None):
        super().__init__('Transformation', parent)
        self.__translated = QLabel()
        self.__rotated = QLabel()
        self.__scaled = QLabel()

        layout = QFormLayout(self)
        layout.add_row('Translated : ', self.__translated)
        layout.add_row('Rotated : ', self.__rotated)
        layout.add_row('Scaled : ', self.__scaled)

    @Slot(str)
    def update_info(self, dataset_name):
        dataset = get_dataset_infos(dataset_name)
        if dataset is None:
            dataset = get_dataset_infos("ABC")
            return

        self.__translated.text = (str(dataset[2]))
        self.__rotated.text = (str(dataset[3]))
        self.__scaled.text = (str(dataset[4]))

class DatasetBox(QGroupBox):
    eventTriggered = Signal() 
    dataset_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__('Dataset', parent)
        self.__setup_data_set_box()

    def __setup_data_set_box(self):
        self.__dataset_list = QComboBox()
        self.__included_dataset = DatasetInformation()
        self.__transformation = DatasetInfoTransformation()

        self.__dataset_list.add_items(get_all_dataset_titles())

        self.__dataset_list.currentTextChanged.connect(self.on_text_changed)

        main_layout = QVBoxLayout()
        layout = QHBoxLayout()

        layout.add_widget(self.__included_dataset)
        layout.add_widget(self.__transformation)

        main_layout.add_widget(self.__dataset_list)
        main_layout.add_layout(layout)

        self.set_layout(main_layout)

        self.dataset_selected.emit("ABC")
        self.__included_dataset.update_info("ABC")
        self.__transformation.update_info("ABC")

    @Slot(str)
    def on_text_changed(self, text):
        self.dataset_selected.emit(text)
        self.__included_dataset.update_info(text)
        self.__transformation.update_info(text)


class SingleTestBox(QGroupBox):
    classify_requested = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__('Single test', parent)
        self.__test_images = {}
        self.__dataset_name = ''
        self.__setup__single_test_box()

    def __setup__single_test_box(self):
        self.__img_list = QComboBox()
        self.__image = QLabel()
        self.__button_classify = QPushButton("Classify")
        self.__is_classified = QLabel("not classified")

        self.__image.alignment = Qt.AlignCenter
        self.__is_classified.alignment = Qt.AlignCenter

        self.__img_list.currentTextChanged.connect(self.selected_img)
        self.__button_classify.clicked.connect(self.on_classify_clicked)

        layout = QVBoxLayout()
        layout.add_widget(self.__img_list)
        layout.add_widget(self.__image)
        layout.add_widget(self.__button_classify)
        layout.add_widget(self.__is_classified)

        self.set_layout(layout)

    @Slot(str)
    def selected_img(self, text):
        if text not in self.__test_images:
            return
        self.__is_classified.text = 'not classified'
        qimage, image, label_id = self.__test_images[text]
        self.__image.pixmap = QPixmap.from_image(
            qimage.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation))

    @Slot(str)
    def update_images(self, title):
        self.__img_list.clear()
        self.__image.clear()
        self.__dataset_name = title
        self.__test_images = get_test_image(title)
        for nom in self.__test_images:
            self.__img_list.add_item(nom)

    @Slot()
    def on_classify_clicked(self):
        self.classify_requested.emit(self.__dataset_name, self.__img_list.current_text)

    @Slot()
    def show_result(self, text):
        self.__is_classified.text = text

class KNNParamBox(QGroupBox):
    dataset_selected = Signal(str)
    classify_requested = Signal(str, str)
    k_changed = Signal(int)
    max_dist_changed = Signal(float) 

    def __init__(self,parent=None):
        super().__init__('Knn Parameters',parent)
        self.__k = QLabel('k = 3')
        self.__max_dist = QLabel('Max dist = 1.0')
        self.scroll_bar_k = QScrollBar(Qt.Horizontal)
        self.scroll_bar_k.set_range(1, 25)
        self.scroll_bar_k.set_value(3)
        self.scroll_bar_k.valueChanged.connect(self.on_scroll_change)

        self.scroll_bar_max_dist = QScrollBar(Qt.Horizontal)
        self.scroll_bar_max_dist.set_range(1, 10)
        self.scroll_bar_max_dist.set_value(10)
        self.scroll_bar_max_dist.valueChanged.connect(self.on_scroll_dist_change)
        self.__about_button = QPushButton('About')
        self.__about_button.clicked.connect(self.show_about)
        self.__k.alignment = Qt.AlignCenter
        self.__max_dist.alignment = Qt.AlignCenter

        layout = QVBoxLayout()
        layout.add_widget(self.__k)
        layout.add_widget(self.scroll_bar_k)
        layout.add_widget(self.__max_dist)
        layout.add_widget(self.scroll_bar_max_dist)
        layout.add_widget(self.__about_button)
        self.set_layout(layout)

    @Slot()
    def show_about(self):
        QMessageBox.about(self, 'KlustR KNN Classifier', ABOUT_TEXT)

    @Slot(int)
    def on_scroll_dist_change(self, value):
        max_dist = value / 10
        self.__max_dist.text = f'Max dist = {max_dist:.1f}'
        self.max_dist_changed.emit(max_dist)

    @Slot(int)
    def on_scroll_change(self, value):
        self.__k.text = f'k = {value}'
        self.k_changed.emit(value)

    @property
    def k(self):
        return self.scroll_bar_k.value

    @property
    def max_dist(self):
        return self.scroll_bar_max_dist.value / 10

class KnnClassification(QWidget):
    dataset_selected = Signal(str)
    classify_requested = Signal(str, str)
    k_changed = Signal(int)
    max_dist_changed = Signal(float)
    TEST_SERIE_NAME = "Test"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__data_set_box = DatasetBox()
        self.__data_set_box.dataset_selected.connect(self.dataset_selected.emit)
        
        self.__single_test_box = SingleTestBox()
        self.__knn_param_box = KNNParamBox()
        self.__knn_param_box.k_changed.connect(self.k_changed.emit)
        self.__knn_param_box.max_dist_changed.connect(self.max_dist_changed.emit)

        self.__data_set_box.dataset_selected.connect(self.__single_test_box.update_images)
        self.__single_test_box.update_images('ABC')

        self.__single_test_box.classify_requested.connect(self.classify_requested.emit)
        
        left_layout = QVBoxLayout()
        left_layout.add_widget(self.__data_set_box)
        left_layout.add_widget(self.__single_test_box)
        left_layout.add_widget(self.__knn_param_box)
        left_layout.add_stretch()

        self.__scatter = QScatter3dViewer(auto_rotate=True)
        self.__scatter.title = 'KlustR KNN Classification'
        self.__scatter.axis_x.range = (0.0, 1.0)
        self.__scatter.axis_y.range = (0.0, 1.0)
        self.__scatter.axis_z.range = (0.0, 1.0)

        main_layout = QHBoxLayout(self)
        main_layout.add_layout(left_layout)
        main_layout.add_widget(self.__scatter, 1)

    @property
    def k(self):
        return self.__knn_param_box.k

    @property
    def max_dist(self):
        return self.__knn_param_box.max_dist

    def show_classification_result(self, text):
        self.__single_test_box.show_result(text)

    def set_axis_titles(self, x, y, z):
        self.__scatter.axis_x.title = x
        self.__scatter.axis_y.title = y
        self.__scatter.axis_z.title = z

    def show_training_points(self, points_by_class):
        self.__scatter.clear()
        QColorSequence.reset()
        for class_name, points in points_by_class.items():
            self.__scatter.add_serie(points, QColorSequence.next(), class_name, 0.15)

    def show_test_point(self, point):
        self.__scatter.remove_serie(self.TEST_SERIE_NAME)
        self.__scatter.add_serie(point,
                                 QColor('black'), self.TEST_SERIE_NAME, 0.3)
