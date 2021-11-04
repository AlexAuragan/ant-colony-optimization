import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_path = os.path.dirname(os.path.realpath(path))
if not dir_path in sys.path :
    sys.path.append(dir_path)

from Classes.Fourmis.Fourmis_basique import Fourmi
from Classes.Fourmis.Fourmis_exploratrice import Fourmi_Exploratrice
from Classes.Fourmis.Fourmis_optimisatrice import Fourmi_Optimale
from Fonctions.Fourmis_function import potentiels
    

class Fourmiliere() :
    """Objet fourmillière qui créer des fourmis"""
    def __init__(self,Terrain,name) :
        self.name = name
        self.Terrain = Terrain
        self.coo = [50,50]
        self.Case = Terrain.Liste_Cases[self.coo[0]][self.coo[1]]
        self.Case.fourmiliere = 1
        self.Liste_Fourmis = []
        for i in potentiels(self.coo,self.Terrain):
            case_autour = self.Terrain.Liste_Cases[i[0]][i[1]]
            case_autour.fourmiliere = 2
            case_autour.a_update()
        self.Case.a_update()
        self.Terrain.update_cases()
        self.Liste_Odeur = []
        self.score = 0

    def __str__(self):
        return "Fourmilière {0} sur {1} à la position {3} qui contient {4} fourmis.".format(self.name, self.Terrain, self.coo, len(self.Liste_Fourmis) )

    def spawn(self, type_fourmi = "Fourmi normale") :#Fait apparaitre une fourmi
        n = len(self.Liste_Fourmis)
        id = n

        if type_fourmi == "Fourmi normale" :
            fourmi = Fourmi(Terrain = self.Terrain,Fourmiliere = self,id =id,coo_case = self.coo, behavior = "search food")
        elif type_fourmi == "Fourmi exploratrice" :
            fourmi = Fourmi_Exploratrice(Terrain = self.Terrain,Fourmiliere = self,id =id,coo_case = self.coo, behavior = "search food")
        elif type_fourmi == "Fourmi optimisatrice" :
            fourmi = Fourmi_Optimale(Terrain = self.Terrain,Fourmiliere = self,id =id,coo_case = self.coo, behavior = "search food")
        self.Case.Liste_Fourmis.append(fourmi)
        self.Liste_Fourmis.append(fourmi)
        
    def agis(self) :
        for fourmi in self.Liste_Fourmis :
            fourmi.behave()

    def fourmi_rentree(self, fourmi):
        if fourmi.id >= 5 :
            self.spawn("Fourmi optimisatrice")
        else :
            self.spawn("Fourmi exploratrice")
    
