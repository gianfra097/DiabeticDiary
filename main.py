from ast import NotIn
from urllib import request
from kivy.utils import _get_platform
from kivy.config import Config                  
if _get_platform() not in ["android", "ios"]:
    Config.set("graphics","width",368)
    Config.set("graphics","height",712)
if _get_platform() == "android":
    import android.activity
import kivy
from kivy.app import App
from auth import AndroidOAuth

class DiabeticDiaryApp(App):
    def build(self):
        self.result_callbacks = []
        if _get_platform() == "android":
            android.activity.bind(on_activity_result=self.android_activity_result_handler) #Passiamo come callback la funzione android_activity_result_handler all'evento on_activity_result gestito dal tool android.activity di kivy

    def android_activity_result_handler(self, requestCode, resultCode, intent):
        for callback in self.result_callbacks:
            if callback['code'] == requestCode:
                callback['callback'](intent)

    def request(self):  #Inizializzo la richiesta che verra' avviata tramite il click del bottone (kv file)
        self.auth = AndroidOAuth('https://sandbox-api.dexcom.com/v2/oauth2/login','https://sandbox-api.dexcom.com/v2/oauth2/token','J0BPeezCjuIxwhvGxwaGOeB59igF8ORP','me.gianfranco.diabeticdiary:/oauth2redirect')
        self.auth.configure()
        self.auth.build_request()

if __name__=='__main__':
    DiabeticDiaryApp().run()

