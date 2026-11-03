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
from db_dao import DBDAO

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.window_title = 'KlustR KNN Classifier'
     

        self.layout = QVBoxLayout(self)
        self.layout.add_widget(KnnClassification()) 

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    db = DBDAO()
    print(db.available_datasets())

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
