from ast import NotIn
from kivy.utils import _get_platform
from kivy.config import Config  #Documentazione
if _get_platform() not in ["android", "ios"]:
    Config.set("graphics","width",368)
    Config.set("graphics","height",712)
import kivy
from kivy.app import App

class DiabeticDiaryApp(App):
    pass

DiabeticDiaryApp().run()
