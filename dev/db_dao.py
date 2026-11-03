import klustr_utils as ku
import klustr_dao as kd
from db_credential import PostgreSQLCredential

class DBDAO():
    def __init__(self):
        super().__init__()
        credential = PostgreSQLCredential(password='AAAaaa111')
        self.__dao = kd.PostgreSQLKlustRDAO(credential)


    # def retourner_donnees(self):
    #     # Utilisez la méthode appropriée de votre DAO pour récupérer les données
    #     data = self.__dao.get_data()  # Remplacez 'get_data' par la méthode réelle de votre DAO
    #     return data