import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_path = os.path.dirname(os.path.realpath(path))
if not dir_path in sys.path :
    sys.path.append(dir_path)

from math import pi
from Fonctions.Fourmis_function import convert_cases_angle, cherche, convert_angle_case, is_odeur_in, potentiels
from Fonctions.Selection import select_odeur_in_case, select_case_around
from Classes.Classe_Odeur import Odeur
from numpy.random import shuffle
from random import random, gauss


class Fourmi() :

    def __init__(self,Fourmiliere,Terrain,id = "",coo_case = [], behavior = "") :
        self.Fourmiliere = Fourmiliere
        self.Terrain = Terrain
        self.coo_case = coo_case
        self.Case = Terrain.Liste_Cases[coo_case[0]][coo_case[1]]
        self.transporte = []
        self.behavior = behavior
        self.id = id
        self.angle = random()*(2*pi)
        self.Case.a_update()
        self.Terrain.update_cases()

    def __str__(self):
        if self.transporte == [] :
            text = "elle ne transporte rien"
        else :
            text = "elle transporte {0}".format(self.transporte[0])
        return "Fourmi {0} appartenant à la fourmilière {1}, elle est à la position {2} et {3}.".format(self.id, self.Fourmiliere.name, self.coo_case,text)

    def destroy(self) :
        if self.transporte == ["food"]:
            self.Fourmiliere.score += 1
        self.Case.Liste_Fourmis.remove(self)
        self.Case.a_update()
        self.Fourmiliere.Liste_Fourmis.remove(self)
        self.Fourmiliere.fourmi_rentree(self)

    def depose_odeur(self,odeur_type,direction) :
        for i in range(len(self.Case.Liste_Odeur[odeur_type])-1,-1,-1): #Cherche une odeur semblable
            odeur = self.Case.Liste_Odeur[odeur_type][i]
            if not odeur.evalue() == False :
                if odeur.Fourmiliere == self.Fourmiliere : #Si la fourmi trouve déjà une odeur similaire...
                    if convert_angle_case(direction,self.coo_case) == odeur.next_case : # ...elle regarde si l'odeur pointe vers la même case.
                        odeur.valeur += 1
                        return 
        self.Fourmiliere.Liste_Odeur.append(Odeur(self.Case,self.Fourmiliere,odeur_type,direction ))
        #S'il n'y a pas d'odeur semblable, dépose une odeur 
      
    def go_home(self) :
        if self.proche_de_la_fourmiliere() :
            return
        self.Case.evalue_case()
        if self.Case.importance["home"] != 0 :
            self.suit_chemin("home") 
            return
        casetrouvee = cherche("home",self)
        if casetrouvee == False :
            self.wander(depose_odeur = False)
            return
        else :
            for i in range(len(self.Case.Liste_Odeur["home"])-1,-1-1) :
                Odeur = self.Case.Liste_Odeur[type][i]
                if not Odeur.evalue() == False :
                    if not Odeur.next_case == self.coo_case :
                        self.angle = Odeur.direction
                        break
            coo1 = self.coo_case
            self.deplace(casetrouvee, self.angle)
            self.depose_odeur("home",convert_cases_angle(casetrouvee,coo1))

    def search_food(self) :
        if self.Case.food >= 1 :
            self.take_food(self.coo_case)
            #self.depose_odeur("food",(self.angle-pi)%(2*pi))
        x = self.coo_case[0]
        y = self.coo_case[1]
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.Terrain.Liste_Cases[x+i][y+j].food >=1  :
                    self.depose_odeur("food",convert_cases_angle([x,y],[x+i,y+j]))
                    self.deplace([x+i,y+j],convert_cases_angle([x,y],[x+i,y+j]))
                    self.depose_odeur("food",convert_cases_angle([x,y],[x+i,y+j]))
                    self.depose_odeur("home",convert_cases_angle([x+i,y+j],[x,y]))
                    return
        coo0 = self.coo_case
        self.Case.evalue_case()
        if self.Case.importance["food"] > 0 :
            self.suit_chemin("food") 
            self.depose_odeur("home",convert_cases_angle(self.coo_case,coo0))
            return 
        #Si la case de la fourmi ne propose aucun chemin     
        else :
            next_case = select_case_around(self.Case, self.angle, odeur_type = "food")
            self.angle = convert_cases_angle(self.coo_case, next_case)
            self.deplace(next_case, (self.angle + gauss(0,0.6))%(2*pi))
            self.depose_odeur("home",convert_cases_angle(self.coo_case,coo0))
      
    def wander(self, depose_odeur = True) :
        if self.Case.food >= 1 :
            self.take_food(self.coo_case)
            #self.depose_odeur("food",(self.angle-pi)%(2*pi))
        x = self.coo_case[0]
        y = self.coo_case[1]
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.Terrain.Liste_Cases[x+i][y+j].food >=1 and not (i == 0 and j == 0) :
                    self.depose_odeur("food",convert_cases_angle([x,y],[x+i,y+j]))
                    self.deplace([x+i,y+j],convert_cases_angle([x,y],[x+i,y+j]))
                    self.depose_odeur("food",convert_cases_angle([x,y],[x+i,y+j]))
                    self.depose_odeur("home",convert_cases_angle([x+i,y+j],[x,y]))
                    return
        mouv = (random() < 0.9)
        if not mouv :
            return
        deviation = gauss(0,0.6) #0.6
        angle = self.angle
        angle += deviation
        angle = angle % (2*pi)
        case_selectionnee = select_case_around(self.Case, self.angle)
        coo1 = self.coo_case
        self.deplace(case_selectionnee,angle)
        if depose_odeur :
            self.depose_odeur("home",direction = convert_cases_angle(case_selectionnee,coo1))

    def found_food(self) : #La fourmie à trouvé de la nourriture et l'a prise
        if self.proche_de_la_fourmiliere() :
            return
        coo1 = self.coo_case
        self.Case.evalue_case()
        if self.suit_chemin("home", odeur_a_deposer = []) : #["home", 0]
            self.depose_odeur("food",convert_cases_angle(self.coo_case,coo1))
            return
        else : 
            next_case = select_case_around(self.Case, self.angle, odeur_type = "home")
            case = self.Terrain.Liste_Cases[next_case[0]][next_case[1]]
            case.evalue_case()
            self.deplace(next_case, self.angle+ gauss(0,0.6)%(2*pi))
            if case.importance["home"] > 0 :
                self.depose_odeur("food",convert_cases_angle(self.coo_case,coo1))
                

    def deplace(self,coo_suivante:list, angle) :
        x,y = self.coo_case
        self.angle = angle
        self.Case.Liste_Fourmis.remove(self)
        self.Case.a_update()
        self.coo_case = coo_suivante
        self.Case=self.Terrain.Liste_Cases[self.coo_case[0]][self.coo_case[1]]
        self.Case.Liste_Fourmis.append(self)
        self.Case.a_update()

    def take_food(self, casetrouvee) :
            self.angle  = (self.angle + pi)%(2*pi)
            self.behavior = "found food"
            self.transporte.append("food")
            self.Terrain.Liste_Cases[casetrouvee[0]][casetrouvee[1]].food -= 1
            self.Case.a_update()
            #if self.coo_case != casetrouvee :
            #    self.depose_odeur("food", convert_cases_angle(self.coo_case,casetrouvee))

    def behave(self):#Agis
        if self.Case.food >= 1 and (self.behavior == "wander" or self.behavior == "search food" ):
            self.take_food(self.coo_case)
            self.behavior = "found food"
        elif self.behavior == "wander" :
            self.wander()
        elif self.behavior == "go home" :
            self.go_home()
        elif self.behavior == "found food" :
            self.found_food()
        elif self.behavior == "search food":
            self.search_food()

    def suit_chemin(self, odeur_type, odeur_a_deposer =[]):
        next_case = select_odeur_in_case(self.Case, self.angle, odeur_type)
        if next_case == None :
            return False
        coo1 = self.coo_case
        self.deplace(next_case, convert_cases_angle(self.coo_case,next_case)) 
        angle_deposé = convert_cases_angle(self.coo_case,coo1)
        for odeur_deposee in odeur_a_deposer :
            self.depose_odeur(odeur_deposee[0],(angle_deposé + odeur_deposee[1])%(2*pi))
        return True

    def proche_de_la_fourmiliere(self):
        if abs(self.coo_case[0]-self.Fourmiliere.coo[0]) <=1 and abs(self.coo_case[1]-self.Fourmiliere.coo[1]) <=1 :
            self.destroy()
            return True
        return False