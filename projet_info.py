""" 
Quentin Denolle
Le programme permet de jouer à la version en anglais et simplifiée de trivial poursuit
On peut choisir le nombre de joueur et la couleur des jetons
On voit sur le plateau où se situe chaque joueur
Les questions sont tirées aléatoirement à partie de la db trivia.sqlite3
J'ai utilisé le code donné dans le sujet
"""

# Importation des bibliothèques 
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sqlite3

# Fonctions
def debut_jeu():
    """ Cette fonction permet l'initialisation du jeu
    On demande le nombre de joueur et créé des listes utilisé plus tard contenant
    autant d'éléments que le nombre de joueur.    
    """
    score_joueurs = []
    nbr_joueur = 0
    position_joueurs = []
    couleur_pions = []
    # Je demande le nombre de joueur jusqu'à avoir une valeur valable
    while nbr_joueur < 1 or nbr_joueur > 6:
        print("The number of players must be between 1 and 6 inclusive.")
        nbr_joueur = int(input("Enter the number of players : "))
    for i in range(nbr_joueur):
    #Pour compter le score je créé une liste qui contient elle même des listes [1,2,3,4,5,6] car il y a 6 catégorie que j'ai numérotées.
    #A chaque fois qu'un joueur va valider une catégorie le chiffre va être remplacer par 0 et je vais compter le nombre de 0.
        score_joueurs.append([1,2,3,4,5,6])
        depart = int(input("Enter 0 to start on a green box,\n7 for orange,\n14 for blue,\
                           \n21 for red,\n28 for yellow\n35 for purple\n\n"))
        position_joueurs.append(depart)
        couleur_pion = input("Please indicate the colour of your pawn: \n")
        couleur_pions.append(couleur_pion)
    #Si 2 joueurs ou plus partent de la même case je redemande d'où il partent
    while position_joueurs.count(0) > 1 or position_joueurs.count(7) > 1 or position_joueurs.count(14) > 1 \
    or position_joueurs.count(21) > 1 or position_joueurs.count(28) > 1 or position_joueurs.count(35) > 1:
        print("Each player must start from a different square.")
        print(position_joueurs) 
        for j in range(nbr_joueur):
            depart = int(input("Enter zero to start on a green box, seven for orange, 14 for blue, \
                               21 for red, 28 for yellow and 35 for purple"))
            position_joueurs[j] = depart
    return nbr_joueur, score_joueurs, position_joueurs, couleur_pions


def deplacement(position_joueurs, joueur, couleur_cellule):
    """ Cette fonction permet le déplacement d'un joueur 
    On lance un dé, on demande ensuite au joueur dans quel sens il veut se déplacer,
    et enfin on lui indique sa nouvelle position.
    """
    de = random.randint(1,6)
    print("\nYou roll the dice... \nYou did: " + str(de))
    position_horaire = de + position_joueurs[joueur]
    #La position_horaire est la position (numero de la cellule) du joueur si il se déplace du sens horaire (compris entre 0 et 41)
    if position_horaire >= 42:
        position_horaire -= 42
    position_anti_horaire = position_joueurs[joueur] - de
    #La position_anti_horaire est la position (numero de la cellule) du joueur si il se déplace du sens anti_horaire (compris entre 0 et 41)
    if position_anti_horaire < 0:
        position_anti_horaire += 42
    choix_sens = int(input("Enter 1 to go clockwise, and go to a colored box " \
                           + str(couleur_cellule[position_horaire]) + \
                           ",\nor 0 to go counter-clockwise, and go to a colored box " \
                           + str(couleur_cellule[position_anti_horaire]) + "\n\n"))
    #J'actualise la position du joueur dans la liste position_joueurs en fonction du choix qu'il a fait
    if choix_sens == 1:
        position_joueurs[joueur] = position_horaire
    else : 
        position_joueurs[joueur] = position_anti_horaire
    print("You are currently on the cell " + str(position_joueurs[joueur]) + " coloured " \
          + str(couleur_cellule[position_joueurs[joueur]]))
    return position_joueurs


