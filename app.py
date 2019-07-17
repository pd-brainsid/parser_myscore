from flask import Flask, jsonify
import db
import logging

APP = Flask(__name__)
logging.basicConfig(filename="log.log", level=logging.INFO)


@APP.route('/')
def index():
    return {
        'INFO': 'Hello! You can get info about completed soccer or hockey games for today'
    }


@APP.route('/api/games/<string:sport_name>', methods=['GET'])
def get_games(sport_name):

    logging.info(f"request for information about {sport_name}")
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


if __name__ == '__main__':
    logging.info(f"--------app started--------")

    APP.run(debug=True)
