from flask_restful import Resource
from flask import Response
from connectors.dbConnector import QueryDatabase
import logging
logger = logging.getLogger("werkzeug")

class ReCreateSchema(Resource):
    def get(self):
        from app import SCHEMA_NAME
        QueryDatabase.ReCreateSchema(SCHEMA_NAME)
        result = { "Status" : 200,
                   "Message": "Recreate schema"
                   }
        return Response(result, status=200)

