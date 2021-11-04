import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_path = os.path.dirname(os.path.realpath(path))
if not dir_path in sys.path :
    sys.path.append(dir_path)
from Classes.Fourmis.Fourmis_basique import Fourmi
from Fonctions.Fourmis_function import convert_cases_angle, convert_angle_case
from Fonctions.Selection import select_odeur_in_case, select_case_around, look_around
from Classes.Classe_Odeur import Odeur
from random import shuffle
from math import pi
    

class Fourmi_Exploratrice(Fourmi) :
    def __init__(self,Fourmiliere, Terrain, id, coo_case, behavior) :
        Fourmi.__init__(self,Fourmiliere,Terrain,id,coo_case, behavior)
        self.nb_pas = 0
        self.distance_food = 0
        self.behavior = "wander"

    def behave(self):#Agis
        self.nb_pas += 1
        if self.nb_pas > 100 and self.transporte == [] :
            self.go_home()
        elif self.Case.food >= 1 and self.behavior == "wander":
            self.take_food(self.coo_case)
            self.behavior = "found food"
        elif self.behavior == "wander" :
            self.wander()
        elif self.behavior == "go home" :
            self.go_home()
        elif self.behavior == "found food" :
            self.found_food()


    def ponderation(self):
        if self.transporte != [] :
            return 1/(self.distance_food/50)
        if self.nb_pas <= 50 :
            return 1
        elif self.nb_pas > 100 :
            self.behavior = "go home"
            return 0 
        else :
            return 1/(self.nb_pas/50)
                
    def depose_odeur(self,odeur_type,direction) :
        shuffle(self.Case.Liste_Odeur[odeur_type])
        for i in range(len(self.Case.Liste_Odeur[odeur_type])-1,-1,-1) : #Cherche une odeur semblable
            odeur = self.Case.Liste_Odeur[odeur_type][i]
            if not odeur.evalue() == False :
                if odeur.Fourmiliere == self.Fourmiliere : #Si la fourmi trouve déjà une odeur similaire...
                    if convert_angle_case(direction,self.coo_case) == odeur.next_case : # ...elle regarde si l'odeur pointe vers la même case.
                        if odeur_type == "home" :
                            poid = 1
                        else : 
                            poid = self.ponderation()
                        odeur.valeur += poid
                        return
        #S'il n'y a pas d'odeur semblable, dépose une odeur 
        Odeur_déposée = Odeur(Case = self.Case,Fourmiliere = self.Fourmiliere,type =odeur_type,direction = direction)
        Odeur_déposée.valeur = self.ponderation()
        self.Fourmiliere.Liste_Odeur.append(Odeur_déposée)

    def take_food(self, casetrouvee) :
            self.angle  = (self.angle + pi)%(2*pi)
            self.behavior = "found food"
            self.transporte.append("food")
            self.Terrain.Liste_Cases[casetrouvee[0]][casetrouvee[1]].food -= 1
            self.Case.a_update()
            #Retien la disance à la nourriture
            self.distance_food = self.nb_pas