import requests
from bs4 import BeautifulSoup


def bf_pre_process():
    global URL, soup
    URL = input('Paste your URL here: ')
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    identify_shop()

def identify_shop():
    params = [i for i in URL.split('/')]
    for param in params:
        for scopes in param.split('.'):
            if scopes == 'zalando':
                zalando()

            if scopes == 'allegro':
                allegro()

            if scopes == 'mediamarkt':
                mediamarkt()

def zalando():
    global soup, title, black_price, red_price
    title = soup.find_all('h1')
    black_price = soup.find_all('span', class_='uqkIZw ka2E9k uMhVZi FxZV-M z-oVg8 weHhRC ZiDB59')
    red_price = soup.find_all('span', class_="uqkIZw ka2E9k uMhVZi dgII7d z-oVg8 _88STHx cMfkVL")
    actuall_price = soup.find_all("span", class_="uqkIZw ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP")

    for i in title:
        title = i.get_text()

    for i in black_price:
        black_price = i.get_text()
        black_price = black_price.split()[0]
        black_price = float(black_price.replace(',','.'))

    for i in red_price:
        red_price = i.get_text()
        red_price = red_price.split()[0]
        red_price = float(red_price.replace(',','.'))

    for i in actuall_price:
        actuall_price = i.get_text()
        actuall_price = actuall_price.split()[0]
        actuall_price = float(actuall_price.replace(',','.'))

    promptcheck()

def allegro():
    global soup, title, black_price, red_price
    title = soup.find_all('h1', class_="_1s2v1 _1djie _4lbi0")
    red_price = soup.find_all('div', class_='_1svub _lf05o _9a071_3SxcJ')
    black_price = soup.find_all('s')
    for i in title:
        title = i.get_text()

    for i in black_price:
        black_price = i.get_text()
        black_price = black_price.split()[0]
        black_price = float(black_price.replace(',','.'))

    for i in red_price:
        red_price = i.get_text()
        red_price = red_price.split()[0]
        red_price = float(red_price.replace(',','.'))

    promptcheck()

def mediamarkt():
    global soup, title, black_price, red_price
    title = soup.find_all('h1', class_="b-ofr_headDataTitle")
    red_price = soup.find('div', class_="m-priceBox_price")
    black_price = soup.find('div', class_='m-priceBox_old')
    red_pric = [i for i in str(red_price).split()][3]
    black_pric = [i for i in str(black_price).split()][2]
    black_price = red_pric
    red_price = black_pric
    print(black_price)
    print(red_price)
    for i in title:
        title = i.get_text()
    print(title)
    promptcheck()

def promptcheck():
    global soup, title, black_price, red_price
    if black_price == []:
        black_price = red_price
        print(f'Actuall Price: {black_price}')
        print(f'Name of product: {title}')

    else:
        print('THIS PRODUCT IS FOR SALE!')
        print(f'Name of product: {title}')
        print(f'Actuall Price: {black_price}')
        print(f'Current price: {red_price}')

howmuch = int(input('How much products do you want to add for tracking?: '))
for i in range(howmuch):
    bf_pre_process()
