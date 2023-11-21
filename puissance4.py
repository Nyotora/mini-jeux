from random import randint
from typing import BinaryIO
from Joueur import PlayerInfo
from module_score import setScore
import pickle


def affGame(t:list):
    """
    Procédure pour afficher la matrice

    Entrée : t : tableau
    """
    i : int
    j : int

    print(" ",end="")
    for i in range(1,8):
        print("  ",i,end="  ")
    print()
    for i in range(5,-1,-1):
        print('║║',end='')
        #Ligne du haut
        for j in range(7):
            if t[i][j]=='R':
                print("▕\033[2;0;041m▔▔▔\033[0;0;0m▏",end="")
            elif t[i][j]=='J':
                print("▕\033[2;0;043m▔▔▔\033[0;0;0m▏",end="")
            elif t[i][j]=='RV':
                print("▕\033[48;5;211m▔▔▔\033[0;0;0m▏",end="")
            elif t[i][j]=='JV':
                print("▕\033[48;5;229m▔▔▔\033[0;0;0m▏",end="")
            else:
                print("     ",end="")
            print('║',end='')
        print('║')
        print('║║',end='')
        #Ligne du bas
        for j in range(7):
            if t[i][j]=='R':
                print("▕\033[2;0;041m▁▁▁\033[0;0;0m▏",end="")
            elif t[i][j]=='J':
                print("▕\033[2;0;043m▁▁▁\033[0;0;0m▏",end="")
            elif t[i][j]=='RV':
                print("▕\033[48;5;211m▁▁▁\033[0;0;0m▏",end="")
            elif t[i][j]=='JV':
                print("▕\033[48;5;229m▁▁▁\033[0;0;0m▏",end="")
            else:
                print("     ",end="")
            print('║',end='')
        
        print('║')
        if i != 0:
            print('╠╬',end='')
            for j in range(7):
                print("═════╬",end="")
            print('╣')
        else:
            print('╚╩',end='')
            for j in range(7):
                print("═════╩",end="")
            print('╝')

def CanPlayAt(col:int,tab:list) -> bool:
    """
    Fonction qui renvoie -1 si il est impossible de jouer sur cette colonne, ou sinon le 
    numéro de la ligne ou le jeton atterira.

    Entrée : col : entier
             tab : tableau

    Retourne : entier
    """
    i : int
    pos : int
    pos = -1
    for i in range(6):
        if tab[i][col] == '' and pos == -1: #Dès qu'on détecte du vide, on stocke la ligne
            pos = i                         # si cela n'est pas déjà fait
    return pos


def WinColor(symb:str,tab:list,coordX:int,coordY:int,Vdir:int,Hdir:int):
    """
    Procédure qui colore le nombre de jetons identiques trouvés sur une même direction
    de manière récursive en se déplaçant au fur et à mesure

    Entrée : symb : chaine de caractères   -> Couleur du jeton
             tab : tableau 
             coordX : entier
             coordY : entier
             Vdir : entier   -> Diretion verticale
             Hdir : entier   -> Direction horizontale
    """
    
    #si on n'a pas atteint le bord
    if ((coordY == 0  and Hdir ==-1) or (coordY == 6  and Hdir ==1)) and (tab[coordX][coordY]==symb or tab[coordX][coordY]==symb+'V'):
        if tab[coordX][coordY]==symb :
            tab[coordX][coordY]=symb+'V'
    else:
        #si on n'a pas atteint le bord
        if ((coordX == 5  and Vdir ==1) and (tab[coordX][coordY]==symb or tab[coordX][coordY]==symb+'V')):
            if tab[coordX][coordY]==symb :
                tab[coordX][coordY]=symb+'V'
        else:
            #Si le jeton sur notre position actuelle a notre couleur
            if tab[coordX][coordY]==symb or tab[coordX][coordY]==symb+'V':
                #Coloration
                if tab[coordX][coordY]==symb :
                    tab[coordX][coordY]=symb+'V'
                #On avance
                coordX = coordX + Vdir
                coordY = coordY + Hdir
                WinColor(symb,tab,coordX,coordY,Vdir,Hdir)

