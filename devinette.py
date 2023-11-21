from random import randint      #importation de la fonction persmettant de choisir un entier aléatoire 
from getpass import getpass     #importation de la fonction permettant de cacher ce que l'on saisi dans le terminal
from time import sleep          #importation de la fonction permettant de faire une pause dans le programme
from typing import BinaryIO
from Joueur import PlayerInfo
from module_score import setScore
import pickle

#Fonction du menu du jeu (choix du mode, ou quitter)
def menu():
    '''
    Procédure qui affiche le menu principal du jeu, avec les différents modes de jeux

    (pas de paramètres)

    '''
    print()
    print("\033[38;5;208m ◦•●◉✿ | DEVINETTES | ✿◉●•◦ \033[0;0m ")
    print()
    print("Choisissez votre mode de jeu :")
    print()
    print("1- Joueur VS Joueur")
    print("2- Joueur VS Ordi")
    print("3- Ordi VS Ordi")
    print("4- Quitter le jeu")
    print()

def affNivDiff():
    '''
    Procédure qui affiche tous les niveaux de difficulté

    (pas de paramètres)
    
    '''
    print()
    print("Voici les niveaux de difficulté :")
    print()
    print("\033[38;5;150m 1) FACILE : -nombre secret : entre 0 et 20")
    print("             -nombre de chances : 5")
    print()
    print("\033[38;5;208m 2) MOYEN : -nombre secret : entre 0 et 50")
    print("            -nombre de chances : 8")
    print()
    print("\033[2;31m 3) DIFFILE : -nombre secret : entre 0 et 100")
    print("              -nombre de chances : 12 \033[0;0m ")
    print()

