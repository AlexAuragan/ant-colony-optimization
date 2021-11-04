import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_path = os.path.dirname(os.path.realpath(path))
if not dir_path in sys.path :
    sys.path.append(dir_path)
from Classes.Classe_Case import Case

class Terrain():
    """Contient tous les objets présents:
        -Fourmiliere"""
    def __init__(self, var_score, canevas):
        self.tk_var_score = var_score
        self.temps = 0
        self.Liste_Fourmiliere = []
        self.Canevas = canevas
        self.cases_a_update = set()
        self.Liste_Cases = [[Case(x,y,self) for y in range(80)] #Fait la matrice associée au terrain
                            for x in range(120)]
        for i in range(80):#Définie les murs, ici les contours du terrain
            self.Liste_Cases[0][i].opacite = 1
            self.Liste_Cases[0][i].a_update()
            self.Liste_Cases[119][i].opacite = 1
            self.Liste_Cases[119][i].a_update()
        for i in range(120) :
            self.Liste_Cases[i][0].opacite = 1
            self.Liste_Cases[i][0].a_update()
            self.Liste_Cases[i][79].opacite = 1 
            self.Liste_Cases[i][0].a_update()
        self.update_cases()
        self.critere_arret = False
        self.score = 0
        
        

    def __str__(self) :
        return "Terrain de 120 cases sur 80, contient {0} fourmilières".format(len(self.Liste_Fourmiliere))

    def next(self) : #Fait agir chaque fourmis
        self.score = 0
        for fml in self.Liste_Fourmiliere :
            fml.agis()
            self.score += fml.score
        self.tk_var_score.set(self.score)
        self.temps += 1
        self.update_cases()
        

    def maj_spin(self,spin_fml,spin_fr, main_fml):
        for fml in self.Liste_Fourmiliere :
            if fml.name == spin_fml.get() :
                main_fml = fml
        spin_fr.config(values= [frm.id for frm in main_fml.Liste_Fourmis])

    def check_odeurs(self) :
        for fml in self.Liste_Fourmiliere :
            for od in fml.Liste_Odeur :
                od.evalue()

    def run(self) :
        nb_fr = 0
        while not self.critere_arret :
            if self.temps > 1000 :
                self.critere_arret = True
            if nb_fr <= 20 :
                for fml in self.Liste_Fourmiliere :
                    fml.spawn("Fourmi exploratrice")
                nb_fr += 1
            self.next()
            self.check_odeurs()


    def load(self):
        for i in range(len(self.Liste_Cases)):
            for j in range(len(self.Liste_Cases[0])) :
                if self.Liste_Cases[i][j].opacite == 1 :
                    self.Liste_Cases[i][0].a_update()

    def update_cases(self) :
        for case in self.cases_a_update :
            case.update_couleur()
        self.cases_a_update = set()
        self.Canevas.update()