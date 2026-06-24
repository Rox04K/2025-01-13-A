import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        opzioni = self._model.getLocalizzazione()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(x), opzioni))
        self._view.dd_localization.options = opzioniDD

    def handle_graph(self, e):
        localizzazione = self._view.dd_localization.value
        if localizzazione == "":
            self._view.create_alert('Scegliere una localizzazione!')
            return

        self._view.txt_result.controls.clear()
        self._model.creaGrafo(localizzazione)

        nodi, archi = self._model.getInfo()
        self._view.txt_result.controls.append(ft.Text(f'Creato grafo con {nodi} nodi e {archi} archi'))

        self._view.txt_result.controls.append(ft.Text())
        archiMagg = self._model.getArchiMagg()
        for a, b, data in archiMagg:
            self._view.txt_result.controls.append(ft.Text(f'{a} <-> {b}: peso {data['weight']}'))

        self._view.update_page()

    def analyze_graph(self, e):
        self._view.txt_result.controls.append(ft.Text())
        compConn = self._model.getCompConn()
        self._view.txt_result.controls.append(ft.Text('Le componenti connesse sono:'))
        for c in compConn:
            if len(c) > 1:
                stringa = ''
                for n in c:
                    stringa += f'{n}, '
                self._view.txt_result.controls.append(ft.Text(f'{stringa} | dimensione componente = {len(c)}'))

        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result.controls.clear()
        cammino, sottocomponenti = self._model.getCamminoOttimo()
        self._view.txt_result.controls.append(ft.Text(f'Il cammino ottimo è lungo {len(cammino)} ed ha {sottocomponenti} componenti connesse'))
        for s in cammino:
            self._view.txt_result.controls.append(ft.Text(s))

        self._view.update_page()

