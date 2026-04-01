from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["jeu_video"]
characters = db["characters"]
monsters = db["monsters"]
user = db["user"]

def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["jeu_video"]
    
    
    characters = [
        {"name": "Guerrier",  "atk": 15, "def": 10, "hp": 100},
        {"name": "Mage",      "atk": 20, "def": 5,  "hp": 80},
        {"name": "Archer",    "atk": 18, "def": 7,  "hp": 90},
        {"name": "Voleur",    "atk": 12, "def": 12, "hp": 85},
        {"name": "Paladin",   "atk": 17, "def": 8,  "hp": 110},
        {"name": "Sorcier",   "atk": 22, "def": 4,  "hp": 70},
        {"name": "Chevalier", "atk": 19, "def": 6,  "hp": 120},
        {"name": "Moine",     "atk": 14, "def": 9,  "hp": 95},
        {"name": "Berserker", "atk": 25, "def": 3,  "hp": 80},
        {"name": "Chasseur",  "atk": 16, "def": 11, "hp": 90},
    ]
    
    monsters = [
        {"name": "Gobelin",    "atk": 10, "def": 5,  "hp": 50},
        {"name": "Orc",        "atk": 20, "def": 8,  "hp": 120},
        {"name": "Dragon",     "atk": 35, "def": 20, "hp": 300},
        {"name": "Zombie",     "atk": 12, "def": 6,  "hp": 70},
        {"name": "Troll",      "atk": 25, "def": 15, "hp": 200},
        {"name": "Spectre",    "atk": 18, "def": 10, "hp": 100},
        {"name": "Golem",      "atk": 30, "def": 25, "hp": 250},
        {"name": "Vampire",    "atk": 22, "def": 12, "hp": 150},
        {"name": "Loup-garou", "atk": 28, "def": 18, "hp": 180},
        {"name": "Squelette",  "atk": 15, "def": 7,  "hp": 90},
    ]

    # on vide les collections avant d'insérer les données
    db.characters.delete_many({})
    db.monsters.delete_many({})
    db.user.delete_many({})
    db.characters.insert_many(characters)
    db.monsters.insert_many(monsters)

if __name__ == "__main__":
    main()