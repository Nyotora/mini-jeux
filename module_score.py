from typing import BinaryIO
import pickle
from Joueur import PlayerInfo

def rechercheJoueur(l:list,nom:str) -> int:
    """
    Fonction qui vérifie l'existence d'un joueur et renvoie sa position dans la liste

    Entrée : l : tableau
             nom : chaine de caractère
    
    Retourne : entier
    """
    for i in range(len(l)):
        if l[i].name == nom:
            return i
    return -1

def setScore(l:list,Player:PlayerInfo,pts:int,game:int):
    """
    Procédure qui gère les scores

    Entrée : l : tableau -> liste des joueurs enregistrés
             Player : PlayerInfo
             pts : entier
             game : entier   -> Numéro du jeu
    
    Sortie : l : tableau
    """
    score : list
    nbGame : list

    score= [0,0,0,0]
    nbGame= [0,0,0,0]
    #Recherche de la position du joueur (même nom)
    pos = rechercheJoueur(l,Player.name)
    if pos != -1:
        score = l[pos].score #Copie du score du joueur dans la variable
        score[game-1] = score[game-1] + pts #Gestion des points
        l[pos].score = score #Remplacement de l'ancien score du joueur par le nouveau
        
        nbGame = l[pos].nbGame #Copie du nb de parties jouées dans la variable
        nbGame[game-1] = nbGame[game-1] + 1 #Incrémentation du nb de parties jouées selon le jeu
        l[pos].nbGame = nbGame #Remplacement de l'ancien nb de parties jouées par le nouveau
    else: #Cas où il n'existe pas
        score[game-1] = pts #Gestion des points
        Player.score = score
        nbGame[game-1] = 1 #Incrémentation du nb de parties jouées selon le jeu
        Player.nbGame = nbGame
        l.append(Player) # Ajout d'un nouveau joueur


def triJoueursInsert(l:list,gameID:int):
    """
    Procédure triant les joueurs à l'aide d'un tri par insertion

    Entrée : l : tableau
             gameID : entier   -> Numéro du jeu
    """
    j : int
    val : int
    i : int

    for i in range(1,len(l)):
        val = l[i]
        j = i
        while j>0 and l[j-1].score[gameID] < val.score[gameID]:
            l[j] = l[j-1]
            j = j-1
        l[j] = val

def affScoreRanked(gameName:str,gameID:int):
    """
    Procédure pour afficher le score des joueurs triés dans l'ordre croissant selon
    le jeu.

    Entrée : gameName : chaine de caractère
             gameID : entier
    """
    l : list
    i : int
    f : BinaryIO
    pos : int

    l = []
    pos = 1
    try:  #Le fichier existe-t-il ?
        f = open("data.dat","rb")
        l = pickle.load(f)
        f.close()
    except FileNotFoundError:
        print("Aucun fichier trouvé !")
    except EOFError:
        print("Aucun fichier trouvé !")

    if l == []:
        print("Désolé, mais aucun score n'est répertorié.")
    else:
        triJoueursInsert(l,gameID) #Tri des joueurs
        if l[0].nbGame[gameID] == 0: #Vérifie si le 1e joueur de la liste triée n'a pas loué à ce jeu
            print("Aucun joueur n'a joué à ce jeu")
        else:
            print("Résultat pour le jeu",gameName,"!")
            for i in range(len(l)):
                if l[i].nbGame[gameID] != 0:

                    #Incrémentation du rang ou non (par exemple en cas d'ex aequo, aucune incrémentation)
                    if i != 0:
                        if l[i].score[gameID] < l[i-1].score[gameID]:
                            pos = pos + 1
                    #Vérification du pluriel
                    if l[i].nbGame[gameID] == 1:
                        print("Rang",pos,":",l[i].name,"| Score :",l[i].score[gameID],"pour",l[i].nbGame[gameID],"partie jouée !")
                    else:
                        print("Rang",pos,":",l[i].name,"| Score :",l[i].score[gameID],"pour",l[i].nbGame[gameID],"parties jouées !")

