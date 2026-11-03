import klustr_utils as ku
import klustr_dao as kd
from db_credential import PostgreSQLCredential

class DBDAO():
    def __init__(self):
        super().__init__()
        credential = PostgreSQLCredential(password='AAAaaa111')
        self.__dao = kd.PostgreSQLKlustRDAO(credential)

    def available_datasets(self):
        # Utilisez la méthode appropriée de votre DAO pour récupérer les données
        data = self.__dao.available_datasets()  # Remplacez 'get_data' par la méthode réelle de votre DAO
        return data
    
    # def label_from_data_set(self, dataset_name):
    #     # Utilisez la méthode appropriée de votre DAO pour récupérer les données
    #     data_set_labels = DBDAO.available_datasets()
    #     data = self.__dao.image_from_dataset_label(dataset_name, data_set_labels)  # Remplacez 'get_data' par la méthode réelle de votre DAO
    #     return data
    

