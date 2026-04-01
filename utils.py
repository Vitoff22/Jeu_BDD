
from pymongo import MongoClient
import models, random
client = MongoClient("mongodb://localhost:27017/")

db = client["jeu_video"]

def ajout_utilisateur(name):
    db["user"].insert_one({"name" : name, "score" : []})

def afficher_choix():
    for characters in list(db["characters"].find()):
        print(f"{characters["name"]} : {characters["atk"]} ATK -- {characters["def"]} DEF -- {characters["hp"]} PV")

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
    #liste des scores du joueur
    score_joueur = nouveau_score(creer_utilisateur, manche)
    #mettre a jour le score du joueur dans la base de donnee
    db["user"].update_one({"name" : creer_utilisateur}, {"$set" : {"score" : score_joueur}})

def nouveau_score(creer_utilisateur, manche):
    #recuperer les scores du joueur
    scores = list(db["user"].find({"name" : creer_utilisateur}))[0]["score"]
    #ajouter le nouveau score a la liste des scores
    scores.append(manche)
    #donner le score par ordre decroissant
    return sorted(scores, reverse=True)

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