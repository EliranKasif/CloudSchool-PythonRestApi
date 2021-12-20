from flask_restful import Resource
from flask import render_template, Response
from connectors.externalAPI import QueryAPI
from models.game import GameModel
from connectors.dbConnector import QueryDatabase
import logging

logger = logging.getLogger("werkzeug")

class Utils:
    @classmethod
    def response_generator(cls, gameList):
        from app import APPLICATION_VERSION, instanceid
        if gameList == None:
            return Response(render_template("error.html", mimetype='text/html'), status=404)
        return Response(render_template("game.html", games=gameList, application_version=APPLICATION_VERSION, instance_id=instanceid, mimetype='text/html'), status = 200)

class GameByCategory(Resource):
    def get (self, name):
        querystring = {"category": name}
        gameList = GameModel.find_by_category(**querystring)
        if len(gameList) == 0:
            logger.info(f"Get games from API")
            gameList = QueryAPI.get_games_query(querystring)
        return Utils.response_generator(gameList)

class GameByPlatform(Resource):
    def get(self, name):
        querystring = {"platform": name}
        gameList = GameModel.find_by_platform(**querystring)
        if len(gameList) == 0:
            gameList = QueryAPI.get_games_query(querystring)
        return Utils.response_generator(gameList)


class GameList(Resource):
    def get (self):
        gameList = GameModel.find_all()
        if len(gameList) == 0:
            gameList = QueryAPI.get_games_query(None)
        return Utils.response_generator(gameList)

