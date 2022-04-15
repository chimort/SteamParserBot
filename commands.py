import requests
import pandas as pd

from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&category1=998&snr=1_7_7_2300_7&specials=1&infinite=1'


def data_dict(url):
    r = requests.get(url)
    data = dict(r.json())

    return data['results_html']


def parse(data):
    gamesList = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', {'class': 'title'}).text
        start_price = game.find('div', {'class': 'search_price'}).text.strip().split('₸')[0]
        discount = game.find('div', {'class': 'search_discount'}).text
        try:
            current_price = game.find('div', {'class': 'search_price'}).text.strip().split('₸')[1]
        except:
            current_price = start_price

        # print(title, start_price, current_price, discount)

        suspect_games = {
            'title': title,
            'start_price': start_price,
            'current_price': current_price,
            'discount': discount.replace('\n', '')
        }
        gamesList.append(suspect_games)
    return gamesList


def get_data(url):
    result = []  # TOTAL LIST OF GAMES

    total_result = int(dict(requests.get(url).json())['total_count'])

    for products in range(0, total_result, 100):
        result.append(parse(data_dict(
            f'https://store.steampowered.com/search/results/?query&start={products}&count=100&dynamic_data=&sort_by=_ASC&category1=998&snr=1_7_7_2300_7&specials=1&infinite=1')))

    """NEED TO ADD GENRE AND AMOUNT OF GAMES"""

    pd.concat([pd.DataFrame(g) for g in result]).to_csv('Games.csv', index=False)


def main():
    get_data(url)


if __name__ == '__main__':
    main()
