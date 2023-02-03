from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

class Allarmi(Screen):
    range_min = NumericProperty()
    range_max = NumericProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self._app = App.get_running_app()

    #Se modalità attività è attiva, aggiorna la scritta "attivato" o "disattivato" sotto il range e rendi i valori di allarme
    #non modificabili, in quanto vengono modificati automaticamente a 140-180 (in modo momentaneo), altrimenti torna tutto normale
    def on_enter(self):
        if self._app.my_app_state_activity.attivita_storage['stato']:
            self.ids.label_stato_attivita.text = "(Stato attività ATTIVATA)"
            self.ids.value_ipo.disabled = True
            self.ids.value_ipo.text = str(140)
            self.ids.value_iper.disabled = True
            self.ids.value_iper.text = str(180)
            self.ids.range_area.text = "140mg/dL - 180mg/dL"
        elif self._app.my_app_state_activity.attivita_storage['stato'] == False and self._app.my_app_state_activity.attivita_storage['cambia_testo'] == 1:
            self.ids.label_stato_attivita.text = "(Stato attività DISATTIVATA)"
            self.ids.value_ipo.disabled = False
            self.ids.value_ipo.text = str(self._app.my_app_settings.settings['range_min'])
            self.ids.value_iper.disabled = False
            self.ids.value_iper.text = str(self._app.my_app_settings.settings['range_max'])
            self.ids.range_area.text = str(self._app.my_app_settings.settings['range_min'])+"mg/dL - "+str(self._app.my_app_settings.settings['range_max'])+"mg/dL"

    
    #Funzione che verifica se il valore inserito può essere considerato nell'intervallo (es: più di 3 numeri non vanno bene e ipo ed iper hanno dei range)
    def verifica_valore(self):
        #Inserisco il testo all'interno della variabile ipo_user_input
        self.allarmi_screen = self._app.root.get_screen('Allarmi')
        self.ipo_user_input = self.allarmi_screen.ids.value_ipo.text
        self.iper_user_input = self.allarmi_screen.ids.value_iper.text
        
        #Verifico che siano massimo 3 numeri, e che siano compresi in un range minimo/massimo, altrimenti il testo diventa rosso e viene disabilitato il bottone
        #IPO:
        if(len(self.ipo_user_input)>1 and len(self.ipo_user_input)<4 and int(self.ipo_user_input)>=75 and int(self.ipo_user_input)<=100):
            self.ids.value_ipo.foreground_color = 0,0,0,1
            self.ids.salva_allarmi.disabled = False
            self.ipo_verificata=1 #Se la condizione ipo e' vera, crea una variabile che permette di attivare il bottone se anche la condizione dell'iper e' vera
        else:
            self.ids.value_ipo.foreground_color = 1,0,0,1
            self.ids.salva_allarmi.disabled = True
            self.ipo_verificata=0 #Altrimenti disattiva bottone anche se la condizione iper e' verificata
        #IPER:
        if(len(self.iper_user_input)>1 and len(self.iper_user_input)<4 and int(self.iper_user_input)>=160 and int(self.iper_user_input)<=280):
            self.ids.value_iper.foreground_color = 0,0,0,1
            if(self.ipo_verificata == 1):
                self.ids.salva_allarmi.disabled = False
        else:
            self.ids.value_iper.foreground_color = 1,0,0,1
            self.ids.salva_allarmi.disabled = True

        #Se uno pieno e uno vuoto, si può salvare, in quanto si modifica un allarme mantenendo invariato l'altro

    def salva_allarmi(self):
        #Se viene cliccato il bottone salva, associo alle variabili "range_min" e "range_max" i valori inseriti dall'utente
        self.range_min = self.ipo_user_input
        self.range_max = self.iper_user_input
        #Modifico i valori nel dizionario con i valori appena salvati all'interno dellw variabili (cioè quelli scritto dall'utente)
        self._app.my_app_settings.settings['range_min'] = int(self.range_min)
        self._app.my_app_settings.settings['range_max'] = int(self.range_max)
        #Salvo i dati nello storage
        self._app.my_app_settings.save_settings_to_storage()
        #Aggiorno il testo nascosto nei quadrati (textinput) ed anche il range personalizzato
        self.ids.value_ipo.hint_text = str(self._app.my_app_settings.settings['range_min'])
        self.ids.value_iper.hint_text = str(self._app.my_app_settings.settings['range_max'])
        self.ids.range_area.text = str(self._app.my_app_settings.settings['range_min'])+"mg/dL - "+str(self._app.my_app_settings.settings['range_max'])+"mg/dL"