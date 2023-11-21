
from random import randint
from time import sleep
from typing import BinaryIO
from Joueur import PlayerInfo
from module_score import setScore
import pickle


def PlayerTurn(Joueur:str) -> int:
    """
    Fonction simulant le choix du joueur

    Entrée : Joueur : chaine de caractère   -> nom du Joueur

    Retourne : entier
    """
    choix : int

    choix = -1
    #Choix du nbr d'allumettes à enlever
    while choix > 3 or choix < 1 :
        print("»\033[2;34m",Joueur,"\033[0;0mchoisissez une, deux ou trois allumettes à enlever.")
        choix = int(input("Choix : "))
    return choix

def OrdiTurn(nb:int) -> int:
    """
    Fonction simulant le choix d'un ORDI intelligent

    Entrée : nb : entier   -> nombre d'allumettes

    Retourne : entier
    """
    choix : int

    #Si le nombre d'allumettes est entre 8 (compris) et 5 (non compris),
    # alors l'ORDI cherchera à gagner logiquement
    if nb == 4:
        choix = 3
    elif nb == 3:
        choix = 2
    elif nb == 2:
        choix = 1
    elif nb <= 8 and nb >5:
        choix = nb - 5
    else:
        choix = randint(1,3)
    print("L'Ordi a choisi de retirer",choix,"allumettes !")
    return choix

def affAllumetes(nb_allumettes:int):
    """
    Procédure pour afficher des allumettes

    Entrée : nb_allumettes : entier
    """

    for i in range(nb_allumettes):
        print("\033[38;5;186m▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\033[2;31m▄██\033[38;5;124m█▄\033[0;0m",end="  ")
        print(i+1)
        print("\033[2;33m                \033[2;31m\033[38;5;124m▀▀▀\033[0;0m",end="  ")
        print("")


def allumettesGAME(J1:str,J2:str,mode:int):
    """
    Procédure modélisant le déroulement de la partie du jeu des allumettes
    selon le mode de jeu (1,2 ou 3 : J1vsJ2, J1vsOrdi, OrdivsOrdi).

    Entrée : J1 : chaine de caractère
             J2 : chaine de caractère
             mode : entier
    """

    f : BinaryIO
    l : list
    end : int
    nb_allumettes : int



    end = -1
    nb_allumettes = 20
    while end == -1: #Tant qu'il n'y a aucun gagnant
        sleep(1)
        affAllumetes(nb_allumettes)
        if mode == 1 or (mode == 2 and J1 !=""): #Si J1 afronte J2 ou l'Ordi
            nb_allumettes = nb_allumettes - PlayerTurn(J1)
        else: #Ordi affronte J2 ou un autre Ordi
            print("»L'Ordi\033[2;34m",J1,"\033[0;0mest en train de jouer...")
            sleep(1)
            nb_allumettes = nb_allumettes - OrdiTurn(nb_allumettes)
        
        #--------Condition de victoire ----------
        if nb_allumettes ==1: # Victoire du J1
            affAllumetes(nb_allumettes)
            print("...")
            print("Il ne reste qu'une seule allumette !")
            if mode == 2 and J1 =="": #Si J1 est l'ORDI, alors il a gagné
                print("\033[2;34mL'Ordi\033[0;0m a gagné !!")
            else:# sinon victoire du joueur
                print("\033[2;34m",J1,"\033[0;0ma gagné !!")
            end = 1
        elif nb_allumettes <1: # Victoire du J2
            if mode == 2 and J2 =="": #Si J2 est l'ORDI, alors il a gagné
                print("\033[2;34mL'Ordi\033[0;0m a gagné !!")
            else:# sinon victoire du joueur
                print("\033[2;34m",J2,"\033[0;0ma gagné !!")
            end = 2
        else:
            sleep(1)
            #================== Tour suivant ====================
            affAllumetes(nb_allumettes)
            if mode == 1 or (mode == 2 and J2 !=""): #Si J2 afronte J1 ou l'Ordi)
                nb_allumettes = nb_allumettes - PlayerTurn(J2)
            else:#Ordi affronte J1 ou un autre Ordi
                print("»L'Ordi\033[2;34m",J2,"\033[0;0mest en train de jouer...")
                sleep(1)
                nb_allumettes = nb_allumettes - OrdiTurn(nb_allumettes)

            #--------Condition de victoire ----------
            if nb_allumettes ==1: # Victoire du J2
                affAllumetes(nb_allumettes) 
                print("...")
                print("Il ne reste qu'une seule allumette !")
                if mode == 2 and J2 =="":#Si J2 est l'ORDI, alors il a gagné
                    print("\033[2;34mL'Ordi\033[0;0m a gagné !!")
                else:# sinon victoire du joueur
                    print("\033[2;34m",J2,"\033[0;0ma gagné !!")
                end = 2
            elif nb_allumettes <1:# Victoire du J1
                if mode == 2 and J1 =="": #Si J1 est l'ORDI, alors il a gagné
                    print("\033[2;34mL'Ordi\033[0;0m a gagné !!")
                else: # sinon victoire du joueur
                    print("\033[2;34m",J1,"\033[0;0ma gagné !!")
                end = 1

    #===== GESTION DES SCORES ================================
    l = []

    if mode != 3:
        p1 = PlayerInfo()
        p1.name = J1
        p2 = PlayerInfo()
        p2.name = J2
    try:
        f = open("data.dat","rb")
        l = pickle.load(f)
        f.close()
        f = open("data.dat","wb")
    except FileNotFoundError:
        f = open("data.dat","wb")
    except EOFError:
        f = open("data.dat","wb")
    

    if mode == 1: #Joueur vs Joueur
        if end == 1:
            setScore(l,p1,1,2)
            setScore(l,p2,-1,2)
                
        else:
            setScore(l,p1,-1,2)
            setScore(l,p2,1,2)
    elif mode == 2: #Joueur vs Ordi
        if p1.name != "":  #Si Joueur = Player 1
            if end == 1:
                setScore(l,p1,1,2)
            else:  
                setScore(l,p1,-1,2)  
        else:  #Si Joueur = Player 2
            if end == 1:
                setScore(l,p2,1,2)
            else:  
                setScore(l,p2,-1,2)         
    pickle.dump(l,f) #Ajout au fichier
    f.close()


