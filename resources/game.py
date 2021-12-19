from flask_restful import Resource
from flask import render_template, Response
from connectors.externalAPI import QueryAPI
from models.game import GameModel
from connectors.dbConnector import QueryDatabase
import logging

logger = logging.getLogger("werkzeug")

class GameByCategory(Resource):
    def get (self, name):
        from app import APPLICATION_VERSION
        querystring = {"category": name}
        gameList = GameModel.find_by_category(**querystring)
        if len(gameList) == 0:
            logger.info(f"Get games from API")
            gameList = QueryAPI.get_games_query(querystring)
            if gameList == None:
                return Response(render_template("error.html", mimetype='text/html'), status=404)
            #QueryDatabase.UpsertGameModelData(gameList)
        return Response(render_template("game.html", games=gameList, application_version = APPLICATION_VERSION, mimetype='text/html'), status = 200)

class GameByPlatform(Resource):
    def get(self, name):
        from app import APPLICATION_VERSION
        querystring = {"platform": name}
        gameList = GameModel.find_by_platform(**querystring)
        if len(gameList) == 0:
            gameList = QueryAPI.get_games_query(querystring)
            if gameList == None:
                return Response(render_template("error.html", mimetype='text/html'), status=404)
            #QueryDatabase.UpsertGameModelData(gameList)
        return Response(render_template("game.html", games=gameList, application_version = APPLICATION_VERSION, mimetype='text/html'), status = 200)


class GameList(Resource):
    def get (self):
        from app import APPLICATION_VERSION
        gameList = GameModel.find_all()
        if len(gameList) == 0:
            gameList = QueryAPI.get_games_query(None)
            if gameList == None:
                return Response(render_template("error.html", mimetype='text/html'), status = 404)
            QueryDatabase.UpsertGameModelData(gameList)
        return Response(render_template("game.html", games=gameList, application_version = APPLICATION_VERSION, mimetype='text/html'), status = 200)

