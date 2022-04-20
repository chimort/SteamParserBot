import requests
import pandas as pd

from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&sort_by=_ASC&category1=998&snr=1_7_7_2300_7&specials=1&infinite=1'

genre_dict = {
    'action': 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&sort_by=_ASC&ignore_preferences=1&tags=19&snr=1_7_7_2300_7&specials=1&infinite=1',
    'for one player': 'https://store.steampowered.com/search/results/?query&start=50&count=50&dynamic_data=&sort_by=_ASC&category1=998&category3=2&snr=1_7_7_2300_7&specials=1&infinite=1',
    'strategy': 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&ignore_preferences=1&force_infinite=1&tags=9&specials=1&snr=1_7_7_2300_7&infinite=1',
    'horror': 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&ignore_preferences=1&force_infinite=1&tags=1667&specials=1&snr=1_7_7_2300_7&infinite=1',
    'coop': 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&sort_by=_ASC&ignore_preferences=1&category3=9&snr=1_7_7_2300_7&specials=1&infinite=1',
    'puzzle': 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&ignore_preferences=1&force_infinite=1&tags=1664&specials=1&snr=1_7_7_2300_7&infinite=1'
}


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
        start_price = game.find('div', {'class': 'search_price'}).text.strip()[0]
        discount = game.find('div', {'class': 'search_discount'}).text
        link = game.get('href')
        try:
            current_price = game.find('div', {'class': 'search_price'}).text.strip().split('$')[1]
        except:
            current_price = start_price

        suspect_games = {
            'title': title,
            'start_price': start_price + '$',
            'current_price': current_price + '$',
            'discount': discount.replace('\n', ''),
            'link': link
        }
        gamesList.append(suspect_games)
    return gamesList


def get_data(url, amount):
    result = []  # TOTAL LIST OF GAMES

    total_result = int(dict(requests.get(url).json())['total_count'])

    if amount != 0:
        result.append(parse(data_dict(url)))
    else:
        for products in range(0, total_result, 100):
            result.append(parse(data_dict(
                f'{url.replace("start=0", f"start={products}")}')))

    pd.concat([pd.DataFrame(g) for g in result]).to_csv('Games.csv', index=False)

    if amount != 0:
        return send_not_all_games(amount)


def send_not_all_games(amount):
    list_of_games = []
    if amount == 10:
        a = 11
    else:
        a = 21

    with open('Games.csv', 'r') as f:
        for item in f:
            if a == 0:
                break
            a -= 1
            list_of_games.append(item.replace('‚ё', '$').replace('в', '').strip())
    list_of_games.pop(0)
    card = '\n'.join('Title - {0} \n'
                     'Start Price - {1} \n'
                     'Current Price - {2}\n'
                     'Discount = {3}\n'
                     'Link - {4}\n'.format(item.split(',')[0],
                                           item.split(',')[1],
                                           item.split(',')[2],
                                           item.split(',')[3],
                                           item.split(',')[4], ) for item in list_of_games)

    return card


def main(amount=0, genre='all'):
    if genre != 'all':
        get_data(url=genre_dict.get(genre), amount=amount)
    else:
        get_data(url, amount=amount)


if __name__ == '__main__':
    main()
