import numpy as np
import math
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)


class AnalyseImage:


    @staticmethod
    def calculer_perimetre(image):
        image = np.asarray(image, dtype=bool)
        if image.ndim < 2:
            raise ValueError("l'image doit avoir au moins deux dimensions")

        centre = image[..., 1:-1, 1:-1]
        haut = image[..., :-2, 1:-1]
        bas = image[..., 2:, 1:-1]
        gauche = image[..., 1:-1, :-2]
        droite = image[..., 1:-1, 2:]

        interieur = centre & haut & bas & gauche & droite

        contour = (interieur != centre)

        perimetres = np.sum(contour, axis=(-2, -1))
        return int(perimetres) if image.ndim == 2 else perimetres

    @staticmethod
    def calculer_aire(image):
        image = np.asarray(image)
        if image.ndim < 2:
            raise ValueError("l'image doit avoir au moins deux dimensions")
        return np.sum(image, axis=(-2, -1))
           
    @staticmethod
    def metric_simplification(image):
        aire = AnalyseImage.calculer_aire(image)
        perimetre = AnalyseImage.calculer_perimetre(image)
        if np.any(perimetre <= 0):
            raise ValueError("le perimetre doit etre positif")
        return (4 * math.pi * aire) / (perimetre ** 2)
        

    @staticmethod
    def metric_circle_filling():
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
    def metric_3():
        pass


    @staticmethod
    def use_all_metrics(images_and_shape):
        resultat = []

        images = np.asarray(images_and_shape[0])
        shape = np.asarray(images_and_shape[1])

        metric_1 = AnalyseImage.metric_simplification(images)
        # metric_2 = AnalyseImage.metric_circle_filling(images)
        # metric_3 = AnalyseImage.metric_3(images)

        resultat = [shape, metric_1]

        return resultat



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