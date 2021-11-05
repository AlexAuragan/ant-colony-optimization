import sys
import os, inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if not path in sys.path :
    sys.path.append(path)

from Classes.Classe_Terrain import Terrain
from Classes.Classe_Fourmiliere import Fourmiliere
from tkinter import filedialog
import tkinter as tk
from math import pi
from time import time
from Fonctions.Sauvegarde import load_terrain, save_terrain

import json
with open('language.json',encoding='utf-8') as fd:
    lang = json.load(fd)

dic = lang["fr"]
 
click = ""
def create_terrain() :
    fenetre1 = tk.Tk()
    fenetre1.geometry("1600x800")
    fenetre1.title("T.I.P.E. Fourmis")
    frame_terrain = tk.Frame(fenetre1,borderwidth= 3,relief= tk.SUNKEN,height = 750,width = 100)
    frame_terrain.place(x=0,y=0)
    frame_fourmis = tk.Frame(fenetre1,borderwidth= 3,relief= tk.SUNKEN,height = 750,width = 100)
    frame_fourmis.place(x=1300,y=0)
    frame_mapmaking = tk.Frame(fenetre1,borderwidth= 3,relief= tk.SUNKEN,height = 750,width = 100)
    frame_mapmaking.place(x = 1300, y= 300)
    canevas = tk.Canvas(master=fenetre1, width = 1200, height = 800, bg = "white")
    canevas.place(x=100,y=0)
    score = tk.IntVar()
    terrain = Terrain(score, canevas)
    fr1 = Fourmiliere(terrain,"fr1")
    terrain.Liste_Fourmiliere.append(fr1)


    def ouvre_fourmi() :
        helpf = tk.Tk()
        helpf.geometry("800x500")
        fourmi = spin_fourmi.get()
        Fourmiliere = spin_fml.get() 
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
    

    but_ouvre_fm = tk.Button(frame_fourmis,text=dic["voir fourmi"], command = ouvre_fourmi)
    but_ouvre_fm.grid(row = 9,padx=10, pady=3)

    def home():
        for Fourmiliere in terrain.Liste_Fourmiliere :
            for fourmi in Fourmiliere.Liste_Fourmis :
                fourmi.behavior = "go home"
                fourmi.angle = (fourmi.angle -pi) % (2*pi)
    but_home = tk.Button(frame_fourmis,text=dic["rentrer"], command = home)
    but_home.grid(row =1,padx=10, pady=3)

    def steps1():
        terrain.next()   
    but_next1= tk.Button(frame_terrain,text=dic["1 pas"], command = steps1)
    but_next1.grid(row = 2,column = 0,padx=10, pady=3)

    def steps20():
        for _ in range(20) :
            terrain.next()   
    but_next20 = tk.Button(frame_terrain,text=dic["20 pas"], command = steps20)
    but_next20.grid(row = 3,column = 0,padx=10, pady=3)

    def steps100():
        t0 = time()
        for i in range(100) :
            if i%1 == 0 :
                terrain.check_odeurs()
            terrain.next()
        print(time()-t0)
    but_next100 = tk.Button(frame_terrain,text=dic["100 pas"], command = steps100)
    but_next100.grid(row = 4,column = 0,padx=10, pady=3)
    
    
    def steps500():
        t0 = time()
        for i in range(500) :
            if i%10 == 0 :
                terrain.check_odeurs()
            terrain.next()
        print(time()-t0)
    but_next500 = tk.Button(frame_terrain,text=dic["500 pas"], command = steps500)
    but_next500.grid(row = 5,column = 0,padx=10, pady=3)

    def spawn1() :#Test, fait apparaitre une fourmis 
        terrain.Liste_Fourmiliere[0].spawn(spin_type_fourmi.get())
        terrain.maj_spin(spin_fml,spin_fourmi, main_fml)
    but_spawn1 = tk.Button(frame_fourmis,text=dic["ajoute 1 fourmi"], command = spawn1)
    but_spawn1.grid(row = 5,padx=10, pady=3)

    def spawn10() :#Test, fait apparaitre dix fourmis
        for _ in range(10):
            terrain.Liste_Fourmiliere[0].spawn(spin_type_fourmi.get())
            terrain.maj_spin(spin_fml,spin_fourmi, main_fml)
    but_spawn10 = tk.Button(frame_fourmis,text=dic["ajoute 10 fourmis"], command = spawn10)
    but_spawn10.grid(row= 6,padx=10, pady=3)
        
    def click_gauche(event):
        """Cliquer sur la grille fait apparaitre de la nourriture si le boutton correspondant est enfoncé"""
        global click
        radius = int(spin_radius.get())
        y = int(event.y//10)
        x = int(event.x//10)
        if click == "spawn food" :
            L = []
            for i in range(-radius+1, radius):
                for j in range(-radius+1,radius) :
                    if i*i + j*j < radius*radius/2 and abs(x+i)<120 and abs(y+j) < 80 and x+i >0 and y+j > 0:
                        L.append([x+i,y+j])
            for couple in L :
                x,y = couple[0],couple[1]
                terrain.Liste_Cases[x][y].food += 3
                s = terrain.Liste_Cases[x][y].a_update()
            terrain.update_cases()
        elif click == "ouvre_case" :
            fenetreC = tk.Tk()
            fenetreC.geometry("800x500")
            canevasC = tk.Canvas(fenetreC,width = 1200, height = 400,bg="white")
            Case = terrain.Liste_Cases[x][y]
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
        elif click == "place block": 
            s = terrain.Liste_Cases[x][y]
            s.opacite = 1
            s.a_update()
        elif click == "remove block": 
            s = terrain.Liste_Cases[x][y]
            s.opacite = 0
            s.a_update()
    def spawn_food() :
        global click
        if click == "spawn food" :
            click = ""
            but_food.config(relief = tk.RAISED)
        else :
            click = "spawn food"
            but_food.config(relief = tk.SUNKEN)
            but_ouvre_case.config(relief = tk.RAISED)

    def select_case() :
        terrain.maj_spin(spin_fml,spin_fourmi, main_fml)
        global click
        if click == "ouvre_case" :
            click = ""
            but_ouvre_case.config(relief = tk.RAISED)
        else :
            click = "ouvre_case"
            but_ouvre_case.config(relief = tk.SUNKEN)
            but_food.config(relief = tk.RAISED)

    but_food = tk.Button(frame_terrain,text=dic["nourriture"], command = spawn_food, activebackground = "gray70")
    but_food.grid(row =10,padx=10, pady=3)
    frame_terrain.grid_rowconfigure(6,minsize = 50)
    but_ouvre_case = tk.Button(frame_terrain,text=dic["info case"], command = select_case, activebackground = "gray70")
    but_ouvre_case.grid(row = 12,padx=10, pady=3)

    def terrain_run() :
        if minimize_window.get() == 1 :
            fenetre1.iconify()
        t0 = time()
        terrain.run()
        terrain.maj_spin(spin_fml,spin_fourmi, main_fml)
        print(time()-t0)
        print(score.get())
    
    but_run = tk.Button(frame_terrain, text = dic["lancer"], command = terrain_run, activebackground = "gray70" )
    but_run.grid(row = 25, padx = 10, pady = 3)
    
    text_score = tk.Label(frame_terrain, text = dic["score"])
    text_score.grid(row = 26, padx = 10, pady = 3)
    score.set(terrain.score)
    var_score = tk.Label(frame_terrain, textvariable = score)
    var_score.grid(row = 27, padx = 0, pady = 0)
    

    def clear() :
        for Fourmiliere in terrain.Liste_Fourmiliere :
            for i in range(len(Fourmiliere.Liste_Fourmis)-1, -1, -1) :
                Fourmiliere.Liste_Fourmis[i].destroy()
            for j in range(len(Fourmiliere.Liste_Odeur)-1, -1, -1):
                Fourmiliere.Liste_Odeur[j].clear()


    but_clear = tk.Button(frame_fourmis,text=dic["reset"], command = clear, activebackground = "gray70")
    but_clear.grid(row = 15,padx=10, pady=3)

    txt_terrain = tk.Label(frame_terrain,text=dic["terrain"],font="Arial 12")
    txt_terrain.grid(row = 0,column = 0,padx=10, pady=3)
    frame_terrain.grid_rowconfigure(1,minsize = 10)
    txt_Fourmiliere = tk.Label(frame_fourmis,text=dic["fourmiliere"],font="Arial 12")
    txt_Fourmiliere.grid(row = 2)
    spin_fml = tk.Spinbox(frame_fourmis, values=[fml.name for fml in terrain.Liste_Fourmiliere], width=20)
    spin_fml.grid(row=3,padx=10, pady=3)
    spin_radius = tk.Spinbox(frame_terrain, values=[1,2,3,4,5,6,7,8,9,10], width=10)
    spin_radius.grid(row = 9,padx=10, pady=3)
    spin_type_fourmi = tk.Spinbox(frame_fourmis, values=["Fourmi normale", "Fourmi exploratrice", "Fourmi optimisatrice"], width=20)
    spin_type_fourmi.grid(row = 4,padx=10, pady=3)
    for fml in terrain.Liste_Fourmiliere :
         if fml.name == spin_fml.get() :
            main_fml = fml
    spin_fourmi = tk.Spinbox(frame_fourmis, values= [fr.id for fr in main_fml.Liste_Fourmis], width=10)
    spin_fourmi.grid(row = 8,padx=10, pady=3)
    minimize_window = tk.IntVar() 
    check_minimize = tk.Checkbutton(frame_terrain, text=dic["reduire"], variable=minimize_window)
    check_minimize.grid(row = 21, padx = 10, pady = 3)


    canevas.bind("<Button-1>", click_gauche)
    for i in range(80) :
        canevas.create_line(0,i*10,1200,i*10)
    for i in range(120) :
        canevas.create_line(i*10,0,i*10,800) 
    
    def save(terrain):
        nom_chemin = filedialog.asksaveasfilename(initialdir = path+"/maps",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        save_terrain(terrain, nom_chemin)
    def load(terrain):
        nom_chemin = filedialog.askopenfilename(initialdir = path+"/maps",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        load_terrain(nom_chemin,terrain)
        terrain.load()

    but_save = tk.Button(frame_mapmaking, text = dic["sauvegarder"], command = lambda: save(terrain), activebackground = "gray70" )
    but_save.grid(row = 10, padx=10, pady=3)
    but_load = tk.Button(frame_mapmaking, text = dic["charger"], command = lambda: load(terrain), activebackground = "gray70" )
    but_load.grid(row = 11, padx=10, pady=3)

    def place_block() :
        global click
        if click == "place block" :
            click = ""
            but_place_block.config(relief = tk.RAISED)
        else :
            click = "place block"
            but_place_block.config(relief = tk.SUNKEN)
            but_remove_block.config(relief = tk.RAISED)
    def remove_block() :
        global click
        if click == "remove block" :
            click = ""
            but_remove_block.config(relief = tk.RAISED)
        else :
            click = "remove block"
            but_remove_block.config(relief = tk.SUNKEN)
            but_place_block.config(relief = tk.RAISED)
    
    but_place_block = tk.Button(frame_mapmaking, text = dic["mettre mur"], command = place_block, activebackground = "gray70" )
    but_place_block.grid(row = 3, padx=10, pady=3)
    but_remove_block = tk.Button(frame_mapmaking, text = dic["enlever mur"], command = remove_block, activebackground = "gray70" )
    but_remove_block.grid(row = 4, padx=10, pady=3)

    fenetre1.mainloop()

if __name__ == "__main__":
    create_terrain()