import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()  # necessario instanziare il grafo (DiGraph o Graph)
        self._IDMap = {}  # Utile per prendere subito il nodo in base all'id

        # impostazione della ricorsione
        self._bestCammino = []
        self._bestSottocomponenti = float('inf')

    def getLocalizzazione(self):
        return DAO.getLocalization()

    def creaGrafo(self, localizzazione):
        self._grafo.clear()
        self._IDMap = {}

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

    def getCamminoOttimo(self):
        self._bestCammino = []
        self._bestSottocomponenti = float('inf')

        lista = sorted(self._grafo.nodes(), key=lambda x: x.GeneID)

        for l in range(len(lista) - 1):
            c = lista[l]
            #condizione di inserimento nella lista
            if c.Essential != '?':
                parziale = [c]
                self._ricorsione(parziale, lista, (l + 1))

        return self._bestCammino, self._bestSottocomponenti

    def _ricorsione(self, parziale, lista, livello):

        if livello == len(lista):
            if len(parziale) > len(self._bestCammino):
                pesoAttuale = self._peso(parziale)
                self._bestCammino = copy.deepcopy(parziale)
                self._bestSottocomponenti = pesoAttuale
                return
            elif len(parziale) == len(self._bestCammino):
                pesoAttuale = self._peso(parziale)
                if pesoAttuale < self._bestSottocomponenti:
                    self._bestCammino = copy.deepcopy(parziale)
                    self._bestSottocomponenti = pesoAttuale
                return
            else:
                return

        attuale = lista[livello]
        if attuale.Essential == parziale[-1].Essential:
            parziale.append(attuale)
            self._ricorsione(parziale, lista, livello + 1)
            parziale.pop()

        self._ricorsione(parziale, lista, livello + 1)

    def _peso(self, parziale):
        grafo = self._grafo.subgraph(parziale)
        return nx.number_connected_components(grafo)


    def get_list_nodes(self):
        self._bestListNodes = []
        self._bestScore = len(self._grafo.nodes)
        self._bestLen = 0

        allNodes = list(self._grafo.nodes)
        allNodes.sort(key=lambda x: x.GeneID)

        for root in allNodes:
            rimanenti = copy.deepcopy(allNodes)
            rimanenti.remove(root)
            rimanenti = [x for x in rimanenti if x.Essential == root.Essential]

            self._ricorsione([root], list(rimanenti))

        print(self._bestLen, self._bestScore)
        return self._bestListNodes, self._bestLen, self._bestScore

    '''def _ricorsione(self, parziale, rimanenti):
        if len(parziale) > self._bestLen:
            self._bestLen = len(parziale)
            self._bestScore = self._getScore(parziale)
            self._bestListNodes = copy.deepcopy(parziale)
            if len(parziale) == self._bestLen:
                if self._getScore(parziale) < self._bestScore:
                    self._bestScore = self._getScore(parziale)
                    self._bestListNodes = copy.deepcopy(parziale)

        if len(rimanenti) == 0:
            return

        for n in rimanenti:
            if n.GeneID > parziale[-1].GeneID:
                parziale.append(n)
                rimanenti.remove(n)
                self._ricorsione(parziale, rimanenti)
                parziale.remove(n)
                rimanenti.append(n)

    def _getScore(self, parziale):
        return nx.number_connected_components(self._grafo.subgraph(parziale))
'''