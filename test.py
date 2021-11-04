import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if not path in sys.path :
    sys.path.append(path)
    
from Classes.Classe_Terrain import Terrain

import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if not path in sys.path :
    sys.path.append(path)

from Classes.Classe_Terrain import Terrain
from Classes.Classe_Fourmiliere import Fourmiliere
from Fonctions.Fourmis_function import convert_cases_angle, convert_angle_case
from tkinter import filedialog
import tkinter as tk
from math import pi
from time import sleep, time
from Sauvegarde import load_terrain, save_terrain

class Interface() :
    
    def ouvre_help(self):
        Help = tk.Tk()
        Help.geometry("800x500")
        canevasH = tk.Canvas(master = Help,width = 1200, height = 400,bg="white")
        canevasH.pack(side = tk.TOP)
        canevasH.create_text(250,50,text="Fiche d'aide.",fill = "black")
        canevasH.create_text(250,75,text="blank", fill = "black")
        canevasH.create_text(250,120,text="blank", fill = "black")
        canevasH.create_text(250,150,text="blank", fill = "black")
        but_exitH = tk.Button(Help,text="Exit.", command =Help.destroy)
        but_exitH.pack(side = tk.TOP)


    def ouvre_fourmi(self) :
        helpf = tk.Tk()
        helpf.geometry("800x500")
        fourmi = self.spin_fourmi.get()
        Fourmiliere = self.spin_fml.get() 
        for fml in terrain.Liste_Fourmiliere :
            if fml.name == Fourmiliere :
                Fourmiliere = fml
                break
        for fr in Fourmiliere.Liste_Fourmis :
            if str(fr.id) == str(fourmi) :
                fourmi = fr
                break
        titre = tk.Label(helpf, text="Information sur fourmi "+str(fourmi.id),font="Arial 16 italic")
        titre.pack(side = tk.TOP)
        canevasF = tk.Canvas(helpf,width = 1200, height = 400,bg="white")
        canevasF.pack(side = tk.TOP)
        canevasF.create_text(250,50,text="fourmi id =" + str(fourmi.id),fill = "black")
        canevasF.create_text(250,75,text="fourmi transporte "+str(fourmi.transporte), fill = "black")
        canevasF.create_text(250,100,text="fourmi behavior " + str(fourmi.behavior),fill = "black")
        canevasF.create_text(250,125,text="coordonnées :"+str(fourmi.coo_case), fill = "black")
        canevasF.create_text(250,150,text="fourmilière :"+str(fourmi.Fourmiliere.name), fill = "black")
        canevasF.create_text(250,175,text="angle :"+str(fourmi.angle), fill = "black")
        canevasF.create_text(250,200,text="Liste odeurs")
        j = 0
        for od_type in fourmi.Case.Liste_Odeur :
            for od in fourmi.Case.Liste_Odeur[od_type] :
                od.evalue()
        for (i,od) in enumerate(fourmi.Case.Liste_Odeur["home"]) :
            canevasF.create_text(250,225 +i*25, text = str(od.type) + " : "+str(od.direction))
            j = i
        for (i,od) in enumerate(fourmi.Case.Liste_Odeur["food"]) :
            canevasF.create_text(250,225 +(i+j)*25, text = str(od.type) + " : "+str(od.direction))
    



    def home(self):
        for Fourmiliere in self.terrain.Liste_Fourmiliere :
            for fourmi in Fourmiliere.Liste_Fourmis :
                fourmi.behavior = "go home"
                fourmi.angle = (fourmi.angle -pi) % (2*pi)


    def steps1(self):
        self.terrain.next()   


    def steps20(self):
        for _ in range(20) :
            self.terrain.next()   


    def steps100(self):
        t0 = time()
        for i in range(100) :
            if i%1 == 0 :
                self.terrain.check_odeurs()
            self.terrain.next()
        print(time()-t0)

    
    def steps500(self):
        t0 = time()
        for i in range(500) :
            if i%10 == 0 :
                self.terrain.check_odeurs()
            self.terrain.next()
        print(time()-t0)

    def spawn1(self) :#Test, fait apparaitre une fourmis 
        self.terrain.Liste_Fourmiliere[0].spawn(self.spin_type_fourmi.get())
        self.errain.maj_spin(self.spin_fml,self.spin_fourmi, self.main_fml)


    def spawn10(self) :#Test, fait apparaitre dix fourmis
        for _ in range(10):
            self.terrain.Liste_Fourmiliere[0].spawn(self.spin_type_fourmi.get())
            self.terrain.maj_spin(self.spin_fml,self.spin_fourmi, self.main_fml)

        
    def click_gauche(self,event):
        """Cliquer sur la grille fait apparaitre de la nourriture si le boutton correspondant est enfoncé"""
        radius = int(self.spin_radius.get())
        y = int(event.y//10)
        x = int(event.x//10)
        if self.click == "spawn food" :
            L = []
            for i in range(-radius+1, radius):
                for j in range(-radius+1,radius) :
                    if i*i + j*j < radius*radius/2 and abs(x+i)<120 and abs(y+j) < 80 and x+i >0 and y+j > 0:
                        L.append([x+i,y+j])
            for couple in L :
                x,y = couple[0],couple[1]
                self.terrain.Liste_Cases[x][y].food += 3
                s = self.terrain.Liste_Cases[x][y]
                s.a_update()
        elif self.click == "ouvre_case" :
            fenetreC = tk.Tk()
            fenetreC.geometry("800x500")
            canevasC = tk.Canvas(fenetreC,width = 1200, height = 400,bg="white")
            Case = self.terrain.Liste_Cases[x][y]
            canevasC.pack(side = tk.TOP)
            canevasC.create_text(250,50,text="coordonnées =" + str(Case.coo),fill = "black")
            canevasC.create_text(250,75,text="Liste des odeurs :", fill = "black")
            canevasC.create_text(250,100,text="La case possède une fourmi: "+str(Case.Liste_Fourmis != [] )+" opacité ="+str(Case.opacite)+" et "+str(Case.food)+"nourriture", fill = "black")
            canevasC.create_text(250,10,text=str([[fr.id, type(fr)] for fr in Case.Liste_Fourmis]))
            for (id,odeur) in enumerate(Case.Liste_Odeur["food"]) : 
                if odeur.evalue() != False :
                    canevasC.create_text(200,150 + id*50,text=str(odeur.type)+" de "+str(odeur.Fourmiliere.name), fill = "black")
                    canevasC.create_text(300,150 + id*50,text=str(odeur.coo_case)+" -> " +str(odeur.next_case), fill = "black")
                    canevasC.create_text(400,150 + id*50,text="de valeur :"+str(odeur.evalue()), fill = "black", anchor="w")
            for (id,odeur) in enumerate(Case.Liste_Odeur["home"]) :
                if odeur.evalue() != False :
                    canevasC.create_text(200,150 + (id+len(Case.Liste_Odeur["food"]))*50,text=str(odeur.type)+" de "+str(odeur.Fourmiliere.name), fill = "black")
                    canevasC.create_text(300,150 + (id+len(Case.Liste_Odeur["food"]))*50,text=str(odeur.coo_case)+" -> " +str(odeur.next_case), fill = "black")
                    canevasC.create_text(400,150 + (id+len(Case.Liste_Odeur["food"]))*50,text="de valeur :"+str(odeur.evalue()), fill = "black", anchor="w")
        elif self.click == "place block": 
            s = terrain.Liste_Cases[x][y]
            s.opacite = 1
            s.a_update()
        elif self.click == "remove block": 
            s = terrain.Liste_Cases[x][y]
            s.opacite = 0
            s.a_update()
    def spawn_food(self) :
        if self.click == "spawn food" :
            self.click = ""
            self.but_food.config(relief = tk.RAISED)
        else :
            click = "spawn food"
            self.but_food.config(relief = tk.SUNKEN)
            self.but_ouvre_case.config(relief = tk.RAISED)

    def select_case(self) :
        self.terrain.maj_spin(self.spin_fml,self.spin_fourmi, self.main_fml)
        if self.click == "ouvre_case" :
            self.click = ""
            self.but_ouvre_case.config(relief = tk.RAISED)
        else :
            self.click = "ouvre_case"
            self.but_ouvre_case.config(relief = tk.SUNKEN)
            self.but_food.config(relief = tk.RAISED)

    def terrain_run(self) :
        if self.minimize_window.get() == 1 :
            self.fenetre1.iconify()
        t0 = time()
        self.terrain.run()
        self.terrain.maj_spin(self.spin_fml,self.spin_fourmi, self.main_fml)
        self.score_t = time()-t0
    


    def clear(self) :
        for Fourmiliere in self.terrain.Liste_Fourmiliere :
            for i in range(len(Fourmiliere.Liste_Fourmis)-1, -1, -1) :
                Fourmiliere.Liste_Fourmis[i].destroy()
            for j in range(len(Fourmiliere.Liste_Odeur)-1, -1, -1):
                Fourmiliere.Liste_Odeur[j].clear()



    def save(self):
        nom_chemin = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        save_terrain(self.terrain, nom_chemin)
    def load(self):
        nom_chemin = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        load_terrain(nom_chemin,self.terrain)
        self.terrain.load()

    def place_block(self) :
        if self.click == "place block" :
            self.click = ""
            self.but_place_block.config(relief = tk.RAISED)
        else :
            self.click = "place block"
            self.but_place_block.config(relief = tk.SUNKEN)
            self.but_remove_block.config(relief = tk.RAISED)
    def remove_block(self) :
        if self.click == "remove block" :
            self.click = ""
            self.but_remove_block.config(relief = tk.RAISED)
        else :
            self.click = "remove block"
            self.but_remove_block.config(relief = tk.SUNKEN)
            self.but_place_block.config(relief = tk.RAISED)
    
    
    def __init__(self) :
        self.click = ""
        self.fenetre1 = tk.Tk()
        self.fenetre1.geometry("1600x800")
        self.fenetre1.title("T.I.P.E. Fourmis")
        self.frame_terrain = tk.Frame(self.fenetre1,borderwidth= 3,relief= tk.SUNKEN,height = 750,width = 100)
        self.frame_terrain.place(x=0,y=0)
        self.frame_fourmis = tk.Frame(self.fenetre1,borderwidth= 3,relief= tk.SUNKEN,height = 750,width = 100)
        self.frame_fourmis.place(x=1350,y=0)
        self.frame_mapmaking = tk.Frame(self.fenetre1,borderwidth= 3,relief= tk.SUNKEN,height = 750,width = 100)
        self.frame_mapmaking.place(x = 1350, y= 300)
        self.canevas = tk.Canvas(master=self.fenetre1, width = 1200, height = 800, bg = "white")
        self.canevas.place(x=100,y=0)
        self.score_p = tk.IntVar()
        self.terrain = Terrain(self.score_p, self.canevas)
        fr1 = Fourmiliere(self.terrain,"fr1")
        self.terrain.Liste_Fourmiliere.append(fr1)

        self.but_help = tk.Button(self.fenetre1,text="Help", command = self.ouvre_help)
        self.but_help.place(x=1305,y=0)

        self.but_ouvre_fm = tk.Button(self.frame_fourmis,text="Voir fourmi", command =self.ouvre_fourmi)
        self.but_ouvre_fm.grid(row = 9,padx=10, pady=3)
    
        self.but_home = tk.Button(self.frame_fourmis,text="Go home", command = self.home)
        self.but_home.grid(row =1,padx=10, pady=3)
    
        self.but_next1= tk.Button(self.frame_terrain,text="+1 steps", command = self.steps1)
        self.but_next1.grid(row = 2,column = 0,padx=10, pady=3)
    
        self.but_next20 = tk.Button(self.frame_terrain,text="+20 steps", command = self.steps20)
        self.but_next20.grid(row = 3,column = 0,padx=10, pady=3) 
        
        self.but_next100 = tk.Button(self.frame_terrain,text="+100 steps", command = self.steps100)
        self.but_next100.grid(row = 4,column = 0,padx=10, pady=3)

        self.but_next500 = tk.Button(self.frame_terrain,text="+500 steps", command = self.steps500)
        self.but_next500.grid(row = 5,column = 0,padx=10, pady=3)
    
        self.but_spawn1 = tk.Button(self.frame_fourmis,text="Spawn 1 ant", command = self.spawn1)
        self.but_spawn1.grid(row = 5,padx=10, pady=3)
        
        self.but_spawn10 = tk.Button(self.frame_fourmis,text="Spawn 10 ants", command = self.spawn10)
        self.but_spawn10.grid(row= 6,padx=10, pady=3)
        
    
        self.but_food = tk.Button(self.frame_mapmaking,text="Spawn food", command = self.spawn_food, activebackground = "gray70")
        self.but_food.grid(row =1,padx=10, pady=3)
        self.frame_terrain.grid_rowconfigure(6,minsize = 50)
        self.but_ouvre_case = tk.Button(self.frame_terrain,text="Info case", command = self.select_case, activebackground = "gray70")
        self.but_ouvre_case.grid(row = 12,padx=10, pady=3)
    
        self.but_run = tk.Button(self.frame_terrain, text = "run", command = self.terrain_run, activebackground = "gray70" )
        self.but_run.grid(row = 25, padx = 10, pady = 3)
        
        self.but_clear = tk.Button(self.frame_fourmis,text="Clear", command = self.clear, activebackground = "gray70")
        self.but_clear.grid(row = 15,padx=10, pady=3)
    
        self.txt_terrain = tk.Label(self.frame_terrain,text="Terrain :",font="Arial 12")
        self.txt_terrain.grid(row = 0,column = 0,padx=10, pady=3)
        self.frame_terrain.grid_rowconfigure(1,minsize = 10)
        self.txt_Fourmiliere = tk.Label(self.frame_fourmis,text="fourmillière :",font="Arial 12")
        self.txt_Fourmiliere.grid(row = 2)
        self.spin_fml = tk.Spinbox(self.frame_fourmis, values=[fml.name for fml in self.terrain.Liste_Fourmiliere], width=20)
        self.spin_fml.grid(row=3,padx=10, pady=3)
        self.spin_radius = tk.Spinbox(self.frame_terrain, values=[10,1,2,3,4,5,6,7,8,9,10], width=10)
        self.spin_radius.grid(row = 9,padx=10, pady=3)
        self.spin_type_fourmi = tk.Spinbox(self.frame_fourmis, values=["Fourmi normale", "Fourmi exploratrice", "Fourmi optimisatrice"], width=20)
        self.spin_type_fourmi.grid(row = 4,padx=10, pady=3)
        for fml in self.terrain.Liste_Fourmiliere :
            if fml.name == self.spin_fml.get() :
                self.main_fml = fml
        self.spin_fourmi = tk.Spinbox(self.frame_fourmis, values= [fr.id for fr in self.main_fml.Liste_Fourmis], width=10)
        self.spin_fourmi.grid(row = 8,padx=10, pady=3)
        self.minimize_window = tk.IntVar() 
        self.check_minimize = tk.Checkbutton(self.frame_terrain, text="Minimize", variable=self.minimize_window)
        self.check_minimize.grid(row = 21, padx = 10, pady = 3)
    
    
        self.canevas.bind("<Button-1>", self.click_gauche)
        for i in range(80) :
            self.canevas.create_line(0,i*10,1200,i*10)
        for i in range(120) :
            self.canevas.create_line(i*10,0,i*10,800) 
        
        self.but_save = tk.Button(self.frame_mapmaking, text = "save", command = lambda: self.save(terrain), activebackground = "gray70" )
        self.but_save.grid(row = 10, padx=10, pady=3)
        self.but_load = tk.Button(self.frame_mapmaking, text = "load", command = lambda: self.load(terrain), activebackground = "gray70" )
        self.but_load.grid(row = 11, padx=10, pady=3)
   
    def affiche(self) :
        self.fenetre1.mainloop()

if __name__ == "__main__":
    f = open("score.txt","a")
    f.write("modèle 3 \n")
    f.write("avec la fenètre ouverte \n")
    for i in range(20) :
        interface = Interface()
        load_terrain("map 1.txt",interface.terrain)
        interface.terrain.load()
        interface.terrain_run()
        interface.canevas.update()
        f.write("t: "+str(interface.score_t)+str("     p: ")+str( interface.score_p.get())+str("\n"))
        interface.fenetre1.destroy()
        print(i)
    f.write("avec la fenètre fermée \n")
    for i in range(20) :
        interface = Interface()
        load_terrain("map 1.txt",interface.terrain)
        interface.terrain.load()
        interface.fenetre1.iconify()
        interface.terrain_run()
        interface.canevas.update()
        f.write("t: "+str(interface.score_t)+str("     p: ")+str( interface.score_p.get())+str("\n"))
        interface.fenetre1.destroy()
        print(i)
    f.close()    
    