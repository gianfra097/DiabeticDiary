from ast import NotIn
from kivy.utils import _get_platform
<<<<<<< HEAD
from kivy.config import Config                  
=======
from kivy.config import Config  #Documentazione
>>>>>>> f6b8d0ac688410f180a4502934432f1e6345a6df
if _get_platform() not in ["android", "ios"]:
    Config.set("graphics","width",368)
    Config.set("graphics","height",712)
import kivy
from kivy.app import App
from auth import AndroidOAuth

class DiabeticDiaryApp(App):
<<<<<<< HEAD
    def build(self):
        self.auth = AndroidOAuth('https://sandbox-api.dexcom.com/v2/oauth2/login','https://sandbox-api.dexcom.com/v2/oauth2/token','J0BPeezCjuIxwhvGxwaGOeB59igF8ORP','me.gianfranco.diabeticdiary:/oauth2redirect')
        self.auth.configure()
        self.auth.build_request()


if __name__=='__main__':
    DiabeticDiaryApp().run()
=======
    pass
>>>>>>> f6b8d0ac688410f180a4502934432f1e6345a6df

