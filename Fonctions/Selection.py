from .Fourmis_function import convert_cases_angle, gaussienne, distance_infinie
from math import pi, exp
from random import random


def look_around(case) :
    liste_cases = case.Terrain.Liste_Cases
    Liste = []
    for i in [-1,0,1] :
        for j in [-1,0,1] :
            if i != 0 or j != 0 :
                case_ajoutee = liste_cases[case.coo[0]+i ][case.coo[1]+j ]
                Liste.append(case_ajoutee)
    return Liste #Liste de case

# [0] [1] [2]
# [3] [X] [4]
# [5] [6] [7]

def select_odeur_in_case(case, angle,odeur_type) :
    ''' '''
    for i in range(len(case.Liste_Odeur[odeur_type])-1,-1,-1) :
        case.Liste_Odeur[odeur_type][i].evalue()
    case.evalue_case()
    p = []
    for Odeur in case.Liste_Odeur[odeur_type] :
        if not Odeur.evalue() == False:
            coo = Odeur.next_case
            p.append(Odeur.evalue()*(1-case.Terrain.Liste_Cases[coo[0]][coo[1]].opacite)*pondereration_direction(angle, case.coo, Odeur.next_case))
    if p == [] : #Si la case ne contient pas de chemin
        return None
    liste_ponderation = normer_liste(p)
    odeur_selectionnee = choice(case.Liste_Odeur[odeur_type],1,p = liste_ponderation)
    if case.Terrain.Liste_Cases[odeur_selectionnee.next_case[0]][odeur_selectionnee.next_case[1]].opacite == 1 :
        raise NameError("Case opaque")
    return odeur_selectionnee.next_case

def select_case_around(case_depart, angle, odeur_type = None) :
    cases_possibles = look_around(case_depart)
    liste_ponderation = []
    if odeur_type == None :
        for case in cases_possibles :
            case.evalue_case()
            liste_ponderation.append( pondereration_direction(angle,case_depart.coo, case.coo) *(1-case.opacite))
        select = choice(cases_possibles, 1, p=normer_liste(liste_ponderation))
        return select.coo
    for case in cases_possibles :
        case.evalue_case()
        liste_ponderation.append( (case.importance[odeur_type] + pondereration_direction(angle,case_depart.coo, case.coo)) *(1-case.opacite) )
    select = choice(cases_possibles, 1, p=normer_liste(liste_ponderation))
    return select.coo
    
def pondereration_direction(angle_fourmi,coo_depart, coo_arrivee) :
    if distance_infinie(coo_depart, coo_arrivee) != 1 :
        raise NameError("Ponderation direction deux cases non adjacentes")
    angle_case = convert_cases_angle(coo_depart, coo_arrivee)
    delta = min(2*pi - abs((angle_case - angle_fourmi)%(2*pi)), abs((angle_case - angle_fourmi)%(2*pi)))
    if gaussienne(0.1, delta/pi, centre = 0) == 0 :
        print(delta/pi)
        raise NameError("Gaussienne bof bof")
    return gaussienne(0.1, delta/pi, centre = 0)
    
def normer_liste(L) :
    norme = 0
    for i in L :
        norme += i
    if norme == 0 :
        print(L)
        raise NameError("liste de poids vide")
        #return None
    return [i/norme for i in L]
    
def choice(L,nb_sample,p) :
    rand_nb = random()
    for i in range(len(L)) :
        limit = 0
        for weigt in p[0:i+1] :
            limit += weigt
        if rand_nb < limit :
            return L[i]


    