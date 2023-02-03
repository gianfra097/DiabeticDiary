from ast import NotIn
from urllib import request
from kivy.utils import _get_platform
from kivy.config import Config
from pkg_resources import get_platform

#Importo le altre pagine per utilizzarle nello ScreenManager e quindi spostarmi di schermata
from homepage import HomePage
from bolo import Bolo
from allarmi import Allarmi
from attivita import Attivita
from dati import Dati

if _get_platform() not in ["android", "ios"]:
    Config.set("graphics", "width", 368)
    Config.set("graphics", "height", 712)
if _get_platform() == "android":
    import android.activity
    from auth import AndroidOAuth
import kivy
from kivy.app import App

from settings import DiabeticDiarySettings
from params import DiabeticDiaryParams
from stato_attivita import DiabeticDiaryStateActivity
from graph import Graph

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import SpinnerOption
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import Image

#Nel main creo la classe login
class LoginPage(Screen):
    pass

#Creo uno spinner da decorare
class DiabeticStdSpinner(SpinnerOption):
    pass

#Creo un boxlayout e lo rendo button in modo da decorarlo
class DiabeticStdButton(ButtonBehavior, BoxLayout):
    button_text = StringProperty("NO_TEXT")

class InfoButton(ButtonBehavior, BoxLayout):
    button_text = StringProperty("NO_TEXT")

class BackButton(ButtonBehavior, Image):
    pass

class GraphButton(ButtonBehavior, Image):
    pass

class DiabeticDiaryApp(App):
    egvs_data = StringProperty("")
    egvs_data_trend = StringProperty("")

    #Metodo di callback utilizzato come callback per evento "on_keyboard" bindato nel metodo build dell'app
    def key_input(self,window,key,scancode,codepoint,modifier):
        if key == 27:
            print("Ho premuto back")
            self.history_back()
            return True
        else:
            return False

    #Salvo la pagina corrente e cambio pagina richiesta
    def cambia_pagina(self,pagina):
        self.percorso.append(self.screen_manager.current)
        self.screen_manager.current = pagina

    #Torno all'ultima pagina visitata (precedente a quella attuale)
    def history_back(self):
        self.screen_manager.current = self.percorso.pop()

    #Funzione dove passiamo i paramentri all'oggetto AndroidOAuth(come specificato sulla classe AndroidOAuth)
    def build(self):
        Window.bind(on_keyboard=self.key_input)
        Window.softinput_mode = "below_target"
        self.my_app_settings =  DiabeticDiarySettings()#Istanzio oggetto settings
        self.my_app_settings.load_settings_from_storage()#Richiamo metodo per caricare i settings
        self.my_app_params =  DiabeticDiaryParams()#Istanzio oggetto params
        self.my_app_params.load_params_from_storage()#Richiamo metodo per caricare i params
        self.my_app_state_activity = DiabeticDiaryStateActivity()
        self.my_app_bolo = Bolo()
        self.my_app_attivita = Attivita()
        self.my_app_homepage = HomePage()
        self.my_app_graph = Graph()
        self.auth = AndroidOAuth(
            "https://sandbox-api.dexcom.com/v2/oauth2/login",
            "https://sandbox-api.dexcom.com/v2/oauth2/token",
            "J0BPeezCjuIxwhvGxwaGOeB59igF8ORP",
            "me.gianfranco.diabeticdiary:/oauth2redirect",
        ) 
        self.auth.load_authentication_data_from_storage() 
        self.result_callbacks = [] 
        if _get_platform() == "android":
            android.activity.bind(
                on_activity_result=self.android_activity_result_handler
        )
        self.request_egvs_data_from_dexcom()#Prima richiesta lettura dati
        self._update_egvs_data_clock = Clock.schedule_interval(lambda dt: self.request_egvs_data_from_dexcom(), 1*60)#Richiesta lettura dati ogni minuto
        self.contatore = 0#Contatore che viene aumentato e serve per leggere i dati successivi
        
        #ScreenManager controlla lo spostamento tra le schermate. Aggiungo quindi la schermata HomePage per potermi spostare su di essa
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginPage(name='LoginPage'))
        self.screen_manager.add_widget(HomePage(name='HomePage'))
        self.screen_manager.add_widget(Bolo(name='Bolo'))
        self.screen_manager.add_widget(Allarmi(name='Allarmi'))
        self.screen_manager.add_widget(Attivita(name='Attivita'))
        self.screen_manager.add_widget(Dati(name='Dati'))
        self.screen_manager.add_widget(Graph(name='Graph'))

        self.percorso = [] 

        return self.screen_manager

    #Settiamo un requestCode (nel caso della chiamata effettuata da first_login e' 200). Tramite questo, selezioniamo la callback da chiamare.
    def android_activity_result_handler(self, requestCode, resultCode, intent):
        for callback in self.result_callbacks:
            if callback["code"] == requestCode:
                callback["callback"](intent)

    #Inizializzo la richiesta che verra' avviata tramite il click del bottone (kv file)
    def request(self):
        if self.auth.is_access_token_valid():#Se l'access token e' valido, al click "accedi", passa alla homepage
            self.cambia_pagina('HomePage')
            print("Token valido")
            print(self.auth.token_storage)
        else:#Se l'access token non e' valido, quindi scaduto o mai generato, vado a configurare il servizio di autenticazione (verifico se e' un prima login o richiedo nuovo access token attraverso il refresh token)
            print("Token non valido")
            self.auth.configure()
            if self.auth.is_first_login():
                self.auth.first_login()
            else:
                self.auth.refresh_token()

    #Metodo di richiesta dei valori da dexcom
    def request_egvs_data_from_dexcom(self):
        def on_success(request,result):
            self.egvs_data = str(result['egvs'][self.contatore]['value'])#Leggo valore corrente
            self.egvs_data_trend = str(result['egvs'][self.contatore]['trend'])#Leggo valore corrente
            self.my_app_homepage.update_egvs_value()#Richiamo funzione della homepage per modificare il cerchio del valore
            self.my_app_graph.update_graph()
            self.contatore+=1#Aumento contatore per leggere poi il valore successivo
            
        def on_failure(request,result):
            pass

        def on_error(request,error):
            pass
        
        #Dati per la richiesta
        req = UrlRequest(
            "https://sandbox-api.dexcom.com/v2/users/self/egvs?startDate=2020-04-05T17:00:00&endDate=2020-07-04T17:00:00",
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error,
            req_headers={"authorization": f"Bearer {self.auth.token_storage['access_token']}"},
            method="GET",
            debug=True,
        )

if __name__ == "__main__":
    DiabeticDiaryApp().run()
