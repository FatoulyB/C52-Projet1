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
    def area(image):
        return np.sum(image==0)

    @staticmethod
    def centroid(image):
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))

        mask_image = (image == 0)

        area = AnalyseImage.area(image)

        centroid_x = np.sum(c[mask_image]) / area
        centroid_y = np.sum(r[mask_image]) / area

        return centroid_x, centroid_y
           
    @staticmethod
    def metric_simplification(image):
        aire = AnalyseImage.calculer_aire(image)
        perimetre = AnalyseImage.calculer_perimetre(image)
        if np.any(perimetre <= 0):
            raise ValueError("le perimetre doit etre positif")
        return (4 * math.pi * aire) / (perimetre ** 2)
        

    @staticmethod
    def draw_circle(image, center, radius):
        x, y = center
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        
        # approche finale
        image[((r-y)**2 + (c-x)**2) <= radius**2] = 1
        #     \________________________________/
        #                      \___ cette série d'opérations 
        #                           retournent une matrice de booléens
        #                           qui sert de masque à l'assignation de 1


    @staticmethod
    def metric_circle_filling(image):
        # Prendre le nd array
        shape = np.array([[0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0],
                         [0,0,1,1,1,1,1,0,0],
                         [0,0,1,1,1,1,1,0,0],
                         [0,0,1,1,1,1,1,0,0],
                         [0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0]])


        
        
        centroid = centroid(image)

        np.hypot(image, centroid, where=True)
        



        # tracer cercle fictif
        # verifier % de remplissage

        #retourner la valeur de la métrique


        pass


    @staticmethod
    def metric_max_dist_over_avg_dist(image):
        #prendre le centre et avoir un tableau avec les valeurs de distance du centroid
        centroid_x, centroid_y = AnalyseImage.centroid(image)

        distances = AnalyseImage.distance_between_points_from_centroid(image, centroid_x, centroid_y)

        distance_avg = np.average(distances)
        distance_max = np.max(distances)

        return distance_max/distance_avg
        


    def distance_between_points_from_centroid(image, centroid_x, centroid_y):
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))

        grille_distances = np.sqrt((c - centroid_x)**2 + (r - centroid_y)**2)

        return grille_distances


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