def menuAllumette():
    """
    Procédure proposant le choix d'un affrontement entre joueurs,
    entre ordinateurs ou entre un joueur et un ordinateur au
    jeu des allumettes.

    Aucun argument.
    """
    choix : int
    J1 : str
    J2 : str

    choix = 0
    while choix != 4:
        print("⋆⋆⋆ ✪ ALLUMETTES ✪ ⋆⋆⋆")
        print("Règles : On dispose de 20 allumettes. Chaque joueur retirent à tour de rôle \n1,2 ou 3 allumettes. Celui qui retire la dernière allumette à perdu\n")
        choix = int(input("1 - J1 ⚔ J2\n2 - J1 ⚔ ORDI\n3 - ORDI ⚔ ORDI\n4 - Quitter\nChoix : "))
    
        if choix == 1:
            J1 = input("Nom du J1 : ")
            while J1 == "":
                J1 = input("Le nom de J1 ne doit pas être vide : ")
            J2 = input("Nom du J2 : ")
            while J2 == "" or J2 == J1:
                J2 = input("Le nom de J2 ne doit pas être vide, ni égal à celui du J1 : ")
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                allumettesGAME(J1,J2,1)
            else:
                print("\033[2;34m",J2,"\033[0;0mcommence !!")
                allumettesGAME(J2,J1,1)
            
        if choix == 2:
            J1 = input("Nom du J1 : ")
            while J1 == "":
                J1 = input("Le nom de J1 ne doit pas être vide : ")
            J2 = ""
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                allumettesGAME(J1,J2,2)
            else:
                print("\033[2;34mL'Ordi\033[0;0mcommence !!")
                allumettesGAME(J2,J1,2)
                
        if choix == 3:
            J1 = input("Nom de l'ordi 1 : ")
            J2 = input("Nom de l'ordi 2 : ")
            if randint(0,1) == 1:
                print("\033[2;34m",J1,"\033[0;0mcommence !!")
                allumettesGAME(J1,J2,3)
            else:
                print("\033[2;34mL'Ordi\033[0;0mcommence !!")
                allumettesGAME(J2,J1,3)
            
        elif choix == 4:
            print("Retour...")