from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

class Bolo(Screen):
    glicemia = NumericProperty()
    fsi_bolo = NumericProperty()
    ic_bolo = NumericProperty()
    carboidrati = NumericProperty()
    insulina_attiva = NumericProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dati_bolo = dict(
            bolo_richiesto=0, insulina_attiva=0, bolo_finale=0, correzione=0
        )
        self._app = App.get_running_app()

    #Controllare quando ancora non si ha nessun valore (prima apertura)
    #Se i valori fsi e ic sono stati cambiati poco prima di entrare nella sezione "bolo", aggiornali appena questa pagina viene aperta
    def on_enter(self):
        if(int(self.ids.fsi_bolo.text) != int(self._app.my_app_params.params['fsi'])):
            self.ids.fsi_bolo.text = str(self._app.my_app_params.params['fsi'])
        if(int(self.ids.r_ic_bolo.text) != int(self._app.my_app_params.params['ic'])):
            self.ids.r_ic_bolo.text = str(self._app.my_app_params.params['ic'])

    #Funzione che verifica se i dati scritti per calcolare il bolo sono validi    
    def verifica_bolo(self):
        #Creo il percorso
        self.bolo_screen = self._app.root.get_screen('Bolo')
    
        #Inserisco i valori all'interno delle rispettive variabili
        self.glicemia_user_input = self.bolo_screen.ids.glicemia.text
        self.fsi_bolo_user_input = self.bolo_screen.ids.fsi_bolo.text
        self.r_ic_bolo_user_input = self.bolo_screen.ids.r_ic_bolo.text
        self.carboidrati_user_input = self.bolo_screen.ids.carboidrati.text
        self.insulina_attiva_user_input = self.bolo_screen.ids.insulina_attiva.text

        #Verifico che gli input siano validi
        #GLICEMIA:
        if(len(self.glicemia_user_input)>0 and int(self.glicemia_user_input)>=30 and int(self.glicemia_user_input)<=500):
            self.ids.glicemia.foreground_color = 0,0,0,1
            self.glicemia_verificata = 1
        else:
            self.ids.glicemia.foreground_color = 1,0,0,1
            self.glicemia_verificata = 0
        #FSI:
        if(len(self.fsi_bolo_user_input)>0 and int(self.fsi_bolo_user_input)>=10 and int(self.fsi_bolo_user_input)<=200):
            self.ids.fsi_bolo.foreground_color = 0,0,0,1
            self.fsi_bolo_verificato = 1
        else:
            self.ids.fsi_bolo.foreground_color = 1,0,0,1
            self.fsi_bolo_verificato = 0
        #I:C:
        if(len(self.r_ic_bolo_user_input)>0 and int(self.r_ic_bolo_user_input)>=10 and int(self.r_ic_bolo_user_input)<=200):
            self.ids.r_ic_bolo.foreground_color = 0,0,0,1
            self.r_ic_bolo_verificato = 1
        else:
            self.ids.r_ic_bolo.foreground_color = 1,0,0,1
            self.r_ic_bolo_verificato = 0
        #CARBOIDRATI:
        if(len(self.carboidrati_user_input)>0 and int(self.carboidrati_user_input)<=200):# and int(str(self.carboidrati_user_input)[:1])!=0):
            self.ids.carboidrati.foreground_color = 0,0,0,1
            self.carboidrati_verificato = 1
        else:
            self.ids.carboidrati.foreground_color = 1,0,0,1
            self.carboidrati_verificato = 0
        #INSULINA ATTIVA:
        if(len(self.insulina_attiva_user_input)>0 and float(self.insulina_attiva_user_input)<=20):
            self.ids.insulina_attiva.foreground_color = 0,0,0,1
            self.insulina_attiva_verificata = 1
        else:
            self.ids.insulina_attiva.foreground_color = 1,0,0,1
            self.insulina_attiva_verificata = 0

        #Se tutti i campi sono stati compilati attiva il bottone salva
        if(self.glicemia_verificata == 1 and self.fsi_bolo_verificato == 1 and self.r_ic_bolo_verificato == 1 and self.carboidrati_verificato == 1 and self.insulina_attiva_verificata == 1):
            self.ids.calcola_insulina.disabled = False
        else:
            self.ids.calcola_insulina.disabled = True

    #Funzione che calcola il bolo e lo inserisce all'interno della variabile inizializzata nell'init ("self.bolo_richiesto"), che verrà
    #stampata tramite il text nel label del popup "BoloPopup"
    def calcola_bolo(self):

        #Memorizzo prima fsi e ic aggiornati (se l'utente li ha cambiati)
        self._app.my_app_params.params['fsi'] = str(self.fsi_bolo_user_input)
        self._app.my_app_params.params['ic'] = str(self.r_ic_bolo_user_input)
        self._app.my_app_bolo.dati_bolo['insulina_attiva'] = float(self.insulina_attiva_user_input)

        #Se non vengono inseriti carboidrati --> Correzione glicemia. Se vengono inseriti carboidrati --> Insulina per tot carboidrati + eventuale correzione
        # (Prendiamo le prime 2 cifre dopo la virgola con round)
        if(int(self.carboidrati_user_input)==0):
            self.bolo_richiesto = (int(self.glicemia_user_input) - 110)/ int(self.fsi_bolo_user_input)
            self._app.my_app_bolo.dati_bolo['bolo_richiesto'] = round(self.bolo_richiesto,2) #Prime due cifre dopo la virgola
            self.bolo_finale = float(self._app.my_app_bolo.dati_bolo['bolo_richiesto']) - float(self._app.my_app_bolo.dati_bolo['insulina_attiva'])
            self._app.my_app_bolo.dati_bolo['bolo_finale'] = round(self.bolo_finale,2) #Prime due cifre dopo la virgola

            if(self._app.my_app_bolo.dati_bolo['bolo_richiesto'])<=0:#Se il bolo da 0 o meno, il bolo richiesto ed il bolo finale saranno 0
                self._app.my_app_bolo.dati_bolo['bolo_richiesto'] = 0
                self._app.my_app_bolo.dati_bolo['bolo_finale'] = 0
        else:
            #Bolo con correzione            
            if(int(self.glicemia_user_input) > 110):
                self.bolo_richiesto = int(self.carboidrati_user_input)/int(self._app.my_app_params.params['ic'])
                self.correzione = (int(self.glicemia_user_input) - 110)/ int(self.fsi_bolo_user_input)
                self.bolo_finale = (float(self.bolo_richiesto) + float(self.correzione)) - float(self.insulina_attiva_user_input)
                self._app.my_app_bolo.dati_bolo['correzione'] = round(self.correzione,2)
            #Bolo senza correzione
            else:
                self.bolo_richiesto = int(self.carboidrati_user_input)/int(self._app.my_app_params.params['ic'])
                self.bolo_finale = float(self.bolo_richiesto) - float(self.insulina_attiva_user_input)

            self._app.my_app_bolo.dati_bolo['bolo_richiesto'] = round(self.bolo_richiesto,2) #Prime due cifre dopo la virgola
            self._app.my_app_bolo.dati_bolo['bolo_finale'] = round(self.bolo_finale,2) #Prime due cifre dopo la virgola

            if(self._app.my_app_bolo.dati_bolo['bolo_richiesto'])<=0:#Se il bolo da 0 o meno, il bolo richiesto ed il bolo finale saranno 0
                self._app.my_app_bolo.dati_bolo['bolo_richiesto'] = 0
                self._app.my_app_bolo.dati_bolo['bolo_finale'] = 0
        
        #Salvo i dati nello storage
        self._app.my_app_params.save_params_to_storage()

        #Pulisco i vari textinput
        self.clear_textinput()
    
    #Funzione che riporta vuoti i textinput
    def clear_textinput(self):
        self.bolo_screen.ids.glicemia.text = ""
        self.bolo_screen.ids.carboidrati.text = ""
        self.bolo_screen.ids.insulina_attiva.text = ""