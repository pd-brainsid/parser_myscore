from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app, prefix="/api/v1")

USER_DATA = {
    "user": "1111"
}



class User(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id='%s')" % self.id


def verify(username, password):
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return User(id=123)


def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}


jwt = JWT(app, verify, identity)


class GamesResources(Resource):
    @jwt_required()
    def get(self, sport_name):
        import db

        games_info = db.get_games(sport_name)
        if len(games_info) == 0:
            answer = {
                'INFO': 'There is no information about this game for today'
            }
        else:
            answer = {
                'INFO': 'There is information about this game for today',
                sport_name: games_info
            }
        return answer


api.add_resource(GamesResources, '/games/<string:sport_name>')

if __name__ == '__main__':
    app.run(debug=True)