def WinCondition(symb:str,tab:list,coordX:int,coordY:int,Vdir:int,Hdir:int) -> int :
    """
    Fonction qui renvoie le nombre de jetons identiques trouvés sur une même direction
    de manière récursive en se déplaçant au fur et à mesure

    Entrée : symb : chaine de caractères   -> Couleur du jeton
             tab : tableau 
             coordX : entier
             coordY : entier
             Vdir : entier   -> Diretion verticale
             Hdir : entier   -> Direction horizontale

    Retourne : entier
    """
    nbJeton : int
    
    #Deux conditions de sortie de la récursivité (si on a atteint le bord)
    if ((coordY == 0  and Hdir ==-1) or (coordY == 6  and Hdir ==1)) and tab[coordX][coordY]==symb:
        nbJeton = 1
    elif (coordX == 5  and Vdir ==1) and tab[coordX][coordY]==symb:
        nbJeton = 1
    else:
        #Si le jeton sur notre position actuelle a notre couleur
        if tab[coordX][coordY]==symb:
            #On avance
            coordX = coordX + Vdir
            coordY = coordY + Hdir 
            nbJeton = 1 + WinCondition(symb,tab,coordX,coordY,Vdir,Hdir)
        else:
            nbJeton=0

    return nbJeton

def WinVerif(symb:str,tab:list,ligne:int,col:int,test:str) -> bool:
    """
    Fonction qui appelle la fonction de vérification en regardant dans toutes
    les directions, puis retourne le booléen de la victoire ou non.

    Entrée : symb : chaine de caractères   -> Couleur du jeton
             tab : tableau
             ligne : entier
             col : entier
             test : str

    Retourne : booléen  
    """
    
    Vdir : int
    Hdir : int
    hasWon:bool
    hasWon = False

    for Vdir in range(-1,2):  # Caractérise le déplacement vertical
        for Hdir in range(-1,2): # Caractérise le déplacement horizontal
            if hasWon == False:
                if not(Vdir == 0 and Hdir == 0): # Il faut au moins une direction =/= 0
                    #Verification dans les deux sens en additionnant les cases vers les direction
                    #Vdir et Hdir, puis leur opposé
                    if WinCondition(symb,tab,ligne,col,Vdir,Hdir) + WinCondition(symb,tab,ligne,col,-Vdir,-Hdir) -1 >= 4:
                        hasWon = True
                        if test == "VERIFICATION":
                            WinColor(symb,tab,ligne,col,Vdir,Hdir)
                            WinColor(symb,tab,ligne,col,-Vdir,-Hdir)
    return hasWon


def OrdiTurn(symb:str,symbAdv:str,tab:list,OrdiNB:int) -> int:
    """
    Fonction qui  permet à un ORDI de déposer un jeton intelligement et qui renvoie 
    le numéro du joueur si il a gagné. (Cette fonction étant à 
    la base une procédure, l'entier retourné devait être dans les sorties également.)

    Entrée : symb : chaine de caractères   -> Couleur du jeton
             symbAdv : chaine de caractères   -> Couleur du jeton adverse
             tab : tableau
             OrdiNB : entier  -> Numéro du Joueur(Ordi) (1 ou 2)
    
    Sortie : tableau

    Retourne : entier  
    """
    i : int
    ligne : int
    col : int
    end : bool   #  end permet de savoir si l'ordi à joué ou non, à la différence de
    hasWon : int #  la variable hasWon, qui permet quand à elle de savoir si il a gagné.

    #initialisation des variables
    hasWon = 0
    ligne = -1
    end = False

    #Vérifie s'il peut gagner
    for i in range(0,7):
        if not end:
            ligne = CanPlayAt(i,tab)
            if ligne != -1:
                tab[ligne][i] = symb
                if WinVerif(symb,tab,ligne,i,"TEST"):
                    end = True
                    hasWon = OrdiNB
                    WinVerif(symb,tab,ligne,i,"VERIFICATION")
                else:
                    tab[ligne][i] = ''
    #Vérifie si l'adversaire peut gagner
    for i in range(0,7):
        if not end:
            ligne = CanPlayAt(i,tab)
            if ligne != -1:
                tab[ligne][i] = symbAdv #Simulation (au dessus)
                if WinVerif(symbAdv,tab,ligne,i,"TEST"):
                    end = True
                    tab[ligne][i] = symb
                else:
                    tab[ligne][i] = ''

    #Joue aléatoirement s'il ne peut ni gagner, ni bloquer.
    if not end:
        ligne = -1
        while ligne == -1:
            col = randint(0,6)
            ligne = CanPlayAt(col,tab)
        tab[ligne][col] = symb #Mise à jour de la matrice.
    return hasWon

