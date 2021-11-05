import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_path = os.path.dirname(os.path.realpath(path))
if not dir_path in sys.path :
    sys.path.append(dir_path)

from math import pi
from Fonctions.Fourmis_function import gaussienne

def convert_cases_angle(case_départ :list, case_arrivée:list) :
    différence = [case_arrivée[0]-case_départ[0],case_arrivée[1]-case_départ[1]] 
    if différence == [0,0] :
        raise NameError("Erreur, comparaison de deux cases identiques")
    elif  différence == [1,0] :
        return 0*pi/4
    elif différence == [1,-1] :
        return 1*pi/4
    elif différence == [0,-1] :
        return 2*pi/4 
    elif différence == [-1,-1] :
        return 3*pi/4
    elif différence == [-1,0] :
        return 4*pi/4
    elif différence == [-1,1] :
        return 5*pi/4
    elif différence == [0,1] :
        return 6*pi/4
    elif différence == [1,1] :
        return 7*pi/4
    else :
        raise NameError("Erreur, cases non adjacentes")

def pondereration_direction(angle_fourmi,coo_depart, coo_arrivee) :
    angle_case = convert_cases_angle(coo_depart, coo_arrivee)
    delta = abs((angle_fourmi - angle_case)%(2*pi))
    return gaussienne(0.3, delta/pi)
coo_depart = [50,50]
coo_arrivee = [51,50]


from Classes.Classe_Terrain import Terrain
from Fonctions.Selection import select_case_around, pondereration_direction
import tkinter as tk

terrain = Terrain(tk.Canvas())
L_cases = []
L_nb = []
for _ in range(1) :
    case = select_case_around(terrain.Liste_Cases[50][50], 0, terrain, odeur_type = "food")
    for i in range(len(L_cases)) :
        if L_cases[i] == case :
            L_nb[i] += 1
            break
    if not case in L_cases :
        L_cases.append(case)
        L_nb.append(1)
print(L_nb, L_cases)
#L =  look_around(terrain.Liste_Cases[50][50], terrain)
#sprint(( [[pondereration_direction(pi/2,[50,50], case.coo),convert_cases_angle([50,50], case.coo)/(pi/4), case.coo] for case in L]))
