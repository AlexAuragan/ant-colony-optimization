def convert_case_to_str(case) :
    [i,j] = case.coo
    opacite = case.opacite
    nourriture = case.food
    return "{0} {1} {2} {3} \n".format(i,j,opacite,nourriture)

def save_terrain(terrain, path):
    txt = open(path+".txt", "w+")
    lines_of_txt = []
    for i in range(len(terrain.Liste_Cases)) :
        for j in range(len(terrain.Liste_Cases[0])) :
            lines_of_txt.append(convert_case_to_str(terrain.Liste_Cases[i][j]))
    txt.writelines(lines_of_txt)
    txt.close()

def convert_line_to_case(ligne, liste_cases) :
    info_case = ligne.split()
    [i,j,op,nour] = info_case
    liste_cases[int(i)][int(j)].food = int(nour)
    liste_cases[int(i)][int(j)].opacite = float(op)
    liste_cases[int(i)][int(j)].a_update()


def load_terrain(nom_fichier,terrain) :
    fichier = open(nom_fichier,"r")
    for ligne in fichier.readlines():
        convert_line_to_case(ligne,terrain.Liste_Cases)
    terrain.update_cases()
