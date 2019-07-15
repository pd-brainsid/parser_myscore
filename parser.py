from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import selenium

DRIVER = webdriver.Chrome()

ADDRESSES = {
    'soccer': 'https://www.myscore.com.ua/football',
    'hockey': 'https://www.myscore.com.ua/hockey/',
}


def open_selected_sport_completed_games(sport_name):
    c_address = ADDRESSES.get(sport_name)

    DRIVER.get(c_address)
    ul = DRIVER.find_element_by_css_selector('ul.tabs__list')
    items = ul.find_elements_by_tag_name("li")

    for item in items:
        if item.text == 'Завершенные':
            item.click()
            return


def get_all_leagues(sport_name):
    games_list = DRIVER.find_element_by_css_selector(f'div.sportName.{sport_name}')
    items = games_list.find_elements_by_css_selector('div.event__header.event__header--no-my-games')
    (games_list.find_elements_by_class_name('event__match.event__match--oneLine'))

    for item in items:
        try:
            # item.find_element_by_css_selector('div.event__expander.icon--expander.expand').click()
            item.find_element_by_css_selector('div.event__expander.icon--expander.collapse').click()
        except NoSuchElementException:
            pass
    #
    # for item in items:
    #     title_box = item.find_element_by_css_selector('div.event__titleBox')
    #     country = title_box.find_element_by_css_selector('span.event__title--type').text
    #     league_name = title_box.find_element_by_css_selector('span.event__title--name').text
    #     item.find_element_by_css_selector('div.event__expander.icon--expander.expand').click()
    #     print(country, league_name)
    #     # participant_home =
    #     # participant_away =
    #     print(len(games_list.find_elements_by_class_name('event__match.event__match--oneLine')))
    #     item.find_element_by_css_selector('div.event__expander.icon--expander.collapse').click()




open_selected_sport_completed_games('soccer')
get_all_leagues('soccer')
