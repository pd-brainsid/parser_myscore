from flask import Flask, jsonify
import db

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/games/<string:sport_name>', methods=['GET'])
def get_games(sport_name):

    return {sport_name: db.get_games(sport_name)}


if __name__ == '__main__':
    app.run(debug=True)
