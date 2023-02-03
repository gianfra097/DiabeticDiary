from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class Attivita(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self._app = App.get_running_app()

    #Quando si apre la pagina attività, se è stata attivata la modalità allora fai comparire solo bottone con scritto disattiva
    def on_enter(self):
        if self._app.my_app_state_activity.attivita_storage['stato'] == True:
            self._app.my_app_state_activity.attivita_storage['cambia_testo'] = 1
            self.ids.testo_centrale_attivita.text = "Modalità attività fisica avviata:\nParametri momentanei:\n Ipo: 140 - Iper: 180"
            self.ids.testo_continua.text = "Vuoi disattivarla?"
            self.ids.attiva_attivita.button_text = "Disattiva"
        elif self._app.my_app_state_activity.attivita_storage['stato'] == False and self._app.my_app_state_activity.attivita_storage['cambia_testo'] == 1:
            self._app.my_app_state_activity.attivita_storage['cambia_testo'] = 0
            self.ids.testo_centrale_attivita.text = "Se continui, i parametri verranno modificati a 140-180, in modo che potrai fermarti e prevenire un eventuale ipoglicemia"
            self.ids.testo_continua.text = "Vuoi attivarla?"
            self.ids.attiva_attivita.button_text = "Attiva"

    #Se premo il bottone, si attiva o disattiva l'attività e torno alla homepage
    def avvia_ferma_attivita(self):
        if self._app.my_app_state_activity.attivita_storage['stato'] == False:
            self._app.my_app_state_activity.attivita_storage['stato'] = True
            self._app.my_app_state_activity.attivita_storage['cambia_popup'] = "attivata"
            self._app.my_app_homepage.update_egvs_value()
        else:
            self._app.my_app_state_activity.attivita_storage['stato'] = False
            self._app.my_app_state_activity.attivita_storage['cambia_popup'] = "disattivata"
            self._app.my_app_homepage.update_egvs_value()
