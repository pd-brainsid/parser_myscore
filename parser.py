from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import db
import datetime
import time
import logging

DRIVER = webdriver.Chrome()
DATE = None
logging.basicConfig(filename="log.log", level=logging.INFO)

ADDRESSES = {
    'soccer': 'https://www.myscore.com.ua/football',
    'hockey': 'https://www.myscore.com.ua/hockey/',
}


def open_selected_sport_completed_games(sport_name):
    c_address = ADDRESSES.get(sport_name)
    logging.info(f"open {c_address}")

    DRIVER.get(c_address)
    ul = DRIVER.find_element_by_css_selector('ul.tabs__list')
    items = ul.find_elements_by_tag_name("li")

    for item in items:
        if item.text == 'Завершенные':
            item.click()
            return


def get_all_leagues(sport_name):
    games = {}
    try:
        games_list = DRIVER.find_element_by_css_selector(f'div.sportName.{sport_name}')
        logging.info(f"there are completed {sport_name} games for today")

    except NoSuchElementException:
        logging.info(f"there are no completed {sport_name} games today")
        return

    items = games_list.find_elements_by_css_selector('div.event__header')
    (games_list.find_elements_by_class_name('event__match.event__match--oneLine'))

    for extended_item in items:
        try:
            extended_item.find_element_by_css_selector('div.event__expander.icon--expander.collapse').click()
        except NoSuchElementException:
            pass

    for item in items:
        title_box = item.find_element_by_css_selector('div.event__titleBox')
        country = title_box.find_element_by_css_selector('span.event__title--type').text
        league_name = title_box.find_element_by_css_selector('span.event__title--name').text
        item.find_element_by_css_selector('div.event__expander.icon--expander.expand').click()
        current_league_games = games_list.find_elements_by_class_name('event__match.event__match--oneLine')
        for game in current_league_games:
            id_ = game.get_attribute('id')
            stage = game.find_element_by_css_selector('div.event__stage').text
            if stage != 'Завершен':
                # delete canceled games
                current_league_games.remove(game)
                continue
            participant_home = game.find_element_by_css_selector('div.event__participant.event__participant--home').text
            participant_away = game.find_element_by_css_selector('div.event__participant.event__participant--away').text

            score_1, score_2 = None, None
            if sport_name == 'soccer':
                score_1, score_2 = game.find_elements_by_css_selector('span')
            elif sport_name == 'hockey':
                score_1 = game.find_element_by_css_selector('div.event__score.event__score--home').text
                score_2 = game.find_element_by_css_selector('div.event__score.event__score--away').text

            if score_1 is None or score_2 is None:
                continue

            game_obj = db.Game(id_, sport_name, participant_home, participant_away, score_1.text, score_2.text, country,
                               league_name)
            games[id_] = game_obj

        if len(current_league_games) == 0:
            # Deleting a record of the league if there were only canceled games in it
            items.remove(item)

        item.find_element_by_css_selector('div.event__expander.icon--expander.collapse').click()
    return games


if __name__ == '__main__':

    logging.info("---------Parser started---------")
    db.create_table()
    DATE = datetime.date.today()
    logging.info(f"set DATE {DATE}")

    while True:
        if DATE != datetime.date.today():
            db.drop_table()
            db.create_table()
            DATE = datetime.date.today()
            logging.info(f"set DATE {DATE}")

        for game_name in ADDRESSES:
            logging.info(f"started get info about {game_name}")
            open_selected_sport_completed_games(game_name)
            games = get_all_leagues(game_name)
            db.add_games(games)

        time.sleep(3600)
