from db_dao import DBDAO

class Controleur:
    def __init__(self):
        db_donnees = DBDAO()
        self.__dao = db_donnees._DBDAO__dao 
