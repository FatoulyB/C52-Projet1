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


from knn_classification_view import KnnClassification
from analyse_image import AnalyseImage
from db_dao import get_dataset_images, shape_names_from_dataset, get_test_image
from knn import KNN
import numpy as np




class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.window_title = 'KlustR KNN Classifier'

        self.knn_view = KnnClassification()

        self.layout = QVBoxLayout(self)
        
        self.layout.add_widget(self.knn_view) 

        self.knn_view.dataset_selected.connect(self._on_dataset_selected)

        self.knn_view.classify_requested.connect(self.on_classify_click)

        self.analyse_image = AnalyseImage()



    @Slot(str)
    def _on_dataset_selected(self, title):
        pass


    @Slot(str)
    def on_classify_click(self, title, image_name):

        test_image = get_test_image(title)[image_name][1]
        test_image = np.array([
            AnalyseImage.metric_simplification(test_image),
            AnalyseImage.metric_circle_filling(test_image),
            AnalyseImage.metric_avg_dist_over_max_dist(test_image),
        ])


        images_and_shape = get_dataset_images(title)
        points = self.analyse_image.use_all_metrics(images_and_shape[1], images_and_shape[0])

        shape_names = shape_names_from_dataset(title)

        shape_name = points[0]
        metric_results = np.column_stack((points[1], points[2], points[3]))

        data = np.column_stack((shape_name, metric_results))

        knn = KNN(3, 5)

        knn.create_dataset(data)
        
        predicted_shape_id = knn.unknown_point(test_image)

        if predicted_shape_id is None:
            result = "no match"
        else:
            result = shape_names[predicted_shape_id]
        self.knn_view.show_classification_result(result)



def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()


    sys.exit(app.exec())


if __name__ == '__main__':
    main()
