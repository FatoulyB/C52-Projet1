import numpy as np
import math
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)


class AnalyseImage:
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
        image = np.asarray(image)
        return np.sum(image, axis=(-2, -1))

    @staticmethod
    def area(image):
        return np.sum(image)

    @staticmethod
    def centroid(image):
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        return (np.sum(r * image), np.sum(c * image)) / AnalyseImage.area(image)

    @staticmethod
    def draw_circle(image, center, radius):
        y, x = center
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        image[((r-y)**2 + (c-x)**2) <= radius**2] = 1
        return image

    @staticmethod
    def metric_simplification(image):
        aire = AnalyseImage.calculer_aire(image)
        perimetre = AnalyseImage.calculer_perimetre(image)
        return (4 * math.pi * aire) / (perimetre ** 2)

    @staticmethod
    def metric_circle_filling(image):
        shape = np.asarray(image) == 0
        indices = np.argwhere(shape)

        center = AnalyseImage.centroid(shape)

        differences = indices - center
        distances = np.sqrt(np.sum(differences ** 2, axis=1))
        radius = np.max(distances)

        circle = AnalyseImage.draw_circle(np.zeros_like(shape), center, radius)

        circle_pixels = np.count_nonzero(circle)
        shape_pixels = np.count_nonzero(shape)

        remaining_pixels = circle_pixels - shape_pixels

        return remaining_pixels


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