from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

Base = declarative_base()
engine = create_engine('sqlite:///games.sqlite', echo=True)
logging.basicConfig(filename="log.log", level=logging.INFO)


class Game(Base):
    __tablename__ = 'games'
    id = Column(String, primary_key=True)
    discipline = Column(String)
    player_1 = Column(String)
    player_2 = Column(String)
    score_p_1 = Column(Integer)
    score_p_2 = Column(Integer)
    country = Column(String)
    league = Column(String)

    def __init__(self, id_, discipline, player_1, player_2, score_p_1, score_p_2, country, league):
        self.id = id_
        self.discipline = discipline
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_p_1 = score_p_1
        self.score_p_2 = score_p_2
        self.country = country
        self.league = league

    def __repr__(self):
        return f'{self.player_1} {self.score_p_1} : {self.score_p_2} {self.player_2}'


def create_table():
    logging.info("table is created")

    Base.metadata.create_all(engine)


def drop_table():
    logging.info("table is deleted")

    Base.metadata.drop_all(engine)


def convert_to_json(list_records):
    dict_view = {}

    for record in list_records:
        obj = {
            'discipline': record.discipline,
            'player_1': record.player_1,
            'player_2': record.player_2,
            'score_p_1': record.score_p_1,
            'score_p_2': record.score_p_2,
            'country': record.country,
            'league': record.league,
        }
        dict_view[record.id] = obj

    return dict_view


def get_games(sport_name):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    exists_records = [game for game in session.query(Game).filter(Game.discipline == sport_name)]
    session.commit()

    return convert_to_json(exists_records)


def add_games(games):
    if games is None:
        return
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    exists_records = [game.id for game in session.query(Game).order_by(Game.id)]
    for game_id, games_obj in games.items():
        if game_id in exists_records:
            continue
        session.add(games_obj)
        logging.info(f"{games_obj.id} added to DB")

    session.commit()
