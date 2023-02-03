from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
import plyer

class HomePage(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self._app = App.get_running_app()

    def update_egvs_value(self):
        
        #Creo il percorso
        self.home_screen = self._app.root.get_screen('HomePage')

        #Se il contatore è uguale a 0 (cioè si sta leggendo il primo valore), elimino il cerchio di caricamento
        if(self._app.contatore == 0):
            #Elimino l'immagine di loading in modo che si veda solo il valore
            self.home_screen.ids.loading_box.remove_widget(self.home_screen.ids.loading_image)
            self.home_screen.ids.sintesi_vocale.disabled = False

        #Se stabile carica cerchio stabile, se in salita ecc. carica cerchio diverso
        if(self._app.egvs_data_trend == 'flat'):
            if(int(self._app.egvs_data) <= int(self._app.my_app_settings.settings['range_min'])):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_stabile_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1
            elif(int(self._app.egvs_data) >= int(self._app.my_app_settings.settings['range_max'])):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_stabile_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) < 140):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_stabile_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) > 180):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_stabile_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            else:
                self.home_screen.ids.circle_image.source = 'images/cerchio_stabile.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
        elif(self._app.egvs_data_trend == 'singleUp'):
            if(int(self._app.egvs_data) <= int(self._app.my_app_settings.settings['range_min'])):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_salita2_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1 
            elif(int(self._app.egvs_data) >= int(self._app.my_app_settings.settings['range_max'])):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_salita2_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) < 140):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_salita2_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) > 180):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_salita2_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            else:
                self.home_screen.ids.circle_image.source = 'images/cerchio_salita2.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
        elif(self._app.egvs_data_trend == 'doubleUp'):
            if(int(self._app.egvs_data) <= int(self._app.my_app_settings.settings['range_min'])):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_doppiasalita_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1 
            elif(int(self._app.egvs_data) >= int(self._app.my_app_settings.settings['range_max'])):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_doppiasalita_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) < 140):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_doppiasalita_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) > 180):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_doppiasalita_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            else:
                self.home_screen.ids.circle_image.source = 'images/cerchio_doppiasalita.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1      
        elif(self._app.egvs_data_trend == 'fortyFiveUp'):
            if(int(self._app.egvs_data) <= int(self._app.my_app_settings.settings['range_min'])):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_salita_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1 
            elif(int(self._app.egvs_data) >= int(self._app.my_app_settings.settings['range_max'])):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_salita_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) < 140):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_salita_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) > 180):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_salita_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            else:
                self.home_screen.ids.circle_image.source = 'images/cerchio_salita.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
        elif(self._app.egvs_data_trend == 'singleDown'):
            if(int(self._app.egvs_data) <= int(self._app.my_app_settings.settings['range_min'])):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_discesa2.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1 
            elif(int(self._app.egvs_data) >= int(self._app.my_app_settings.settings['range_max'])):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_discesa2.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) < 140):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_discesa2_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) > 180):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_discesa2_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            else:
                self.home_screen.ids.circle_image.source = 'images/cerchio_discesa2.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
        elif(self._app.egvs_data_trend == 'doubleDown'):
            if(int(self._app.egvs_data) <= int(self._app.my_app_settings.settings['range_min'])):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_doppiadiscesa.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1 
            elif(int(self._app.egvs_data) >= int(self._app.my_app_settings.settings['range_max'])):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_doppiadiscesa.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) < 140):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_doppiadiscesa_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) > 180):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_doppiadiscesa_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            else:
                self.home_screen.ids.circle_image.source = 'images/cerchio_doppiadiscesa.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
        elif(self._app.egvs_data_trend == 'fortyFiveDown'):
            if(int(self._app.egvs_data) <= int(self._app.my_app_settings.settings['range_min'])):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_discesa.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1 
            elif(int(self._app.egvs_data) >= int(self._app.my_app_settings.settings['range_max'])):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_discesa.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) < 140):
                self.home_screen.ids.circle_image.source = 'images/ipo/cerchio_discesa_ipo.png'
                self.home_screen.ids.glucose_value_label.color = 1,1,1,1
            elif(self._app.my_app_state_activity.attivita_storage['stato'] == True and int(self._app.egvs_data) > 180):
                self.home_screen.ids.circle_image.source = 'images/iper/cerchio_discesa_iper.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1
            else:
                self.home_screen.ids.circle_image.source = 'images/cerchio_discesa.png'
                self.home_screen.ids.glucose_value_label.color = 0,0,0,1

    def attiva_sintesi_vocale(self):
        plyer.tts.speak("Il tuo valore è " + self._app.egvs_data)