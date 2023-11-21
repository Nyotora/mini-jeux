from devinette import prog_Devinette
from allumetes import menuAllumette
from morpion import menuMorpion
from puissance4 import menuPuissance4
from module_score import affScoreRanked


if __name__ == "__main__":
    # Création des variables :
    choix : int

    #--------------------------
    choix = 0

    #DEBUT DU PROGRAMME : MENU PRINCIPAL
    while choix != 3:
        print("⋆⋆⋆ ✪ JEU ✪ ⋆⋆⋆")
        choix = int(input("1 - Jouer\n2 - Afficher les scores\n3 - Quitter\nChoix : "))

        #JOUER
        if choix == 1:
            while choix != 5:
                choix = int(input("1 - DEVINETTES\n2 - ALLUMETTES ☀\n3 - MORPION O✕\n4 - PUISSANCE 4 O✕\n5 - Quitter\nChoix : "))
                if choix == 1:
                    prog_Devinette()

                if choix == 2:
                    menuAllumette()

                if choix == 3:
                    menuMorpion()

                if choix == 4:
                    menuPuissance4()

                if choix == 5:
                    print("Retour...")

        #AFFICHER LES SCORES
        if choix == 2:
            while choix != 5:
                print("Afficher les scores pour quel jeu ?\n")
                choix = int(input("1 - DEVINETTES\n2 - ALLUMETTES ☀\n3 - MORPION O✕\n4 - PUISSANCE 4 O✕\n5 - Quitter\nChoix : "))
                if choix == 1:
                    affScoreRanked("Devinettes",0)

                if choix == 2:
                    affScoreRanked("Allumettes",1)

                if choix == 3:
                    affScoreRanked("Morpion",2)

                if choix == 4:
                    affScoreRanked("Puissance 4",3)

                if choix == 5:
                    print("Retour...")

        #QUITTER
        if choix == 3:
            print("Au revoir")
        print("----------------------------------")
    