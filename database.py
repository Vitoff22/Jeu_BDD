"""Shared local database configuration. Never print connection strings."""
import os

from pymongo import MongoClient


def database_name():
    return os.environ.get("MONGODB_DB", "jeu_video")


def create_client():
    # The default is a local development instance, not a publicly exposed server.
    return MongoClient(
        os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017/"),
        connect=False,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
    )
