from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
import webbrowser

class Dati(Screen):
    eta = NumericProperty()
    peso = NumericProperty()
    tipo_diabete = StringProperty()
    terapia = StringProperty()
    fsi = NumericProperty()
    ic = NumericProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self._app = App.get_running_app()

    def on_enter(self):
        #Aggiorno la scelta di "tipo diabete" e "terapia" anche a schermo oltre che nel file .json, cambiando il text
        self.ids.tipo_diabete.text = self._app.my_app_params.params['tipo_diabete']
        self.ids.terapia.text = self._app.my_app_params.params['terapia']

        #Se i valori fsi e ic sono stati cambiati poco prima di entrare nella sezione "bolo", aggiornali appena questa pagina viene aperta
        if(int(self.ids.fsi.text) != int(self._app.my_app_params.params['fsi'])):
            self.ids.fsi.text = str(self._app.my_app_params.params['fsi'])
        if(int(self.ids.r_ic.text) != int(self._app.my_app_params.params['ic'])):
            self.ids.r_ic.text = str(self._app.my_app_params.params['ic'])

    #Funzione che verifica se i parametri inseriti sono corretti
    def verifica_parametri(self):
        #Creo il percorso
        self.dati_screen = self._app.root.get_screen('Dati')

        #Inserisco i valori che vengono scritti all'interno delle rispettive variabili
        self.eta_user_input = self.dati_screen.ids.eta.text
        self.peso_user_input = self.dati_screen.ids.peso.text
        self.fsi_user_input = self.dati_screen.ids.fsi.text
        self.r_ic_user_input = self.dati_screen.ids.r_ic.text
        self.tipo_diabete_user_input = self.ids.tipo_diabete.text
        self.terapia_user_input = self.ids.terapia.text
        
        #Verifico che gli input siano validi
        #ETA:
        if(len(self.eta_user_input)>0 and int(self.eta_user_input)>0 and int(self.eta_user_input)<=100 and int(str(self.eta_user_input)[:1])!=0):
            self.ids.eta.foreground_color = 0,0,0,1
            self.eta_verificata = 1
        else:
            self.ids.eta.foreground_color = 1,0,0,1
            self.eta_verificata = 0
        #PESO:
        if(len(self.peso_user_input)>0 and int(self.peso_user_input)>=10 and int(self.peso_user_input)<=200 and int(str(self.peso_user_input)[:1])!=0):
            self.ids.peso.foreground_color = 0,0,0,1
            self.peso_verificato = 1
        else:
            self.ids.peso.foreground_color = 1,0,0,1
            self.peso_verificato = 0
        #FSI:
        if(len(self.fsi_user_input)>0 and int(self.fsi_user_input)>=10 and int(self.fsi_user_input)<=200 and int(str(self.fsi_user_input)[:1])!=0):
            self.ids.fsi.foreground_color = 0,0,0,1
            self.fsi_verificato = 1
        else:
            self.ids.fsi.foreground_color = 1,0,0,1
            self.fsi_verificato = 0
        #I:C:
        if(len(self.r_ic_user_input)>0 and int(self.r_ic_user_input)>=10 and int(self.r_ic_user_input)<=200 and int(str(self.r_ic_user_input)[:1])!=0):
            self.ids.r_ic.foreground_color = 0,0,0,1
            self.r_ic_verificato = 1
        else:
            self.ids.r_ic.foreground_color = 1,0,0,1
            self.r_ic_verificato = 0

        #Se tutti i campi sono stati compilati attiva il bottone salva
        if(self.eta_verificata == 1 and self.peso_verificato == 1 and self.fsi_verificato == 1 and self.r_ic_verificato == 1 and self.tipo_diabete_user_input != "Seleziona" and self.terapia_user_input != "Seleziona"):
            self.ids.salva_parametri.disabled = False
        else:
            self.ids.salva_parametri.disabled = True

    def salva_dati(self):
        #Se viene cliccato il bottone salva, associo alle variabili peso,eta,tipo_diabete,terapia,fsi e ic i valori inseriti dall'utente
        self.eta = self.eta_user_input
        self.peso = self.peso_user_input
        self.tipo_diabete = self.tipo_diabete_user_input
        self.terapia = self.terapia_user_input
        self.fsi = self.fsi_user_input
        self.ic = self.r_ic_user_input

        #Modifico i valori nel dizionario con i valori appena salvati all'interno dellw variabili (cioè quelli scritto dall'utente)
        self._app.my_app_params.params['eta'] = int(self.eta_user_input)
        self._app.my_app_params.params['peso'] = int(self.peso_user_input)
        self._app.my_app_params.params['tipo_diabete'] = self.tipo_diabete_user_input
        self._app.my_app_params.params['terapia'] = self.terapia_user_input
        self._app.my_app_params.params['fsi'] = int(self.fsi_user_input)
        self._app.my_app_params.params['ic'] = int(self.r_ic_user_input)

        #Salvo i dati nello storage
        self._app.my_app_params.save_params_to_storage()

    #Funzione che preimposta un messaggio con i dati da inviare via mail
    def invia_report(self):
        webbrowser.open(
            "mailto:?subject=Report Dati&body=Età: {}\nPeso: {}\nTipo di diabete: {}\nTerapia: {}\nFSI: {}\nIC: {}".format(
                self._app.my_app_params.params["eta"],
                self._app.my_app_params.params["peso"],
                self._app.my_app_params.params['tipo_diabete'],
                self._app.my_app_params.params['terapia'],
                self._app.my_app_params.params['fsi'],
                self._app.my_app_params.params['ic']
            )
        )