from pymongo.errors import PyMongoError

from database import create_client, database_name


def seed_database(db):
    """Add missing reference data without deleting or replacing saved data."""
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

    # Only insert missing reference entries. Existing stats and user scores stay intact.
    # Run initialization once at a time, before starting the local CLI game.
    for collection, documents in (("characters", characters), ("monsters", monsters)):
        for document in documents:
            db[collection].update_one(
                {"name": document["name"]}, {"$setOnInsert": document}, upsert=True
            )


def main():
    with create_client() as client:
        seed_database(client[database_name()])
    print("Personnages et monstres initialisés. Les scores existants sont conservés.")

if __name__ == "__main__":
    try:
        main()
    except PyMongoError:
        raise SystemExit("Initialisation impossible. Vérifiez MongoDB et MONGODB_URI. Aucune réinitialisation des scores n'a été demandée.") from None
