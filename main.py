import requests
import pandas as pd

from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&category1=998&snr=1_7_7_2300_7&specials=1&infinite=1'


def total_result(url):
    r = requests.get(url)
    data = dict(r.json())
    total_Result = data['total_count']

    return int(total_Result)


def get_data(url):
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
            'discount': discount.replace('\n', '').replace('-', '')
        }
        gamesList.append(suspect_games)
    return gamesList


def output(gamesList):
    gamesdf = pd.concat([pd.DataFrame(g) for g in result])
    gamesdf.to_csv('Games_price_list.csv', index=False)
    print(gamesdf.head())

    return


result = []
for x in range(0, 151, 50):
    data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&category1=998&snr=1_7_7_2300_7&specials=1&infinite=1')
    result.append(parse(data))


output(result)

# df = pd.read_csv('Games_price_list.csv')
# print(df.head())

