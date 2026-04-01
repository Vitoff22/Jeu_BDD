import utils, random, time

def start_fight(equipe):
    manche = 1

    while True:
        choix_monstre = utils.monstre_choix()
        print(f"manche : {manche}")
        debut_manche(equipe.team, choix_monstre.team)
        if len(equipe.team) == 0:
            print("Vous avez perdu la partie")
            return manche
        manche += 1



def debut_manche(equipe, ennemi):
    while True:
        #attque de notre equipe
        attaque_equipe(equipe, ennemi)
        #affichage des participants
        showCharacters(equipe, ennemi)

        #verification si le monstre est mort

        if ennemi[0].hp == 0:
            print("Vous avez gagné la manche")
            break
        #attaque du monstre
        attaque_equipe2(ennemi, equipe)
        #affichage des participants
        showCharacters(equipe, ennemi)
        #verification si equipe est morte
        reste_equipe(equipe)
        #verifier si il reste des personnages dans l'equipe
        if len(equipe) == 0:
            print("Vous avez perdu la manche")
            break



def attaque_equipe(equipe, ennemi):
    for personnage in equipe:
        personnage.attaque(ennemi[0])

def attaque_equipe2(ennemi, equipe):
    #selection le perso a attaquer
    cible = random.choice(equipe)
    #attquer le perso
    ennemi[0].attaque(cible)


def showCharacters(equipe, ennemi):
    time.sleep(1)
    showCharactersMyTeam(equipe)
    print()
    showCharactersEnnemi(ennemi)

def showCharactersMyTeam(equipe):
    print("Mon équipe : ")
    for character in equipe:
        print(f"{character.name} : {character.atk} ATK -- {character.deff} DEF -- {character.hp} PV")

def showCharactersEnnemi(ennemi):
    print("Monstre : ")
    for character in ennemi:
        print(f"{character.name} : {character.atk} ATK -- {character.deff} DEF -- {character.hp} PV")

def reste_equipe(equipe):
    for personnage in equipe:
        if personnage.hp == 0:
            equipe.remove(personnage)