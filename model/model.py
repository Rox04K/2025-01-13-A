import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()  # necessario instanziare il grafo (DiGraph o Graph)
        self._IDMap = {}  # Utile per prendere subito il nodo in base all'id

        # impostazione della ricorsione
        self._bestCammino = []
        self._bestLunghezza = 0

    '''Comunicazione con il DAO. Quando chiamato dal controller, prende il necessario dal DAO.
       Se serve può farci dei lavori sopra (es. ordinamenti o filtri) per poi restituirlo al controller
       che andrà a riempire i dropdown o mostrare dei valori. 
    '''

    def getLocalizzazione(self):
        return DAO.getLocalization()

    ''' OPERAZIONI SUI GRAFI '''

    def creaGrafo(self, localizzazione):
        # Come prima cosa bisogna pulire il grafo per poterlo ricreare senza dati vecchi
        self._grafo.clear()
        self._IDMap = {}

        # Poi bisogna prendere i nodi e aggiungerli sia al grafo che all'id map
        nodi = DAO.getNodi(localizzazione)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._IDMap[n.GeneID] = n

        archi = DAO.getArchi(localizzazione, self._IDMap)

        for a in archi:
            u = a[0]
            v = a[1]

            cromU = DAO.getPeso(u.GeneID)
            cromV = DAO.getPeso(v.GeneID)
            peso = []
            for p in cromU:
                if p not in peso:
                    peso.append(p)
            for q in cromV:
                if q not in peso:
                    peso.append(q)

            weight = sum(peso)
            self._grafo.add_edge(u, v, weight=weight)

    def getInfo(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getArchiMagg(self):
        archi_ordinati = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'])
        return archi_ordinati

    def getCompConn(self):
        return sorted(nx.connected_components(self._grafo), key=len, reverse=True)


    ''' METODO DI RICORSIONE '''

    def getCammino(self):
        # Prima di tutto bisogna reimpostare i valori della ricorsione a 0 perchè così non salviamo valori vecchi
        self._bestCammino = []
        self._bestLunghezza = 0

        # Poi prepariamo la base della ricorsione. Ci sono diversi tipi di ricorsione che vengono trattati nella parte apposita
        parziale = []

        for n in self._grafo.nodes():
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestCammino, (self._bestLunghezza - 1)

    def _ricorsione(self, parziale):
        # Qui scriviamo il metodo ricorsivo
        pass
