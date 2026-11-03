import numpy as np

class KNN:
    def __init__(self, k, dist, nb_points, nb_metric):
        self.k = k
        self.dist = dist
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
        list_dist.sort()    # sorted par ordre croissant
        list_dist = np.resize(list_dist, (self.k))      # retenu juste les k plus proche
        # doit retenir que ceux dont la distance est plus petite que self.dist
        







def main():
    knn = KNN(1, 30, 5, 3)
    liste = [[1, 30.0, 40.0, 100.0],
             [2, 40.0, 50.0, 110.0],
             [1, 50.0, 60.0, 120.0],
             [2, 60.0, 70.0, 130.0],
             [1, 70.0, 80.0, 140.0],]
    knn.create_dataset(liste)

    print(knn.metrics_list)
    print(knn.class_list)
    temp = np.array([35.0, 45.0, 105.0])
    knn.unknown_point(temp)


if __name__ == "__main__":
    main()