def affiche_plateau(position_joueurs, couleur_pions):
    """ Cette fonction permet l'affichage d'un plateau de jeu
    Pour chaque case du plateau on a une coordonnée.
    On place chaque pion avec la couleur que le joueur à choisi sur la position qui correspond.
    """
    i = 0
    #Pour chaque cellule je donne les coordonnées sur le plateau
    coordonnees = [[720,110],[790,160],[835,200],[870,250],[900,300],[930,360],[940,415],\
                   [940,500],[940,585],[930,640],[900,700],[870,750],[835,800],[790,840],\
                   [720,890],[650,920],[590,935],[530,950],[470,950],[410,935],[350,920],\
                   [280,890],[210,840],[165,800],[130,750],[100,700],[70,640],[60,585],\
                   [60,500],[60,415],[70,360],[100,300],[130,250],[165,200],[210,160],\
                   [280,110],[350,80],[410,65],[470,50],[530,50],[590,65],[650,80]]
    img = mpimg.imread('plateau.png')
    imgplot = plt.imshow(img)
    #Chaque joueur a un pion rond de la couleur choisi sur sa position
    while i < len(position_joueurs):
        circle= plt.Circle(coordonnees[position_joueurs[i]], radius= 20, color=couleur_pions[i])
        ax = plt.gca()
        ax.add_patch(circle)
        plt.axis('scaled')
        i += 1
    plt.show()
    return 


def calcul_score(position_joueurs, score_joueurs, joueur):
    """ Cette fonction permet de calculer le score d'un joueur
    Dans la fonction debut_jeu on a créé la liste score_joueur, qui contient 
    elle même des liste [1,2,3,4,5,6].
    Lorsque qu'un joueur répond correctement à une question intersection,
    on remplace le nombre de la liste correspondant à la catégorie par 0.
    Pour savoir le nombre de point d'un joueur, on compte le nombre de 0 dans sa liste.
    """
    #score_joueur contient (initialement) la liste [1,2,3,4,5,6] pour chaque joueur qui va ensuite être modifié
    score_joueur = score_joueurs[joueur]
    #J'ai numéroté chaque cellule avec l'intersection verte = 0, l'intersection orange = 7, ...
    #Chaque intersection est donc un multiple de 7 (0,7,14,21,28,35)
    categorie = (position_joueurs[joueur] / 7)    
    score_joueur[int(categorie)] = 0
    score = score_joueur.count(0)
    return score


def poserQuestion(couleur):
    """ Cette fonction permet de choisir et poser une question à un joueur
    A partir de la couleur de la case on détermine la catégorie.
    On stocke ensuite toutes les lignes du tableau question et de cette catégorie dans lst_question.
    On tire ensuite une ligne au hasard, puis on va chercher dans le tableau answer les lignes correspondantes.
    On stocke ensuite toutes les réponses dans lst_reponse et la réponse correcte dans reponse_correcte.
    On renvoie ensuite valeur_reponse en fonction de la réponse du joueur (bonne ou pas).
    """
    if couleur == "Green":
        categorie = "'Science & Nature'"
    elif couleur == "Orange":
        categorie = "'General Knowledge'"            
    elif couleur == "Blue":
        categorie = "'Geography'"            
    elif couleur == "Red":
        categorie = "'%Entertainment%'"          
    elif couleur == "Yellow":
        categorie = "'History'"
    else:
        categorie = "'Animals'"
    conn = sqlite3.connect('./trivia.sqlite3')
    c = conn.cursor()
    req_question = (f"SELECT * FROM question WHERE category LIKE {categorie}")
    c.execute(req_question)
    lst_question = c.fetchall()
    id_question, categorie, question = lst_question[random.randint(0,len(lst_question)-1)]
    req_reponse = (f"SELECT text FROM answer WHERE id_question={id_question}")
    req_rc = (f"SELECT text FROM answer WHERE id_question={id_question} AND is_correct=1")
    c.execute(req_reponse)
    lst_reponse = c.fetchall()
    c.execute(req_rc)
    reponse_correcte = c.fetchall()
    print(f"Here's a question from the category: {categorie}")
    print(question)
    print("Be sure to choose one of the following answers:")
    for i in lst_reponse:
        print(i[0])   
    reponse_joueur = input("My answer : ")
    print(f"The correct answer was: {reponse_correcte[0][0]}")
    if reponse_joueur == reponse_correcte[0][0]:
        valeur_reponse = True
    else:
        valeur_reponse = False
    conn.close()     
    return valeur_reponse


