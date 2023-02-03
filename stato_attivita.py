import os
import json
from kivy.app import App

#Classe che serve solo ad aggiornare una variabile per mostrare a schermo se "attività" è attiva o no
class DiabeticDiaryStateActivity:
    def __init__(self):
        self.attivita_storage = dict(
            stato = False,
            cambia_testo = 0,
            cambia_popup = "disattivata"
        )
        self._app = App.get_running_app()