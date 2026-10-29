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

class MainWindow(QWidget):

    def __init__(self, dao):
        super().__init__()

        self.window_title = 'KlustR KNN Classifier'
        self.__dao = dao

        self.layout = QVBoxLayout(self)
        self.layout.add_widget(KnnClassification(dao)) 

def main():
    app = QApplication(sys.argv)
    credential = PostgreSQLCredential(password='123') 
    #credential = PostgreSQLCredential(password='AAAaaa111') --> chez moi !! NE PAS EFFACER PLSSS -fatou
    dao =PostgreSQLKlustRDAO(credential)

    window = MainWindow(dao)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