def jeu():
    """ Cettte fonction est la fonction principale, qui fait tourner le jeu
    Je commence par appeler la fonction debut_jeu, et je créé une liste qui contient chaque couleur de case.
    J'indique quel joueur joue et sa position, j'appele ensuite la fonction affichage_plateau.
    Je créé ensuite une boucle qui ne s'arrête que lorsqu'un joueur répond mal ou atteint 6 point.
    Lorsque cette boucle s'arrête je change de joueur et relance la boucle.
    J'arrête la fonction (et le jeu) lorsqu'un joueur atteint 6 points.
    """
    nbr_joueur, score_joueurs, position_joueurs, couleur_pions = debut_jeu()
    joueur = 0
    #J'ai créé une liste qui indique pour chaque cellule sa couleur (j'ai commencé par l'intersection verte)
    couleur_cellule = ["Green","Red","White","Blue","Purple","White","Yellow",\
                       "Orange","Yellow","White","Red","Green","White","Purple"\
                       ,"Blue","Purple","White","Yellow","Orange","White","Green",\
                       "Red","Green","White","Purple","Blue","White","Orange",\
                       "Yellow","Orange","White","Green","Red","White","Blue",\
                       "Purple","Blue","White","Orange","Yellow","White","Red"]  
    while True:
        valeur_reponse = True
        print("Player " + str(joueur + 1) + " it's up to you.")
        print("You are currently on the cell " + str(position_joueurs[joueur]) \
              + " coloured " + str(couleur_cellule[position_joueurs[joueur]]))
        affiche_plateau(position_joueurs, couleur_pions)
        while True:
            position_joueurs = deplacement(position_joueurs, joueur, couleur_cellule)
            affiche_plateau(position_joueurs, couleur_pions)
            #Je vérifie que le joueur soit sur une case de couleur et je lui pose ensuite une question avec la fonction poserQuestion
            #Si il répond bien il peut continuer de joueur
            if couleur_cellule[position_joueurs[joueur]]!="White" :
                valeur_reponse = poserQuestion(couleur_cellule[position_joueurs[joueur]])
                if valeur_reponse == True:
                    print("Bravo you have the right answer you can keep playing.")
            #Je regarde si le joueur a mal répondu et dans ce cas je change de joueur
            if valeur_reponse == False:
                print("Too bad you got the wrong answer.\n")
                break
            #Je regarde si le joueur est sur une intersection et dans ce cas je calcul ses points avec la fonction calcul_score
            if position_joueurs[joueur]==0 or position_joueurs[joueur]==7 or position_joueurs[joueur]==14 \
            or position_joueurs[joueur]==21 or position_joueurs[joueur]==28 or position_joueurs[joueur]==35:
                score = calcul_score(position_joueurs, score_joueurs, joueur)
                print("Your score is : " + str(score))
                #Si le joueur a 6 points (tous les points) le jeu s'arrêt
                if score == 6:
                    print("Congratulations on winning the game!")
                    return      
        if joueur < nbr_joueur - 1:
            joueur += 1
        else:
            joueur += 1 - nbr_joueur
    return

# Programme principale
jeu()