from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def getLocalization():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct localization
                        from classification c 
                        order by Localization desc """
            cursor.execute(query)

            for row in cursor:
                result.append(row['localization'])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(localizzazione):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select g.GeneID , c.Localization , g.Essential 
                        from genes g , classification c 
                        where g.GeneID = c.GeneID
                        and c.Localization = %s
                                               """
            cursor.execute(query, (localizzazione,))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi(localizzazione, mappa):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select GeneID1 , GeneID2 
                        FROM interactions 
                        where GeneID1 in (select GeneID from classification c where Localization = %s)
                        and GeneID2 in (select GeneID from classification c where Localization = %s)
                        and GeneID1 != GeneID2
                    """
            cursor.execute(query, (localizzazione, localizzazione,))

            for row in cursor:
                result.append((mappa[row['GeneID1']], mappa[row['GeneID2']]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getPeso(id):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct Chromosome 
                        from genes g 
                        where GeneID = %s"""
            cursor.execute(query, (id,))

            for row in cursor:
                result.append(row['Chromosome'])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result




