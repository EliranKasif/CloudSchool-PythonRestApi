from db import db
from models.game import GameModel


class QueryDatabase:

    @classmethod
    def UpsertGameModelData(cls, jsonData):
        if jsonData is not None and len(jsonData) > 0:
            for gameJson in jsonData:
                game = GameModel(**gameJson)
                game.save_to_db()

    @classmethod
    def ReCreateSchema(cls, SCHEMA_NAME):
        db.session.execute(f"DROP DATABASE IF EXISTS {SCHEMA_NAME}")
        db.session.execute(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_NAME}")


