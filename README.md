# Jeu Python + MongoDB

Projet académique en ligne de commande : constituer une équipe de trois personnages, affronter des monstres et conserver les scores dans MongoDB. Il s'agit d'un jeu local, sans service web ni authentification des joueurs. Un pseudo n'est pas un compte protégé.

## Installation locale

Prérequis : Python 3.12 ou plus récent et une instance MongoDB locale accessible uniquement depuis la machine.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python db_init.py
.venv\Scripts\python main.py
```

`db_init.py` ajoute uniquement les personnages et monstres absents. Le relancer conserve les scores, les données personnalisées et les statistiques déjà enregistrées. Lancer cette initialisation une seule fois à la fois, avant le jeu. Les doublons éventuellement présents dans une ancienne base ne sont pas supprimés automatiquement.

Le menu de consultation globale du classement n'est pas encore implémenté ; les meilleurs scores du joueur sont présentés après une partie.

## Configuration et sécurité

- `MONGODB_URI` remplace l'adresse de connexion par défaut `mongodb://127.0.0.1:27017/`.
- `MONGODB_DB` remplace le nom de base par défaut `jeu_video`.
- Les deux scripts utilisent cette configuration commune, avec des délais d'attente réseau de cinq secondes.
- Ces variables sont lues dans l'environnement du processus. Aucun fichier `.env` n'est automatiquement chargé.

Pour un environnement partagé ou une connexion distante, configurer l'authentification MongoDB, un utilisateur dédié limité à cette base, TLS et un filtrage réseau. Ne pas ouvrir le port 27017 à Internet. Le programme ne configure pas ces protections à la place du serveur. Ne pas désactiver la validation des certificats TLS dans l'URI.

Garder les mots de passe et URI authentifiées dans l'environnement local ou un gestionnaire de secrets, jamais dans les sources, captures ou journaux partagés. `.gitignore` exclut les fichiers de secrets usuels, les sauvegardes et les caches ; il ne retire pas un secret déjà publié de l'historique. Conserver une sauvegarde avant toute intervention manuelle sur une base existante.

Documentation : [sécurisation de MongoDB](https://www.mongodb.com/docs/manual/administration/security-checklist/), [options PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/), [version PyMongo](https://pypi.org/project/pymongo/4.18.3/).

## Vérifications sans base réelle

```powershell
python -B -m unittest discover -s tests -v
```

Ces tests utilisent un faux client PyMongo en mémoire : conservation des scores et des données existantes, initialisation répétée, configuration et écritures atomiques. Ils ne valident pas une installation MongoDB, les permissions réseau ou les identifiants réels.