def JoueurTurn(symb:str,tab:list,playerNB:int) -> int:
    """
    Fonction qui  permet au joueur de déposer un jeton et qui renvoie 
    le numéro du joueur si il a gagné. (Cette fonction étant à 
    la base une procédure, l'entier retourné devait être dans les sorties également.)

    Entrée : symb : chaine de caractères   -> Couleur du jeton
             tab : tableau
             playerNB : entier  -> Numéro du Joueur (1 ou 2)
    
    Sortie : tableau

    Retourne : entier  
    """
    choix : str
    ligne : int
    hasWon : int

    #initialisation des variables
    ligne = -1
    hasWon = 0
    #Verification de la saisie
    while ligne == -1:
        choix = input("Choisissez un emplacement : ") #Choix est un str car nous faisons la conversion plus tard.
        if choix == '1' or choix == '2' or choix == '3' or choix == '4' or choix == '5' or choix == '6' or choix == '7':
            ligne = CanPlayAt(int(choix)-1,tab) #Vérifie si l'emplacement choisi est jouable.
    tab[ligne][int(choix)-1] = symb #Mise à jour de la matrice.

    #Condition de victoire
    if WinVerif(symb,tab,ligne,int(choix)-1,"VERIFICATION"):
        hasWon = playerNB
        
    return hasWon

def noEspaceLeft(tab:list) -> int:
    """
    Fonction qui renvoie 0 si il détecte un endroit jouable sur la ligne du haut,
    -1 si il n'y a plus d'espace jouble, caractérisant une égalité.

    Entrée : tab : tableau

    Retourne : entier
    """
    i:int
    egalite : int
    egalite = -1
    for i in range(7):
        if tab[5][i] == '': #Détection d'un espace
            egalite = 0
    return egalite


