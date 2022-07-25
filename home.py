KV = '''
#:import rgba kivy.utils.get_color_from_hex

Screen:

    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'images/BackgroundApp.png'

    Image: 
        source: 'images/prova1.png'
        size_hint_y: 0.3 
        allow_stretch: True
        pos_hint: {"x": 0, "y": 0.68}

'''

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.network.urlrequest import UrlRequest

class DiabeticDiary(MDApp):
    #Creo la finestra iniziale dell'app
    def build(self):                   
        self.title = "DiabeticDiary"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

DiabeticDiary().run()
