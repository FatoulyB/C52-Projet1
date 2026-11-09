import numpy as np

class KNN:
    def __init__(self, k, max_dist):
        #  validation de l'intrant k
        self.k = max(1, int(k))  # k doit etre un entier positif, si k < 1 alors k = 1
        self.max_dist = max_dist
        self.class_list = None
        self.metrics_list = None

    def create_dataset(self, list_class_points):
        data = np.array(list_class_points)
        self.class_list = data[:, 0].astype(int)            # liste des classes
        self.metrics_list = data[:, 1:].astype(float)       # liste des metrics

    
    def add_point(self, point_class, metrics):
        metrics = np.array(metrics)

        if(self.metrics_list is None or len(self.metrics_list) == 0):
            self.metrics_list = np.array([metrics])                           # init les metrics_list avec le premier point
            self.class_list = np.array([point_class])                         # init les class_list avec la liste du premier point
        else:
            self.metrics_list = np.vstack([self.metrics_list, metrics])       # creer une nouveller list avec l'ancienne et le nouveau point rajouter à la fin (metrics doit être une liste)
            self.class_list = np.append(self.class_list, point_class)         # append rajoute une valeur singuliere a un array (point_class doit être un int)
    
    def clear(self):
        self.metrics_list = None
        self.class_list = None
    
    def calc_dist(self, matrix):
        return (np.sum((self.metrics_list - matrix)**2, axis=1)**0.5)
    
    def unknown_point(self, metrics_unknown):
        if self.metrics_list is None or len(self.metrics_list) == 0:
            return None
        list_dist = self.calc_dist(metrics_unknown)
        list_dist_arg_sorted = np.argsort(list_dist)[:self.k]                 # sorted par ordre croissant et retiens que k valeur (le slicing plus efficace que resize)

        mask = list_dist[list_dist_arg_sorted] <= self.max_dist               # masque = tab de true/false (seulememnt les plus k plus proche) si dist <= max dist
        list_dist_arg_sorted = list_dist_arg_sorted[mask]                     # cleanup avec le masque
        list_class = self.class_list[list_dist_arg_sorted]

        if len(list_class) == 0:    # si il y a aucun point plus proche que max_dist
            return None

        return self.most_common_class(list_class)
        
    def most_common_class(self, list_class):
        if len(list_class) <= 1:
            return list_class[0] if len(list_class) == 1 else None           # s'il y a juste une class elle est return si il y a aucune class return None

        values, indexs, counts = np.unique(list_class, return_index=True, return_counts=True)   # retourne: valeurs sans repition, position de premiere apparition, nbre de repetition
        original_order = np.argsort(indexs)                                                     # reclasse les indexs pour retrouver l'ordre original des valeurs

        ordered_values = values[original_order]                                                 # retourne les valeurs dans l'ordre original
        ordered_counts = counts[original_order]                                                 # retourne les nbre de repetition dans l'ordre original

        max_count = np.max(ordered_counts)                                                      # retourne le max de repition d'une (ou plusieurs) classes
        mask = (ordered_counts == max_count)
        
        if (np.sum(mask) > 1):                                                                  # si il y a plusieur classe avec le nbre max de repetition
            return self.most_common_class(list_class[:-1])                                      # on relance la fonction avec  pour trouver le plus proche

        return ordered_values[np.argmax(ordered_counts)]                                        # retourne la valeur de la classe avec le nbre max de repetition










def main():
    knn = KNN(2, 30)
    liste = [
             [1, 30.0, 40.0, 100.0],
             [1, 70.0, 80.0, 140.0],
             [2, 60.0, 70.0, 130.0],
             [1, 50.0, 60.0, 120.0],
             [2, 40.0, 50.0, 110.0],
             ]
    knn.create_dataset(liste)

    temp = np.array([35.0, 45.0, 105.0])
    print(knn.unknown_point(temp))



if __name__ == "__main__":
    main()


