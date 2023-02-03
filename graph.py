from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib
import matplotlib.pyplot as plt
from kplot.backend_kivyagg import FigureCanvasKivyAgg
import numpy as np

plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0.0),  #Sfondo esterno rosso con opacità 0%(Quindi senza sfondo)
    "axes.facecolor":    (1.0, 1.0, 1.0, 1.0),  #Sfondo interno bianco
})

#Inizializzo il grafico con 0,0, linea nera e scritta glicemia a sinistra
x = [0]
y = [0]
plt.plot(x,y,color="black")
plt.ylabel("Glicemia")

class Graph(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self._app = App.get_running_app()
        self.contatore = 0 #Mi servira' per la x
        self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def update_graph(self):
        plt.rcParams.update({
            "figure.facecolor":  (1.0, 0.0, 0.0, 0.0),  #Sfondo esterno rosso con opacità 0%(Quindi senza sfondo)
            "axes.facecolor":    (1.0, 1.0, 1.0, 1.0),  #Sfondo interno bianco
        })

        #Aggiorno x e y
        self.contatore += .1
        x.append(self.contatore)
        y.append(int(self._app.egvs_data))
        plt.cla() #Elimino linea o punto precedente
        #plt.scatter(x,y) #Disegno il punto
        plt.plot(x,y,color="black") #Disegno linea
        plt.ylabel("Glicemia")
        plt.draw()