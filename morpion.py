from random import randint
from typing import BinaryIO
from Joueur import PlayerInfo
from module_score import setScore
import pickle

def egalite(tab:list) -> bool:
    """
    Fonction vérifiant un match nul ou non

    Entrée : tab : tableau

    Retourne : booléen
    """
    nbCase : int
    i : int
    j : int

    nbCase = 0
    for i in range(3):
        for j in range(3):
            if tab[i][j] == 'O' or tab[i][j] == 'X':
                nbCase = nbCase + 1
    if nbCase == 9:
        return True
    else:
        return False


def hasWon(tab:list,symbol:str) -> bool:
    """
    Fonction qui vérifie si un joueur à gagné ou non

    Entrée : tab : tableau
             symbol : chaine de caractère
    
    Retourne : booléen
    """
    victory : bool
    i : int

    victory = False
    for i in range(3):
        #En ligne
        if not victory and tab[i][0] == symbol and tab[i][1] == symbol and tab[i][2] == symbol:
            victory = True
        #En colonne
        elif not victory and tab[0][i] == symbol and tab[1][i] == symbol and tab[2][i] == symbol:
            victory = True
    #En diagonale
    if not victory and ((tab[0][0] == symbol and tab[1][1] == symbol and tab[2][2] == symbol) or (tab[0][2] == symbol and tab[1][1] == symbol and tab[2][0] == symbol)):
        victory = True
    return victory

