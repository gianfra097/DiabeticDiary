from ast import NotIn
from kivy.utils import _get_platform
from kivy.config import Config                  
if _get_platform() not in ["android", "ios"]:
    Config.set("graphics","width",368)
    Config.set("graphics","height",712)
import kivy
from kivy.app import App
from auth import AndroidOAuth

class DiabeticDiaryApp(App):
    def build(self):
        pass
    
    def request(): #Inizializzo la richiesta che verra' avviata tramite il click del bottone (kv file)
        self.auth = AndroidOAuth('https://sandbox-api.dexcom.com/v2/oauth2/login','https://sandbox-api.dexcom.com/v2/oauth2/token','J0BPeezCjuIxwhvGxwaGOeB59igF8ORP','me.gianfranco.diabeticdiary:/oauth2redirect')
        self.auth.configure()
        self.auth.build_request()

if __name__=='__main__':
    DiabeticDiaryApp().run()
