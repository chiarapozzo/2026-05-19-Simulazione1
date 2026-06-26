import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getGeneri()
        for g in generi:
            self._view._ddGenre.options.append(ft.dropdown.Option(g))
        self._view._page.update()

    def handleCreaGrafo(self, e):
        # print("IL BOTTONE FUNZIONA!")  # <--- AGGIUNGI QUESTO
        genere = self._view._ddGenre.value
        self._model.buildGraph(genere)
        if genere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere", color= "red"))
            self._view._page.update()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodes()} "))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumEdges()} "))
        self._view._page.update()

        bestArtista, bestScore = self._model.getBestArtista()

        if bestArtista is not None:
            self._view.txt_result.controls.append(ft.Text(f"Artista con maggior influenza {bestArtista}, con influenza: {bestScore}"))

        top5 = self._model.getTop5()
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi: "))
        for u, v, peso in top5:
            testo_arco = f" {u.Name} -> {v.Name} : {peso["weight"]}"
            self._view.txt_result.controls.append(ft.Text(testo_arco))

        self._view._page.update()





    def handleCammino(self,e):
        pass

