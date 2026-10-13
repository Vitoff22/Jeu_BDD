
import models, random
from database import create_client, database_name
client = create_client()

db = client[database_name()]

def ajout_utilisateur(name):
    # Replaying under the same name must not create a second empty score record.
    db["user"].update_one(
        {"name": name}, {"$setOnInsert": {"name": name, "score": []}}, upsert=True
    )

def afficher_choix():
    for characters in list(db["characters"].find()):
        print(f"{characters['name']} : {characters['atk']} ATK -- {characters['def']} DEF -- {characters['hp']} PV")

def personnage_dans_liste(personnages):
    for personnage in list(db["characters"].find()):
        if personnage["name"] == personnages:
            return True
    return False

def rappel_personnage(personnages):
    for personnage in list(db["characters"].find()):
        if personnage["name"] == personnages:
            return models.Characters(personnage["name"],personnage["atk"],personnage["def"],personnage["hp"])
        
def monstre_choix():
    equipe_monstre = models.Team()
    liste_monstre = list(db["monsters"].find())
    choix_monstre_random = random.choice(liste_monstre)
    choix_monstre_random = models.Characters(choix_monstre_random["name"],choix_monstre_random["atk"],choix_monstre_random["def"],choix_monstre_random["hp"])
    equipe_monstre.team.append(choix_monstre_random)
    return equipe_monstre

def enregistrer_score(creer_utilisateur, manche):
    # Atomic append: do not overwrite a score saved between a read and a write.
    db["user"].update_one(
        {"name": creer_utilisateur},
        {"$push": {"score": {"$each": [manche], "$sort": -1}}},
    )

def nouveau(creer_utilisateur):
    #recuperer les scores du joueur
    scores = list(db["user"].find({"name" : creer_utilisateur}))[0]["score"]
    #donner le score par ordre decroissant
    return verifier_score(scores)

def verifier_score(scores):
    if len(scores) < 3:
        return scores
    else:
        return scores[:3]