def partie_Avec_Joueur(pseudo2 : str, nb_secret : int, nb_chance : int) -> bool :
    '''
    Fonction qui fait se dérouler la partie lorsque le mode est Joueur_Joeur ou Joueur_VS_Ordi, et qui renvoie 
    un booléen vrai si le joueur J2 a gagné ou bien faux s'il a perdu.

    paramètres d'entrée :
        - pseudo2 : entier  -> pseudo du J2
        - nb_secret : entier  -> nombre secret
        - nb_chance : entier  -> nombre de chance restants
    
    paramètre de sortie :
        - gagne : booléen  -> booléen qui permet de savoir si l'ordi J2 a gagné
    '''
  
    maxChance : int
    gagne : bool
    nb : int
    f : BinaryIO
    l : list

    maxChance = nb_chance
    gagne = False

    #tant que le J2 n'a pas gagné et qu'il n'a pas épuisé ses chances, la partie continue
    while not gagne and nb_chance != 0 :

        #Saisie du nombre auquel pense le joueur J2
        print()
        print(pseudo2, end ="")
        nb = int(input(", saisissez le nombre auquel vous pensez :  "))

        # Comparaison du nombre proposé et le nombre secret, puis indication donné à l'utilisateur
        if nb < nb_secret :
            print("Trop petit !")
        elif nb > nb_secret:
            print("Trop grand !")
        else :
            print("C'est gagné !")
            gagne = True
        
        # à chaque boucle on décrémente 1 au nombre de chance et on l'affiche s'il n'a pas gagné
        if not gagne :
            nb_chance = nb_chance - 1
            print()
            print("Il te reste ", nb_chance," chances")
    
    #===== GESTION DES SCORES ================================

    #Création structure PlayerInfo
    p1 = PlayerInfo()
    p1.name = pseudo2

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

    if gagne:
        setScore(l,p1,nb_chance,1)
    else:
        setScore(l,p1,-maxChance//2,1)         
    pickle.dump(l,f) #Ajout au fichier
    f.close()

    return gagne

def partie_Ordi_VS_Ordi(pseudo2 : str, nb_secret : int, lim_nb : int , nb_chance : int) -> bool : 
    '''
    Fonction qui fait se dérouler la partie lorsque le mode est Ordi_VS_Ordi, et qui renvoie un booléen 
    vrai si l'ordi J2 a gagné ou bien faux s'il a perdu.

    paramètres d'entrée :
        - pseudo2 : entier  -> pseudo du J2
        - nb_secret : entier  -> nombre secret
        - lim_nb : entier  -> limite du nombre a deviner
        - nb_chance : entier  -> nombre de chance restants
    
    paramètre de sortie :
        - gagne : booléen  -> booléen qui permet de savoir si l'ordi J2 a gagné
    '''
    intelligence : int
    gagne : bool
    nb : int
    ajout : int

    gagne = False

    #On chosit aléatoirement si l'ordinateur qui devine joue bêtement ou intelligemment
    intelligence = randint(0,1)
  
    #Ici c'est la manière aléatoire de jouer de l'ordi "bête"
    if intelligence == 0 :

        #Boucle  qui s'exécute tant que l'ordi J2 n'a pas gagné et qu'il n'a pas épuisé toutes ses chances 
        while not gagne and nb_chance != 0 :

            #Affichage du nombre que l'ordi J2 a choisi aléatoirement
            print()
            nb = randint(1, lim_nb)
            print(pseudo2, ", saisissez le nombre auquel vous pensez : ", nb )
           
           #Comparaison entre le nombre secret et celui choisi par l'ordi J2 + indication (avec une pause pour que l'on puisse suivre)
            sleep(2)
            if nb < nb_secret :
                print("Trop petit !")
            elif nb > nb_secret:
                print("Trop grand !")
            else :
                print("C'est gagné !")
                gagne = True
            
            #On décrémente 1 au nombre de chance, puis on affiche le nombre de chance qu'il reste, si l'ordi J2 n'a pas gagné
            if not gagne :
                nb_chance = nb_chance - 1
                print()
                print("Il te reste ", nb_chance," chances")
            #petite pause pour que l'on puisse suivre la partie en temps réel
            sleep(3)
        
    #Ici c'est la manière intelligente de joueur de l'ordi intelligent
    else :
        
        nb = lim_nb // 2    #nombre que l'ordi va prposer, commence par proposer le nombre au cente de l'ensemble de définition
        ajout= nb           #valeur que l'on va ajouter ou soustraire au nombre que l'ordi J2 va proposer

        #Boucle  qui s'exécute tant que l'ordi J2 n'a pas gagné et qu'il n'a pas épuisé toutes ses chances
        while not gagne and nb_chance != 0 :

            ajout = ajout // 2   

            #Affichage du nombre proposé par l'ordi J2
            print()
            print(pseudo2, ", saisissez le nombre auquel vous pensez : ", nb )
            
            #Comparaison entre le nombre secret et celui choisi par l'ordi J2 + indication + calcul du prochain nombre à proposer + pause
            sleep(2)
            if nb < nb_secret :
                print("Trop petit !")
                nb= nb + ajout + 1        #ajout du nombre stratégique au nombre proposé pour le prochain tour

            elif nb > nb_secret:
                print("Trop grand !")
                nb= nb - ajout - 1        #soustraction du nombre stratégique au nombre proposé pour le prochain tour

            else :
                print("C'est gagné !")
                gagne = True
            
            #On décrémente 1 au nombre de chance, puis on affiche le nombre de chance qu'il reste, si l'ordi J2 n'a pas gagné
            if not gagne :
                nb_chance = nb_chance - 1
                print()
                print("Il te reste ", nb_chance," chances")
            #petite pause pour que l'on puisse suivre la partie en temps réel
            sleep(3)

    return gagne

def jeu(mode : int):
    '''
    Procédure du jeu en lui-même, qui fonctionne selon le mode de jeu choisi

    paramètre d'entrée : le mode de jeu -> entier
    
    '''

    pseudo1 : str
    pseudo2 : str
    diff : int
    lim_nb : int
    nb_chance : int
    nb_secret : int
    gagne : bool

    #Saisie des pseudo
    pseudo1 = input("Pseudo J1 : ")
    pseudo2 = input("Pseudo J2 : ")
    
    #Choix de la difficulté
    affNivDiff()
    diff = int(input("Choisir le niveau de difficulté : "))

    #Choix de la limite du nombre secret ainsi que du nombre d'essai, selon la difficulté
    if diff == 1 :
        lim_nb = 20
        nb_chance = 5
    
    elif diff == 2 :
        lim_nb = 50
        nb_chance = 8

    elif diff == 3 :
        lim_nb = 100
        nb_chance = 12
    print()

    #Choix du nombre secret en mode Joueur VS Joueur
    if mode == 1 :
         
        print(pseudo1, "veuillez saisir un nombre secret entre 0 et",lim_nb, " : ")

        #permet de saisir le nombre secret sans qu'il s'affiche dans le terminal
        nb_secret = int(getpass("nombre secret :"))

        #Vérification de la saisie, redemande la saisie du nombre secret si le nombre n'est pas dans l'ensemble de définition
        while nb_secret >= lim_nb or nb_secret < 0:
            print("\033[2;31mErreur de saisie \033[0;0m ")
            print(pseudo1, "veuillez saisir un nombre secret entre 0 et ",lim_nb, " : ")
            nb_secret = int(getpass("nombre secret :"))
        
        print()
        print("Le joueur J1 -", pseudo1, " a choisi son nombre secret, J2 -", pseudo2," à vous de le deviner !")

    
    elif mode == 2 :#Choix du nombre secret en mode Joueur VS Ordi

        nb_secret = randint(1, lim_nb)
        print()
        print("L'ordi J1 -", pseudo1, " a choisi le nombre secret, J2 -", pseudo2, " à vous de le deviner !")

    
    else :#Choix du nombre secret en mode Ordi VS Ordi
        nb_secret = randint(1, lim_nb)
        print()
        print("L'ordi J1 -", pseudo1, " a choisi le nombre secret, à l'ordi J2 -", pseudo2, " de le deviner !")


    #Exécution de la fonction du déroulement de la partie selon le mode de jeu
    if mode == 1 or mode == 2:

        gagne = partie_Avec_Joueur(pseudo2, nb_secret, nb_chance)
    
    else : 
        gagne = partie_Ordi_VS_Ordi(mode, pseudo1, pseudo2, nb_secret, lim_nb, nb_chance)
    
    #s'il n'a pas gagné après avoir epuisé ses chances, J2 a perdu, et J1 a agné
    if not gagne :
        print("PERDU... Le nombre était : ", nb_secret)
        print()
        print("⭐ Vainqueur :  ", pseudo1, " ⭐")

    #s'il a gagné alors on l'affiche
    else : 
        print()
        print("⭐ Vainqueur :  ", pseudo2, " ⭐")

#--------------------------------------------------------------

#programme principal du jeu devinettes

def prog_Devinette():
    '''
    Procédure principale du jeu des devinettes

    (pas de paramètres)
    
    '''
    choix : int
    quitter : bool

    choix = 0
    quitter = False

    #Boucle qui affiche le menu et lance les différentes parties selon le choix saisi 
    #tant que l'utilisateur ne decide de quitter le jeu en saisissant le choix 4
    while not quitter :

        menu()

        #Saisie du choix
        choix = int(input("Veuillez saisir le numéro du mode de votre choix : "))


        if choix == 1 :
            #Affichage de bienvenue et des règles selon le mode de jeu choisi
            print()
            print("Bienvenue dans le mode Joueur VS Joueur !")
            print()
            print("Règles : Le joueur J1 doit faire deviner un nombre au joueur J2.")
            print()

            jeu(1)

        elif choix == 2 :
            print()
            print("Bienvenue dans le mode Joueur VS Ordi !")
            print()
            print("Règles : Le ordi J1 doit faire deviner un nombre au joueur J2.")
            print()

            jeu(2)

        elif choix == 3 :
            print()
            print("Bienvenue dans le mode Ordi VS Ordi !")
            print()
            print("Règles : L'ordi J1 doit faire deviner un nombre à l'ordi J2.")
            print()

            jeu(3)
        
        elif choix == 4 :

            quitter = True




