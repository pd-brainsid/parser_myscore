from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///games.sqlite', echo=True)


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
    Base.metadata.create_all(engine)


def add_games(games):

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    # print()
    exists_records = [game.id for game in session.query(Game).order_by(Game.id)]
    for game_id, games_obj in games.items():
        if game_id in exists_records:
            continue
        session.add(games_obj)
    session.commit()
