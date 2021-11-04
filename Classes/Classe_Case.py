import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_path = os.path.dirname(os.path.realpath(path))
if not dir_path in sys.path :
    sys.path.append(dir_path)

from Classes.Fourmis.Fourmis_basique import Fourmi
from Classes.Fourmis.Fourmis_exploratrice import Fourmi_Exploratrice
from Classes.Fourmis.Fourmis_optimisatrice import Fourmi_Optimale


class Case() :
    def __init__(self,x,y,Terrain):
        self.coo = [x,y]
        self.Terrain = Terrain
        self.Liste_Odeur = {"home" : [], "food" : [] }
        self.Canevas = self.Terrain.Canevas
        self.food = 0
        self.fourmiliere = 0
        self.Liste_Fourmis = []
        self.importance = {"home":0,"food":0}
        self.opacite = 0
        self.couleur = self.Terrain.Canevas.create_rectangle(x*10,y*10,(x+1)*10,(y+1)*10,fill = "purple")
        [self.couleur1, self.couleur2] = self.Terrain.Canevas.create_cross(x*10,y*10,10,width = 2,fill = "purple")
        self.couleur3 = self.Terrain.Canevas.create_circle(x*10+5,y*10+5,3, fill = "purple", outline = "")

        self.Canevas.itemconfigure(self.couleur, state='hidden')
        self.Canevas.itemconfigure(self.couleur1, state='hidden')
        self.Canevas.itemconfigure(self.couleur2, state='hidden')
        self.Canevas.itemconfigure(self.couleur3, state='hidden')

    def __str__(self) :
        liste = [fourmi.id for fourmi in self.Liste_Fourmis]
        return "La case {0} qui contient {1} ".format(self.coo, liste)
   
   
    def evalue_case(self):
        for odeur_type in self.importance :
            val = 0
            for i in range(len(self.Liste_Odeur[odeur_type])-1,-1,-1): #Cherche une odeur semblable
                if not self.Liste_Odeur[odeur_type][i].evalue() == False :
                    val += self.Liste_Odeur[odeur_type][i].evalue()
            self.importance[odeur_type] = val       

    def update_couleur(self):
        
        if self.opacite == 1 :
            self.change_couleur_case("black")
        elif self.Liste_Fourmis != [] :
            self.change_couleur_case("blue")
        elif self.fourmiliere == 1 :
            self.change_couleur_case("black")
        elif self.fourmiliere == 2 :
            self.change_couleur_case("brown")
        elif self.food > 0 :
            self.change_couleur_case("orange")
        elif self.Liste_Odeur["food"] != [] :
            self.change_couleur_case("green")
        elif self.Liste_Odeur["home"] != [] :
            self.change_couleur_case("pink")
        else :
            self.Canevas.itemconfig(self.couleur,state='hidden')

        fourmi_type = 0
        fourmi_avec_nourriture = 0
        for fourmi in self.Liste_Fourmis :
            if isinstance(fourmi, Fourmi_Exploratrice) :
                fourmi_type = 1
            elif isinstance(fourmi, Fourmi_Optimale) :
                fourmi_type = 2
            
            if fourmi.transporte != [] :
                fourmi_avec_nourriture = 1

        if fourmi_type == 1 :
            self.Canevas.itemconfig(self.couleur1, fill = "green", state = 'normal')
            self.Canevas.itemconfig(self.couleur2, fill = "green", state = 'normal')
        elif fourmi_type == 2 :
            self.Canevas.itemconfig(self.couleur1, fill = "black", state = 'normal')
            self.Canevas.itemconfig(self.couleur2, fill = "black", state = 'normal')
        else : 
            self.Canevas.itemconfig(self.couleur1, state = 'hidden')
            self.Canevas.itemconfig(self.couleur2, state = 'hidden')
        
        if fourmi_avec_nourriture == 1:
            self.Canevas.itemconfig(self.couleur3, fill = "orange", state = 'normal')
        else :
            self.Canevas.itemconfig(self.couleur3, state = 'hidden')

    def change_couleur_case(self, couleur) :
        change_couleur_rectangle(self.Canevas,self.couleur, couleur)

    def a_update(self) :
        self.Terrain.cases_a_update.add(self)

def change_couleur_rectangle(canevas, item, couleur) :
    canevas.itemconfig(item, fill=couleur,state='normal')
