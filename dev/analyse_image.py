import numpy as np
import math


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
    def metrique_1(image):
        return np.sum(image)
           
    @staticmethod
    def simplification(image):
        aire = AnalyseImage.calculer_aire(image)
        perimetre = AnalyseImage.calculer_perimetre(image)
        if(perimetre <= 0):
            raise ValueError("le perimetre doit etre positif")
        return ((4 * math.pi) * aire ) / (perimetre **2)
        

    @staticmethod
    def mertique_2():
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

masque = np.zeros((150, 150), dtype=bool)
masque[1:4, 1:4] = True
print(AnalyseImage.metrique_1(masque))