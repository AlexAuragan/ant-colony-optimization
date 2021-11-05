from math import pi, exp

def convert_angle_case(angle0,coo_case):#Convertis un angle et une case en la case suivante
    if not type(angle0) == float :
        print(angle0)
        raise NameError("Angle donné n'est pas un nombre")
    angle = (angle0 %( 2*pi))
    if angle < pi/6 :
        coo_case = [coo_case[0]+1,coo_case[1]]
    elif angle < 2*pi/6 :
        coo_case = [coo_case[0]+1,coo_case[1]-1]
    elif angle < 4*pi/6 :
        coo_case = [coo_case[0],coo_case[1]-1]
    elif angle < 5*pi/6 :
        coo_case = [coo_case[0]-1,coo_case[1]-1]
    elif angle < 7*pi/6 :
        coo_case = [coo_case[0]-1,coo_case[1]]
    elif angle < 8*pi/6 :
        coo_case = [coo_case[0]-1,coo_case[1]+1]
    elif angle < 10*pi/6 :
        coo_case = [coo_case[0],coo_case[1]+1]
    elif angle < 11*pi/6 :
        coo_case = [coo_case[0]+1,coo_case[1]+1]
    else :
        coo_case = [coo_case[0]+1,coo_case[1]]
    return coo_case

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

def cherche(odeur,Fourmi) : #Renvois la case avec une odeur précise autours de la fourmis la plus proche depuis sa direction
    angle = Fourmi.angle
    coo_case = Fourmi.coo_case
    L_cases = []
    for coo_case in potentiels(Fourmi.Case.coo,Fourmi.Terrain) :
        Case = Fourmi.Terrain.Liste_Cases[coo_case[0]][coo_case[1]]
        if is_odeur_in(Case,odeur) :
            L_cases.append(Case)
    if len(L_cases) == 0 :
        return False
    elif len(L_cases) == 1 :
        return L_cases[0].coo
    else : 
        L_coo = []
        for case in L_cases :
            L_coo.append(case.coo)
            for coo in L_coo :
                if is_odeur_in(Fourmi.Terrain.Liste_Cases[coo[0]][coo[1]], odeur) == False :
                    raise NameError("Erreur dans la fonction de recherche")
        if (convert_angle_case(angle,coo_case) in L_coo) :
            return convert_angle_case(angle,coo_case)
        elif (convert_angle_case(angle+(pi/6),coo_case) in L_coo) :
            return convert_angle_case(angle+(pi/6),coo_case)
        elif (convert_angle_case(angle-(pi/6),coo_case) in L_coo) :
            return convert_angle_case(angle-(pi/6),coo_case)
        elif (convert_angle_case(angle+(2*pi/6),coo_case) in L_coo) :
            return convert_angle_case(angle+(2*pi/6),coo_case)
        elif (convert_angle_case(angle-(2*pi/6),coo_case) in L_coo) :
            return convert_angle_case(angle-(2*pi/6),coo_case)
        elif (convert_angle_case(angle+(3*pi/6),coo_case) in L_coo) :
            return convert_angle_case(angle+(3*pi/6),coo_case)
        elif (convert_angle_case(angle-(3*pi/6),coo_case) in L_coo) :
            return convert_angle_case(angle-(3*pi/6),coo_case)
        else :
            return L_coo[0]

def potentiels(coo_case,Terrain) :
    """ Créé la liste des case adjacente aux case vivantes"""
    L_potentiels=[]
    i = coo_case
    L_potentiels.append([i[0]-1,i[1]+1])
    L_potentiels.append([i[0],i[1]+1])
    L_potentiels.append([i[0]+1,i[1]+1])
    L_potentiels.append([i[0]-1,i[1]])
    L_potentiels.append([i[0]+1,i[1]])
    L_potentiels.append([i[0]-1,i[1]-1])
    L_potentiels.append([i[0],i[1]-1])
    L_potentiels.append([i[0]+1,i[1]-1]) 
    for var in L_potentiels :
        if Terrain.Liste_Cases[var[0]][var[1]].opacite == 1 :
            L_potentiels.remove(var)
    return L_potentiels

def distance_infinie(c1,c2):
    return max(abs(c1[0]-c2[0]),abs(c1[1]-c2[1]))

import tkinter as tk
def create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = create_circle

def create_cross(self, x, y, taille, **kwargs):
    id1 = self.create_line(x,y+taille, x+taille,y, **kwargs)
    id2 = self.create_line(x,y,x+taille, y+taille, **kwargs)
    return id1,id2 
tk.Canvas.create_cross = create_cross

def is_odeur_in(case, odeur_type, coo_a_eviter = []) :
    for Odeur in case.Liste_Odeur[odeur_type] :
        if not Odeur.evalue == False :
            if Odeur.type == odeur_type :
                if coo_a_eviter == [] or coo_a_eviter != Odeur.next_case :
                    return True
    return False

from random import choice

def random_mouv():
    L = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]
    return choice(L)

def gaussienne(ecart_type, t, centre = 0) :
    #return (1/(ecart_type*sqrt(2*pi)))*exp(-0.5*((t-centre)/ecart_type)**2)
    return exp(-0.5*((t-centre)/ecart_type)**2)