from flask import Flask
from flask_restful import Resource, Api
import requests


app = Flask(__name__)
api = Api(app)


class WorkingResource(Resource):
    def get(self):
        return {
            "working": True,
        }


class PokemonByNameResource(Resource):
    def get(self, name):
        raw = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name)) # 200, 404
        if raw.ok:
            data = raw.json()
            abilities = []
            for a in data["abilities"]:
                abilities.append(a["ability"]["name"])
            return {
                "name": data["name"],
                "weight": data["weight"],
                "abilities": abilities,
            }
        return {
            "error": "an error happened"
        }, 400


api.add_resource(WorkingResource, "/")
api.add_resource(PokemonByNameResource, "/pokemon-by-name/<string:name>/")


if __name__ == "__main__":
    app.run(debug = True)


# GET /pokemon-by-name/<name>/ => {"name": "pikachu", "height": "4kg", "abilities": ["electric"]}