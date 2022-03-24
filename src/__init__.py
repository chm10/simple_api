# src/__init__.py


from flask import Flask, jsonify
from flask_restx import Resource, Api


# instantiate the app
app = Flask(__name__)

api = Api(app)


class Status(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'API ok'
        }


api.add_resource(Status, '/status')