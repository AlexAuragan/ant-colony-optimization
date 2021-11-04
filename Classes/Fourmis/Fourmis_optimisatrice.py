import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_path = os.path.dirname(os.path.realpath(path))
if not dir_path in sys.path :
    sys.path.append(dir_path)
from Classes.Fourmis.Fourmis_basique import Fourmi
from Fonctions.Fourmis_function import convert_cases_angle, convert_angle_case, distance_infinie
from Fonctions.Selection import select_odeur_in_case
from Classes.Classe_Odeur import Odeur
from math import pi
from random import shuffle

class Fourmi_Optimale(Fourmi) :
    def __init__(self,Fourmiliere, Terrain, id, coo_case, behavior) :
        Fourmi.__init__(self,Fourmiliere,Terrain,id,coo_case, behavior)

    def suit_chemin(self, odeur_type, odeur_a_deposer = []) :
        if self.Case.Liste_Odeur[odeur_type] == [] :
            return False 
        next_case1 = select_odeur_in_case(self.Case, self.angle, odeur_type)
        if next_case1 == None :
            return False
        coo0 = self.coo_case
        next_case2 = select_odeur_in_case(self.Terrain.Liste_Cases[next_case1[0]][next_case1[1]], (self.angle-pi)%(2*pi), odeur_type)
        if next_case2 == None:
            self.deplace(next_case1, convert_cases_angle(self.coo_case,next_case1)) 
            angle_deposé = convert_cases_angle(self.coo_case,coo0)
            for odeur_deposee in odeur_a_deposer :
                self.depose_odeur(odeur_deposee[0],(angle_deposé + odeur_deposee[1])%(2*pi))
            return True
        if distance_infinie(coo0, self.Terrain.Liste_Cases[next_case2[0]][next_case2[1]].coo ) == 1 :
            self.deplace(next_case2, convert_cases_angle(self.coo_case,next_case2)) 
            angle_deposé = convert_cases_angle(self.coo_case,coo0)
            for odeur_deposee in odeur_a_deposer :
                self.depose_odeur(odeur_deposee[0],(angle_deposé + odeur_deposee[1])%(2*pi))
            return True
        else :
            self.deplace(next_case1, convert_cases_angle(self.coo_case,next_case1)) 
        angle_deposé = convert_cases_angle(self.coo_case,coo0)
        for odeur_deposee in odeur_a_deposer :
            self.depose_odeur(odeur_deposee[0],(angle_deposé + odeur_deposee[1])%(2*pi))
        return True 