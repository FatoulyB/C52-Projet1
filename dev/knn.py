import numpy as np

class KNN:
    def __init__(self, k, max_dist, nb_points, nb_metric):
        self.k = k
        self.max_dist = max_dist
        self.nb_points = nb_points
        self.nb_metric = nb_metric

        self.metrics_list = np.zeros([nb_points, nb_metric], float)
        self.class_list = np.zeros(nb_points, int)

    def create_dataset(self, list_class_points):
        counter = 0
        for points in list_class_points:
            self.class_list[counter] = points[0]    # class_list

            for i in range(self.nb_metric):         # ref_list
                self.metrics_list[counter, i] = points[i+1]     # i in range(..) start with 0 or 1 ? ++ [couter, i] va chercher la valeur à cette coordonné ?

            counter += 1
    
    def add_point(self, point_class, metrics):
        self.metrics_list = np.vstack(self.metrics_list, metrics)       # creer une nouveller list avec l'ancienne et le nouveau point rajouter à la fin (metrics doit être une liste)
        self.class_list = np.vstack(self.class_list, point_class)       # même chose mais point_class est un entier singulier
        self.nb_points += 1
    
    def clear(self):
        # rinitie les deux list avec des zéros¸
        pass
    
    def calc_dist(self, matrix):
        return (np.sum((self.metrics_list[:] - matrix)**2, axis=1)**0.5)
    
    def unknown_point(self, metrics_unknown):
        list_dist = self.calc_dist(metrics_unknown)
        list_dist_arg_sorted = np.argsort(list_dist)[:self.k]                   # sorted par ordre croissant et retiens que k valeur (le slicing plus efficace que resize)

        mask = list_dist[list_dist_arg_sorted] <= self.max_dist               # masque = tab de true/false (seulememnt les plus k plus proche) si dist <= max dist
        list_dist_arg_sorted = list_dist_arg_sorted[mask]                     # cleanup avec le masque
        list_class = self.class_list[list_dist_arg_sorted]

        if len(list_class) == 0:    # si il y a aucun point plus proche que max_dist
            return None

        return self.most_common_class(list_class)
        # si egalite dans nombre de class choisir ceux plus proche
        
    def most_common_class(self, list_class):
        values, indexs, counts = np.unique(list_class, return_index=True, return_counts=True)   # retourne: valeurs sans repition, position de premiere apparition, nbre de repetition
        original_order = np.argsort(indexs)                                                     # reclasse les indexs pour retrouver l'ordre original des valeurs

        if (self.contains_clones(counts[original_order])):    # si il y a des clones (egalité) dans le nombre de repetition
            # return values[original_order][np.argmin(np.sum((self.metrics_list[list_class == values[original_order]] - self.metrics_list[list_class == values[original_order]])**2, axis=1)**0.5)]   # retourne la valeur de la classe la plus proche (la plus petite distance)
            # doit calculer la moyenne des index de chaque classe et retourner la classe avec la plus petite distance à la moyenne
            
            pass

        return values[original_order][np.argmax(counts[original_order])]

    def contains_clones(self, ndArray):
        return len(ndArray) != len(np.unique(ndArray))


        
        







def main():
    knn = KNN(2, 30, 5, 3)
    liste = [
             [1, 30.0, 40.0, 100.0],
             [1, 70.0, 80.0, 140.0],
             [2, 60.0, 70.0, 130.0],
             [1, 50.0, 60.0, 120.0],
             [2, 40.0, 50.0, 110.0],
             ]
    knn.create_dataset(liste)

    print(knn.metrics_list)
    print(knn.class_list)
    temp = np.array([35.0, 45.0, 105.0])
    print(knn.unknown_point(temp))



if __name__ == "__main__":
    main()


