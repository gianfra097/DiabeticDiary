import os
import json
from kivy.app import App

class DiabeticDiarySettings:
    def __init__(self):
        self.settings = dict(
            range_min=85, range_max=180
        )
        self._app = App.get_running_app()#Andiamo a rendere disponibile all'interno dell'oggetto quella che e' l'applicazione kivy in fase di esecuzione

    @property
    def data_path(self):
        #Percorso file json per salvataggio settings
        return os.path.join(
            self._app.user_data_dir, "settings.json"
        )

    #Questa funzoine si occupa di caricare i dati di autenticazione dal nostro storage persistente (file .json settings.json)
    #Se il file esiste andiamo ad aprirlo in modalita' di lettura e carichiamo nel dizionario self.settings, il contenuto del file json.
    def load_settings_from_storage(self): 
        if os.path.exists(
            self.data_path
        ):
            with open(self.data_path, "r") as f:
                self.settings = json.load(f)

    #Salviamo i dati per l'autenticazione attraverso un dump del dizionario (rappresentazione a stringa) dopo aver aperto il file in modalita' di scrittura
    def save_settings_to_storage(self):
        with open(self.data_path, "w") as f:
            json.dump(self.settings, f)