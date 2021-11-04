import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_path = os.path.dirname(os.path.realpath(path))
if not path in sys.path :
    sys.path.append(dir_path)
from Fonctions.Fourmis_function import convert_angle_case

class Odeur() :
    odeur_max = 15
    def __init__(self, Case,Fourmiliere,type,direction,importance = 0, valeur = 1):
        if type == "home" :
            couleur = "pink"
        elif type == "food":
            couleur = "green"
        self.importance = importance
        self.Case = Case
        self.direction = direction
        self.coo_case = Case.coo
        self.Fourmiliere = Fourmiliere
        self.type = type
        self.valeur = valeur
        self.Case.Liste_Odeur[type].append(self)
        self.next_case = convert_angle_case(direction,self.coo_case)
        self.valeur_reelle = 1
        self.t0 = self.Case.Terrain.temps
        self.Canevas = self.Fourmiliere.Terrain.Canevas
        if self.Case.Liste_Fourmis == [] :
            raise NameError("Odeur non règlementaire")
        self.Case.a_update()

    def clear(self):
        self.Case.Liste_Odeur[self.type].remove(self)
        self.Fourmiliere.Liste_Odeur.remove(self)
        self.Case.a_update()

    def evalue(self) :
        DT = self.Case.Terrain.temps - self.t0
        val = self.valeur * ((0.97)**DT)#((0.96)**DT)
        if val > 0.001 :
            self.valeur_reelle = val
            return min(val,self.odeur_max)
        else :
            self.clear()
            return False

