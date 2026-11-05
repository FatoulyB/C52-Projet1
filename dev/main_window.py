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


from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from knn_classification_view import KnnClassification
from db_dao import get_all_dataset_titles, get_dataset_images


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.window_title = 'KlustR KNN Classifier'

        self.knn_view = KnnClassification()

        self.layout = QVBoxLayout(self)
        
        self.layout.add_widget(self.knn_view) 

        self.knn_view.dataset_selected.connect(self._on_dataset_selected)


    def _on_dataset_selected(self, title):
        images = get_dataset_images(title)
        print(f"Selected {title}; loaded {len(images)} images")

        

        # ici call knn avec le dataset


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()


    sys.exit(app.exec())


if __name__ == '__main__':
    main()
6