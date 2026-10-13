"""Regression checks with an in-memory PyMongo stand-in; never connect to MongoDB."""
import copy
import importlib
import os
import sys
import types
import unittest
from unittest.mock import patch


class FakeCollection:
    def __init__(self, documents=()):
        self.documents = copy.deepcopy(list(documents))
        self.updates = []

    def update_one(self, query, update, upsert=False):
        self.updates.append((copy.deepcopy(query), copy.deepcopy(update), upsert))
        document = next((item for item in self.documents if all(item.get(k) == v for k, v in query.items())), None)
        if document is None and upsert:
            document = dict(query)
            document.update(copy.deepcopy(update.get("$setOnInsert", {})))
            self.documents.append(document)
        if document is not None and "$push" in update:
            for key, operation in update["$push"].items():
                document.setdefault(key, []).extend(copy.deepcopy(operation["$each"]))
                document[key].sort(reverse=operation.get("$sort") == -1)
        # Deliberately no delete/drop methods: destructive initialization fails tests.

    def find(self, query=None):
        return copy.deepcopy([item for item in self.documents if all(item.get(k) == v for k, v in (query or {}).items())])


class FakeDatabase:
    def __init__(self):
        self.collections = {}
        self.accessed = []

    def __getitem__(self, key):
        self.accessed.append(key)
        return self.collections.setdefault(key, FakeCollection())


class FakeClient:
    def __init__(self, *args, **kwargs):
        self.databases = {}
        self.closed = False

    def __getitem__(self, key):
        return self.databases.setdefault(key, FakeDatabase())

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


fake_pymongo = types.ModuleType("pymongo")
fake_pymongo.MongoClient = FakeClient
fake_errors = types.ModuleType("pymongo.errors")
fake_errors.PyMongoError = type("PyMongoError", (Exception,), {})
with patch.dict(sys.modules, {"pymongo": fake_pymongo, "pymongo.errors": fake_errors}):
    import database
    import db_init
    import utils


class SecurityTests(unittest.TestCase):
    def test_seed_never_accesses_or_erases_user_scores(self):
        db = FakeDatabase()
        original = [{"name": "Julien", "score": [12, 8, 5]}]
        db.collections["user"] = FakeCollection(original)
        db_init.seed_database(db)
        self.assertEqual(db.collections["user"].documents, original)
        self.assertNotIn("user", db.accessed)

    def test_repeated_seed_adds_no_duplicate_reference_entries(self):
        db = FakeDatabase()
        db_init.seed_database(db)
        before = {name: copy.deepcopy(collection.documents) for name, collection in db.collections.items()}
        db_init.seed_database(db)
        self.assertEqual(len(db["characters"].documents), 10)
        self.assertEqual(len(db["monsters"].documents), 10)
        self.assertEqual(before, {name: collection.documents for name, collection in db.collections.items()})

    def test_seed_preserves_modified_stats_and_custom_monsters(self):
        db = FakeDatabase()
        mage = {"name": "Mage", "atk": 31, "def": 8, "hp": 92, "custom": True}
        boss = {"name": "Boss personnalisé", "atk": 2, "def": 2, "hp": 2}
        db.collections["characters"] = FakeCollection([mage])
        db.collections["monsters"] = FakeCollection([boss])
        db_init.seed_database(db)
        self.assertIn(mage, db["characters"].documents)
        self.assertIn(boss, db["monsters"].documents)
        self.assertEqual(len(db["characters"].documents), 10)
        self.assertEqual(len(db["monsters"].documents), 11)

    def test_seed_closes_client_if_an_operation_fails(self):
        client = FakeClient()
        with patch.object(db_init, "create_client", return_value=client), patch.object(db_init, "seed_database", side_effect=fake_errors.PyMongoError):
            with self.assertRaises(fake_errors.PyMongoError):
                db_init.main()
        self.assertTrue(client.closed)

    def test_client_defaults_to_loopback_with_bounded_lazy_connection(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(database, "MongoClient") as constructor:
            database.create_client()
            constructor.assert_called_once_with("mongodb://127.0.0.1:27017/", connect=False, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000, socketTimeoutMS=5000)
            self.assertEqual(database.database_name(), "jeu_video")

    def test_connection_and_database_are_configurable(self):
        with patch.dict(os.environ, {"MONGODB_URI": "mongodb://127.0.0.1:27018/", "MONGODB_DB": "jeu_test"}), patch.object(database, "MongoClient") as constructor:
            database.create_client()
            self.assertEqual(constructor.call_args.args[0], "mongodb://127.0.0.1:27018/")
            self.assertEqual(database.database_name(), "jeu_test")

    def test_replaying_does_not_duplicate_or_reset_user(self):
        db = FakeDatabase()
        original = {"name": "Julien", "score": [12, 8]}
        db.collections["user"] = FakeCollection([original])
        with patch.object(utils, "db", db):
            utils.ajout_utilisateur("Julien")
            utils.ajout_utilisateur("Julien")
        self.assertEqual(db["user"].documents, [original])

    def test_new_user_is_created_only_once(self):
        db = FakeDatabase()
        with patch.object(utils, "db", db):
            utils.ajout_utilisateur("Nouveau")
            utils.ajout_utilisateur("Nouveau")
        self.assertEqual(db["user"].documents, [{"name": "Nouveau", "score": []}])

    def test_score_append_preserves_previous_scores_and_order(self):
        db = FakeDatabase()
        db.collections["user"] = FakeCollection([{"name": "Julien", "score": [12, 8]}])
        with patch.object(utils, "db", db):
            utils.enregistrer_score("Julien", 10)
            utils.enregistrer_score("Julien", 15)
            self.assertEqual(utils.nouveau("Julien"), [15, 12, 10])
        self.assertEqual(db["user"].documents[0]["score"], [15, 12, 10, 8])
        self.assertTrue(all("$push" in update and "$set" not in update for _, update, _ in db["user"].updates))

    def test_importing_main_does_not_start_an_interactive_game(self):
        with patch.dict(sys.modules, {"pymongo": fake_pymongo, "pymongo.errors": fake_errors}), patch("builtins.input", side_effect=AssertionError("Unexpected interactive prompt")):
            importlib.import_module("main")


if __name__ == "__main__":
    unittest.main()
