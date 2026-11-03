import numpy as np
import math
from klustr_utils import qimage_argb32_from_png_decoding, ndarray_from_qimage_argb32
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)


class AnalyseImage:

    @staticmethod
    def png_to_nd_array(img_png):
        #DOIT METTRE L'IMAGE PNG DANS LES PARAM DE qimage_argb32_from_png_decoding()
        qimage = qimage_argb32_from_png_decoding(img_png)
        nd_array = ndarray_from_qimage_argb32(qimage)
        return nd_array
        

    @staticmethod
    def calculer_perimetre(image):
        image = image.astype(bool)

        centre = image[1:-1, 1:-1]
        haut = image[:-2, 1:-1]
        bas = image[2:,1:-1]
        gauche = image[1:-1,:-2]
        droite = image[1:-1, 2:]

        interieur = centre & haut & bas & gauche & droite

        contour = (interieur != centre)

        return int(np.sum(contour))

    @staticmethod
    def calculer_aire(image):
        return np.sum(image)
           
    @staticmethod
    def metrique_simplification(image):
        aire = AnalyseImage.calculer_aire(image)
        perimetre = AnalyseImage.calculer_perimetre(image)
        if(perimetre <= 0):
            raise ValueError("le perimetre doit etre positif")
        return ((4 * math.pi) * aire ) / (perimetre **2)
        

    @staticmethod
    def metrique_circle_filling():
        # Prendre le nd array
        #shape = AnalyseImage.png_to_nd_array()
        shape = np.array([[0,0,0,0,0,0,0,0,0],
                         [0,0,1,1,1,1,1,0,0],
                         [0,0,1,1,1,1,1,0,0],
                         [0,0,1,1,1,1,1,0,0],
                         [0,0,0,0,0,0,0,0,0]])
        

        # analyser le ndarray
        # trouver centroid avec fonction du prof 
        # tracer cercle fictif
        # verifier % de remplissage

        #retourner la valeur de la métrique


        pass

    @staticmethod
    def metrique_3():
        pass



# #TEST
# masque = np.zeros((5, 5), dtype=bool)
# masque[1:4, 1:4] = True      # carré 3x3
# print(AnalyseImage.calculer_perimetre(masque))   # attendu : 8

# a = np.arange(25).reshape(5, 5)
#print(a[1:-1, 1:-1])   # le centre
#print(a[:-2, 1:-1])    # haut
#print(a[2:5, 1:3])

# masque = np.zeros((150, 150), dtype=bool)
# masque[1:4, 1:4] = True
# print(AnalyseImage.metrique_1(masque))