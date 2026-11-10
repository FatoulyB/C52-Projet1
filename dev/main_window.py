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
        self.knn_view.set_axis_titles('Simplification',
                                      'Remplissage du cercle',
                                      'Dist. moy. / dist. max')

        self.layout = QVBoxLayout(self)
        self.layout.add_widget(self.knn_view) 

        self.knn = KNN(3, 5)
        self.shape_names = {}

        self.knn_view.dataset_selected.connect(self._on_dataset_selected)
        self.knn_view.classify_requested.connect(self.on_classify_click)

        self._on_dataset_selected("ABC")
        



    @Slot(str)
    def _on_dataset_selected(self, title):
        images, labels = get_dataset_images(title)
        labels = np.asarray(labels)
        self.shape_names = shape_names_from_dataset(title)

        # Phase 1 : métriques -> KNN -> graphique
        _, m1, m2, m3 = AnalyseImage.use_all_metrics(labels, images)
        metrics = np.column_stack((m1, m2, m3))

        self.knn.clear()
        self.knn.create_dataset(np.column_stack((labels, metrics)))

        points_by_class = {
            self.shape_names[int(label_id)]: metrics[labels == label_id]
            for label_id in np.unique(labels)
        }
        self.knn_view.show_training_points(points_by_class)


    @Slot(str, str)
    def on_classify_click(self, title, image_name):
        test_image = get_test_image(title)[image_name][1]
        test_point = np.array([
            AnalyseImage.metric_simplification(test_image),
            AnalyseImage.metric_circle_filling(test_image),
            AnalyseImage.metric_avg_dist_over_max_dist(test_image),
        ])

        predicted_shape_id = self.knn.unknown_point(test_point)

        if predicted_shape_id is None:
            result = "no match"
        else:
            result = self.shape_names[int(predicted_shape_id)]
                
        self.knn_view.show_test_point(test_point.reshape(1,3))
        self.knn_view.show_classification_result(result)
        
        




def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()


    sys.exit(app.exec())


if __name__ == '__main__':
    main()