def PlayerTurn(symb:str,tab:list):
    """
    Procédure simulant le choix d'un joueur.

    Entrée : symb : chaine de caractère
             tab : tableau

    Sortie : tab : tableau
    """
    x : int
    x = int(input('Choisissez une case entre 1 et 9 : '))
    while x <= 0  or x >= 10 or tab[(x-1)//3][(x-1)%3] == 'O' or tab[(x-1)//3][(x-1)%3] == 'X':
        x = int(input('Erreur !\nChoisissez une case entre 1 et 9 : '))
    tab[(x-1)//3][(x-1)%3] = symb

def OrdiTurn(symb:str,symbAdv:str,tab:list):
    """
    Procédure simulant le choix d'un ORDI intelligent.

    Entrée : symb : chaine de caractère
             symbAdv : chaine de caractère
             tab : tableau

    Sortie : tab : tableau
    """
    randCase : int

    randCase = randint(1,9)
    #=====PeutGagner=======
    casePos = canComplete(tab,symb)
    if casePos != -1:
        tab[(casePos-1)//3][(casePos-1)%3] = symb
    #============================================
    else:
        #=====Blocage=======
        casePos = canComplete(tab,symbAdv)
        if casePos != -1:
            tab[(casePos-1)//3][(casePos-1)%3] = symb
        #============================================
        else: #Aléatoire
            while tab[(randCase-1)//3][(randCase-1)%3] == 'O' or tab[(randCase-1)//3][(randCase-1)%3] == 'X':
                randCase = randint(1,9)
            tab[(randCase-1)//3][(randCase-1)%3] = symb

def canComplete(tab:list,symb:str) -> int:
    """
    Fonction vérifiant toutes les combinaisons et renvoie une qui peut être complétée
    pour gagner.

    Entrée : tab : tableau
             symb : chaine de caractères

    Retourne : entier
    """
    casePos : int
    i : int

    casePos = -1
    for i in range(3): #Verification en ligne
        if casePos == -1:
            casePos = isWinning(symb,[tab[i][0],tab[i][1],tab[i][2]])
            if casePos != -1:
                casePos = casePos + i*3 + 1
        if casePos == -1: #Verification en colonne
            casePos = isWinning(symb,[tab[0][i],tab[1][i],tab[2][i]])
            if casePos != -1:
                casePos = i+casePos*3 + 1
    
    #Verification en diagonales
    if casePos == -1:
        casePos = isWinning(symb,[tab[0][0],tab[1][1],tab[2][2]])
        if casePos == -1:
            casePos = isWinning(symb,[tab[0][2],tab[1][1],tab[2][0]])
            if casePos != -1:
                casePos = (casePos+1)*2 +1
        else:
            casePos = casePos*4 +1
    return casePos

def isWinning(symb:str,l:list) -> int:
    """
    Fonction qui vérifie si un joueur peut gagner en un seul coup.

    Entrée : symb : chaine de caractère   -> Rond ou Croix
             l : tableau

    Retourne : entier
    """
    isWin : bool
    n : int
    nbSymb : int
    nbEspace : int
    espPos : int

    isWin = True
    n = 0
    nbSymb = 0
    nbEspace = 0
    espPos = 0
    # Tant qu'il peut gagner mais qu'il n'y a pas 2 symboles idetiques ainsi qu'un seul espace
    while isWin and not (nbSymb == 2 and nbEspace == 1):
        if n == 3: #condition d'arret
            isWin = False
        else:
            if l[n] == ' ': #Détéction d'un espace
                nbEspace = nbEspace+1
                espPos = n
            if l[n] == symb: #Détéction d'un symbole identique
                nbSymb = nbSymb + 1

            #Si il y a 0 ou 2 espaces ou un symbole adverse de détectés
            if nbEspace >= 2 or (l[n] != symb and l[n] != ' ') or (nbEspace == 0  and n==3):
                isWin = False
            n = n+1 #Incrémentation
    if isWin : #Il peut gagner
        return espPos
    else: #Il peut pas gagner
        return -1 

def affList(tab:list):
    """
    Procédure pour afficher la matrice

    Entrée : tab : tableau
    """
    i : int
    j : int
    print("╔════════╦════════╦════════╗")
    for i in range(6): 
        print("║  ",end='')
        for j in range(3):
            if tab[i//2][j] == 'X' and i%2==0:
                print("\033[2;31m \/ \033[0;0m",end="  ║  ")
            elif tab[i//2][j] == 'X' and i%2==1:
                print(" /\ ",(j+1) +3*(i//2),end="║  ")
            elif tab[i//2][j] == 'O' and i%2==0:
                print(" ╔\033[2;34m╗ \033[0;0m",end="  ║  ")
            elif tab[i//2][j] == 'O' and i%2==1:
                print("\033[2;34m ╚\033[0;0m╝ ",(j+1) +3*(i//2),end="║  ")
            elif tab[i//2][j] == ' ' and i%2==0:
                print("    ",end="  ║  ")
            elif tab[i//2][j] == ' ' and i%2==1:
                print("    ",(j+1) +3*(i//2),end="║  ")
        if i%2==1 and i != 5:
            print("\n╠════════╬════════╬════════╣")
        else:
            print('')
    print("╚════════╩════════╩════════╝")

def MorpionGAME(J1:str,J2:str,mode:int):
    """
    Procédure modélisant le déroulement de la partie de Morpion
    selon le mode de jeu (1,2 ou 3 : J1vsJ2, J1vsOrdi, OrdivsOrdi).

    Entrée : J1 : chaine de caractère
             J2 : chaine de caractère
             mode : entier
    """

    f : BinaryIO
    l : list
    tab : list
    end : bool



    tab = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    end = False  
    affList(tab)
    while not end : #Tant qu'il n'y a aucun gagnant

        #Test égalitée
        if egalite(tab):
            end = True
        if not end:
            if mode == 1 or (mode == 2 and J1 !=""): #Si J1 afronte J2 ou l'Ordi)
                PlayerTurn('O',tab)
                end = hasWon(tab,'O')
            else: #Ordi affronte J2 ou un autre Ordi
                print("TOUR DE L'ORDI\033[2;34m",J1,"\033[0;0m")
                OrdiTurn('O','X',tab)
                end = hasWon(tab,'O')
            
            affList(tab)

        #Test égalitée    
        if egalite(tab) == True:
            end = True
        if end == False:
            if mode == 1 or (mode == 2 and J2 !=""): #Si J2 afronte J1 ou l'Ordi
                PlayerTurn('X',tab)
                end = hasWon(tab,'X')
            else: #Ordi affronte J1 ou un autre Ordi
                print("TOUR DE L'ORDI\033[2;34m",J2,"\033[0;0m")
                OrdiTurn('X','O',tab)
                end = hasWon(tab,'X')
            affList(tab)

    if hasWon(tab,'O'):
        print("\033[2;34m",J1,"\033[0;0ma gagné !!")
    elif hasWon(tab,'X'):
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
    try: #Le fichier existe-t-il ?
        f = open("data.dat","rb")
        l = pickle.load(f)
        f.close()
        f = open("data.dat","wb")
    except FileNotFoundError:
        f = open("data.dat","wb")
    except EOFError:
        f = open("data.dat","wb")
    

    if mode == 1: #Joueur vs Joueur
        if hasWon(tab,'O'):
            setScore(l,p1,1,3)
            setScore(l,p2,-1,3)
                
        elif hasWon(tab,'X'):
            setScore(l,p1,-1,3)
            setScore(l,p2,1,3)
    elif mode == 2: #Joueur vs Ordi
        if p1.name != "": #Si Joueur = Player 1
            if hasWon(tab,'O'):
                setScore(l,p1,1,3)
            elif hasWon(tab,'X'):  
                setScore(l,p1,-1,3)  
        else: #Si Joueur = Player 2
            if hasWon(tab,'X'):
                setScore(l,p2,1,3)
            elif hasWon(tab,'O'):  
                setScore(l,p2,-1,3)         
    pickle.dump(l,f) #Ajout au fichier
    f.close()

def menuMorpion():
    """
    Procédure proposant le choix d'un affrontement entre joueurs,
    entre ordinateurs ou entre un joueur et un ordinateur au
    morpion.

    Aucun argument.
    """
    choix : int
    J1 : str
    J2 : str

    choix = 0
    while choix != 4:
        print("⋆⋆⋆ ✪ MORPION ✪ ⋆⋆⋆")
        print("Règles : Chaque joueur dépose sa marque (Rond ou Croix) dans une matrice 3x3. \nLe premier qui en alligne 3 dans n'importe quelle direction à gagné.\n")
        choix = int(input("1 - J1 ⚔ J2\n2 - J1 ⚔ ORDI\n3 - ORDI ⚔ ORDI\n4 - Quitter\nChoix : "))
    
        if choix == 1:
            J1 = input("Nom du J1 : ")
            while J1 == "":
                J1 = input("Le nom de J1 ne doit pas être vide : ")
            J2 = input("Nom du J2: ")
            while J2 == "" or J2 == J1:
                J2 = input("Le nom de J2 ne doit pas être vide, ni égal à celui du J1 : ")
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                MorpionGAME(J1,J2,1)
            else:
                print("\033[2;34m",J2,"\033[0;0mcommence !!")
                MorpionGAME(J2,J1,1)
            
        if choix == 2:
            J1 = input("Nom du J1 : ")
            while J1 == "":
                J1 = input("Le nom de J1 ne doit pas être vide : ")
            J2 = ""
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                MorpionGAME(J1,J2,2)
            else:
                print("\033[2;34mL'Ordi\033[0;0mcommence !!")
                MorpionGAME(J2,J1,2)
                
        if choix == 3:
            J1 = input("Nom de l'ordi 1 : ")
            J2 = input("Nom de l'ordi 2 : ")
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                MorpionGAME(J1,J2,3)
            else:
                print("\033[2;34mL'Ordi\033[0;0mcommence !!")
                MorpionGAME(J2,J1,3)
            
        elif choix == 4:
            print("Retour...")