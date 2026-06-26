import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMap = {}
        pass

    def getGeneri(self):
        return DAO.getAllGenre()

    def buildGraph(self, genere):
        self._graph = nx.DiGraph()
        self._graph.clear()
        self._nodes = DAO.getAllNodes(genere)
        for n in self._nodes:
            self._idMap[n.ArtistId] = n
        self._graph.add_nodes_from(self._nodes)

        mappa_popolarita = DAO.getPopolarita(genere)
        archi = DAO.getAllEdges(genere)

        for id1, id2 in archi:
            nodo_a = self._idMap[id1]
            nodo_b = self._idMap[id2]

            #prendo la popolarità, se l'artista non c'è nella mappa vuol dire che ha venduto 0
            pop_a = mappa_popolarita.get(id1, 0)
            pop_b = mappa_popolarita.get(id2, 0)

            peso = pop_a + pop_b

            if pop_a > pop_b:
                self._graph.add_edge(nodo_a, nodo_b, weight=peso)
            elif pop_a == pop_b:
                self._graph.add_edge(nodo_a, nodo_b, weight=peso)
                self._graph.add_edge(nodo_b, nodo_a, weight=peso)
            elif pop_b > pop_a:
                self._graph.add_edge(nodo_b, nodo_a, weight=peso)

    def getBestArtista(self):
        bestArtista = None
        bestScore = 0
        for n in self._graph.nodes:
            somma_archi_entranti = 0
            somma_archi_uscenti = 0
            for e in self._graph.out_edges(n, data=True):
                somma_archi_uscenti += e[2]["weight"]
            for e in self._graph.in_edges(n, data=True):
                somma_archi_entranti += e[2]["weight"]
            influenza = somma_archi_uscenti - somma_archi_entranti
            if influenza > bestScore:
                bestArtista = n
                bestScore = influenza
        return bestArtista, bestScore

    def getTop5(self):
        archi = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]
        return archi




    def getNumNodes(self):
        return len(self._nodes)

    def getNumEdges(self):
        return len(self._graph.edges)
