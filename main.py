import utils,models,game

def main():

    #choisir entre jouer et afficher le classement
    utilisateur = choix_utilisateur()
    
    if utilisateur == '1':
        #si il veut jouer on demarre le jeu
        start_game()


    #si affichage classement
    
    #sinon quitter

def choix_utilisateur():

    while True:

        #choix d'un chiffre
        reponse = input("Tapez 1 pour jouer, \n2 pour les scores \n3 pour quitter ")
        #choix valide
        if reponse in ['1','2','3']:
            return reponse
        
def start_game():
    #creation utilisateur
    creer_utilisateur = input("Ecrire votre pseudo")
    while True:
        #ajouter a la base de donnee
        utils.ajout_utilisateur(creer_utilisateur)
        #creation equipe
        equipe = creer_equipe()
        #commencer le combat
        manche = game.start_fight(equipe)
        utils.enregistrer_score(creer_utilisateur, manche)
        montrerLeScores(creer_utilisateur, manche)
        if not rejouer():
            break


def creer_equipe():
#creation de la classe personnage
    MyTeam = models.Team()
    while len(MyTeam.team) != 3:
        #afficher les personnages
        utils.afficher_choix()
        #choisir personnage
        personnages = input('Choisir ton personnage ')
        #verification
        if verification_perso(personnages, MyTeam.team):
            #creation du perso dans la classe
            personnage_creation = utils.rappel_personnage(personnages)
            #ajout du perso dans l'equipe
            MyTeam.team.append(personnage_creation)
            #voir mon equipe
            showMyCharacters(MyTeam.team)
            print()
    return MyTeam

def showMyCharacters(listChoiceCharacters):
    print("Mon équipe : ")
    for character in listChoiceCharacters:
        print(f"{character.name} : {character.atk} ATK -- {character.deff} DEF -- {character.hp} PV")

def verification_perso(personnages, MyTeam):
    if personnage_unique(personnages, MyTeam) and utils.personnage_dans_liste(personnages):
        return True
    return False

def personnage_unique(personnages, MyTeam):
    for personnage in MyTeam:
        if personnages == personnage.name:
            return False
    return True
def montrerLeScores(creer_utilisateur, manche):
    #recuperer les 3 meilleurs scores 
    scores = utils.nouveau(creer_utilisateur)
    #afficher le score actuel et les 3 meilleurs scores
    voir_score(scores, manche)

def voir_score(scores, manche):
    print(f"Votre score : {manche}")
    for i in range(len(scores)):
        print(f"{i+1}- {scores[i]}")

def rejouer():
    while True:
        reponse = input("Voulez-vous rejouer ? (O/N) ")
        if reponse in ['O', 'N']:
            return reponse == 'O'

main()
