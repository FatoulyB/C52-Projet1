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
        return np.sum(image == 0)

    def centroid_tuple(image):
        true_form = image == 0
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        return (np.sum(r * true_form), np.sum(c * true_form)) / AnalyseImage.area(image)
    

    @staticmethod
    def centroid(image):
        #true_form = tout le blanc = false et le noir = true
        true_form = image == 0
        area = AnalyseImage.area(image)

        if area == 0:
            return 0.0, 0.0

        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        centroid_x = np.sum(c * true_form) / area
        centroid_y = np.sum(r * true_form) / area

        return centroid_x, centroid_y

    @staticmethod
    def draw_circle(image, center, radius):
        y, x = center
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        image[((r-y)**2 + (c-x)**2) <= radius**2] = 1
        return image

    @staticmethod
    def distance_between_points_from_centroid(image, centroid_x, centroid_y):
        true_form = image == 0
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))

        x_forme = c[true_form]
        y_forme = r[true_form]

        grille_distances = np.sqrt((x_forme - centroid_x)**2 + (y_forme - centroid_y)**2)
        return grille_distances

    @staticmethod
    def metric_avg_dist_over_max_dist(image):
        #prendre le centre et avoir un tableau avec les valeurs de distance du centroid
        centroid_x, centroid_y = AnalyseImage.centroid(image)
        grille_distances = AnalyseImage.distance_between_points_from_centroid(image, centroid_x, centroid_y)

        if len(grille_distances) == 0:
            print("NOOOOOO c egale a 0")
            return 0.0

        distance_avg = np.average(grille_distances)
        distance_max = np.max(grille_distances)
        print(distance_avg/distance_max)

        return distance_avg / distance_max

           
    @staticmethod
    def metric_simplification(image):
        aire = AnalyseImage.area(image)
        perimetre = AnalyseImage.calculer_perimetre(image)
        return (4 * math.pi * aire) / (perimetre ** 2)

    @staticmethod
    def metric_circle_filling(image):
        shape = np.asarray(image) == 0
        indices = np.argwhere(shape)

        center = AnalyseImage.centroid_tuple(shape)

        differences = indices - center
        distances = np.sqrt(np.sum(differences ** 2, axis=1))
        radius = np.max(distances)

        circle = AnalyseImage.draw_circle(np.zeros_like(shape), center, radius)

        circle_pixels = np.count_nonzero(circle)
        shape_pixels = np.count_nonzero(shape)

        remaining_pixels = circle_pixels - shape_pixels

        return remaining_pixels


    @staticmethod
    def use_all_metrics(images_and_shape):
        images, shape = images_and_shape    # images = liste de matrices 2D

        metric_1 = np.array([AnalyseImage.metric_simplification(img) for img in images])
        metric_3 = np.array([AnalyseImage.metric_avg_dist_over_max_dist(img) for img in images])

        return [np.asarray(shape), metric_1, metric_3]



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