def partiePui4(J1:str,J2:str,mode:int):
    """
    Procédure modélisant le déroulement de la partie de Puissance 4
    selon le mode de jeu (1,2 ou 3 : J1vsJ2, J1vsOrdi, OrdivsOrdi).

    Entrée : J1 : chaine de caractère
             J2 : chaine de caractère
             mode : entier
    """

    f : BinaryIO
    l : list
    gagnant : int
    tab : list

    gagnant = 0 #Variable caractérisant le numéro du gagnant (-1 pour une égalité, 0 pour
                # aucun gagnant, 1 et 2 pour les numéros respéctifs des joueurs.)

    #Gestion de la matrice 7x6
    tab = [['','','','','','',''],['','','','','','',''],['','','','','','',''],['','','','','','',''],['','','','','','',''],['','','','','','','']]
    affGame(tab)
    while gagnant == 0: #Tant qu'il n'y a aucun gagnant
        if mode == 1 or (mode == 2 and J1 !=""): #Si J1 afronte J2 ou l'Ordi)
            gagnant = JoueurTurn('R',tab,1)
            affGame(tab)
        else: #Ordi affronte J2 ou un autre Ordi
            print("TOUR DE L'ORDI\033[2;34m",J1,"\033[0;0m")
            gagnant = OrdiTurn('R','J',tab,1)
            affGame(tab)

        #Test égalitée
        if gagnant == 0:
            gagnant = noEspaceLeft(tab)
        if gagnant == 0:
            if mode == 1 or (mode == 2 and J2 !=""):#Si J2 afronte J1 ou l'Ordi)
                gagnant = JoueurTurn('J',tab,2)
                affGame(tab)
            else: #Ordi affronte J1 ou un autre Ordi
                print("TOUR DE L'ORDI\033[2;34m",J2,"\033[0;0m")
                gagnant = OrdiTurn('J','R',tab,2)
                affGame(tab)
        #Test égalitée
        if gagnant == 0:
            gagnant = noEspaceLeft(tab)

    if gagnant == 1:
        print("\033[2;34m",J1,"\033[0;0ma gagné !!")
    elif gagnant == 2:
        print("\033[2;34m",J2,"\033[0;0ma gagné !!")
    else:
        print("Egalité !")

    #===== GESTION DES SCORES ================================

    #Création structure PlayerInfo
    if mode != 3:
        p1 = PlayerInfo()
        p1.name = J1
        p2 = PlayerInfo()
        p2.name = J2

    l = []
    try:  #Le fichier existe-t-il ?
        f = open("data.dat","rb")
        l = pickle.load(f)
        f.close()
        f = open("data.dat","wb")
    except FileNotFoundError:
        f = open("data.dat","wb")
    except EOFError:
        f = open("data.dat","wb")
    

    if mode == 1: #Joueur vs Joueur
        if gagnant == 1:
            setScore(l,p1,1,4)
            setScore(l,p2,-1,4)
                
        elif gagnant == 2:
            setScore(l,p1,-1,4)
            setScore(l,p2,1,4)
    elif mode == 2: #Joueur vs Ordi
        if p1.name != "": #Si Joueur = Player 1
            if gagnant == 1:
                setScore(l,p1,1,4)
            elif gagnant == 2:
                setScore(l,p1,-1,4)  
        else:#Joueur = Player 2
            if gagnant == 2:
                setScore(l,p2,1,4)
            elif gagnant == 1:  
                setScore(l,p2,-1,4)         
    pickle.dump(l,f) #Ajout au fichier
    f.close()

def menuPuissance4():
    """
    Procédure proposant le choix d'un affrontement entre joueurs,
    entre ordinateurs ou entre un joueur et un ordinateur au
    puissance 4.

    Aucun argument.
    """
    choix : int
    J1 : str
    J2 : str

    choix = 0
    while choix != 4:
        #Affichage du menu
        print("⋆⋆⋆ ✪ PUISSANCE 4 ✪ ⋆⋆⋆")
        print("Règles : Pour gagner, il suffit d'être le premier à aligner 4 jetons de sa \ncouleur horizontalement, verticalement et diagonalement.\n")
        choix = int(input("1 - J1 ⚔ J2\n2 - J1 ⚔ ORDI\n3 - ORDI ⚔ ORDI\n4 - Quitter\nChoix : "))
    
        if choix == 1:
            J1 = input("Nom du J1 : ")
            while J1 == "":
                J1 = input("Le nom de J1 ne doit pas être vide : ")
            J2 = input("Nom du J2: ")
            while J2 == "" or J2 == J1:
                J2 = input("Le nom de J2 ne doit pas être vide, ni égal à celui du J1 : ")
            #Décision de l'ordre de jeu
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                partiePui4(J1,J2,1)
            else:
                print("\033[2;34m",J2,"\033[0;0mcommence !!")
                partiePui4(J2,J1,1)
            
        if choix == 2:
            J1 = input("Nom du J1 : ")
            while J1 == "":
                J1 = input("Le nom de J1 ne doit pas être vide : ")
            J2 = "" #Ordi n'ayant aucun nom pour faciliter les comparaisons.
            #Décision de l'ordre de jeu
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                partiePui4(J1,J2,2)
            else:
                print("\033[2;34mL'Ordi\033[0;0m commence !!")
                partiePui4(J2,J1,2)
                
        if choix == 3:
            J1 = input("Nom de l'ordi 1 : ")
            J2 = input("Nom de l'ordi 2 : ")
            #Décision de l'ordre de jeu
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                partiePui4(J1,J2,3)
            else:
                print("\033[2;34m",J2,"\033[0;0mcommence !!")
                partiePui4(J2,J1,3)
            
        elif choix == 4:
            print("Retour...")
