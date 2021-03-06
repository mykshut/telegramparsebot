import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv
import random
import smtplib

all_titles = []
all_black_prices = []
all_red_prices = []
USERS = []
IDS = []
EMAILS = []

def bf_pre_process(URL): #1
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    identify_shop(URL, soup)

def identify_shop(URL, soup): #2
    shops = ['zalando', 'allegro', 'mediamarkt']
    params = [i for i in URL.split('/')]
    for param in params:
        for scopes in param.split('.'):
            if scopes == 'zalando':
                findshop(scopes, URL)
                zalando(soup)

            if scopes == 'allegro':
                findshop(scopes, URL)
                allegro(soup)

            if scopes == 'mediamarkt':
                findshop(scopes, URL)
                mediamarkt(soup)

            if scopes == 'coffeeproficiency':
                findshop(scopes, URL)
                coffeeproficiency(soup)

            if scopes == 'mediaexpert':
                findshop(scopes, URL)
                mediaexpert(soup)


def zalando(soup): #3.1
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

    promptcheck(title, black_price, red_price)

def allegro(soup): #3.2
    title = soup.find_all('h1', class_="_1s2v1 _1djie _4lbi0")
    red_price = soup.find_all('div', class_='_1svub _lf05o _9a071_3SxcJ')
    black_price = soup.find_all('s')
    or_black_price = soup.find_all('span', class_="_qnmdr")

    if black_price == []:
        black_price = red_price
        red_price = []

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

    promptcheck(title, black_price, red_price)

def mediamarkt(soup): #3.3
    title = soup.find_all('h1', class_="b-ofr_headDataTitle")
    red_price = soup.find('div', class_="m-priceBox_price")
    black_price = soup.find('div', class_='m-priceBox_old')
    red_price = [i for i in str(red_price).split()][3]
    black_price = [i for i in str(black_price).split()][2]

    for i in title:
        title = i.get_text()

    promptcheck(title, black_price, red_price)

def mediaexpert(soup):
    title = soup.find_all('h1', class_='a-typo is-primary')
    red_price = soup.find_all('span', class_='a-price_price')[0]
    black_price = soup.find_all('span', class_='a-price_price')[2]

    for i in title:
        title = i.get_text()
        for i in title.split('\n')[0:2]:
            title = i

    for i in red_price:
        red_price = i

    for i in black_price:
        black_price = i

    if red_price == black_price:
        red_price = []

    promptcheck(title, black_price, red_price)

def findshop(scopes, URL):
    print(f'We found {scopes} in your {URL} so we think your shop is {scopes.upper()}')
    time.sleep(1)

# def coffeeproficiency(soup):
#     title = soup.find_all('h1', class_="product_title entry-title")
#     black_price = soup.find_all('span', class_="woocommerce-Price-amount amount")
#     for i in title:
#         title = i.get_text()
#     for i in black_price:
#         black_price = i.get_text()
#         black_price = black_price.split()[0]
#         black_price = float(black_price.replace(',','.'))
#     print(black_price)


def promptcheck(title, black_price, red_price): #4
    # global all_titles, all_black_prices, all_red_prices
    if black_price == []:
        black_price = actuall_price
        print(f'Actuall Price: {black_price}')
        print(f'Name of product: {title}')
        all_titles.append(title)
        all_black_prices.append(black_price)
        all_red_prices.append('NOT FOR SALE')
    if red_price == []:
        print(f'Actuall Price: {black_price}')
        print(f'Name of product: {title}')
        all_titles.append(title)
        all_black_prices.append(black_price)
        all_red_prices.append('NOT FOR SALE')
    else:
        print('THIS PRODUCT IS FOR SALE!')
        print(f'Name of product: {title}')
        print(f'Actuall Price: {black_price}')
        print(f'Current price: {red_price}')
        all_titles.append(title)
        all_black_prices.append(black_price)
        all_red_prices.append(red_price)


def show_df(username): #5
    for black,red,title in zip(all_black_prices, all_red_prices, all_titles):
        with open('products.csv', mode='a', encoding='utf-8') as prod_data:
            prod_writer = csv.writer(prod_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            prod_writer.writerow([username, title, black, red])
            prod_data.close()
    print(' ')
    print('product.csv file was succesfully updated with new data')

def showcsvforuser(namefor,username,email): #Func which show user`s URL with data
    dataformail = []
    datamessage = ''
    with open('products.csv', 'r', newline='',encoding='utf-8') as prod_data:
        reader = csv.reader(prod_data)
        for line in reader:
            if line != []:
                user, title, black, red = line
                user = int(user)
                username = int(username)
                if user == username:
                    print(line)
                    dataformail.append(line)
    dyw = input('Do you want to got email with your data?: ')
    if dyw == 'YES':
        time.sleep(0.35)
        password = input('Password: ')
        static_email = 'print.python.academy@gmail.com'
        message = f'Dear {namefor},\nBelow you can find data below to you\n{dataformail}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(static_email, password)
        server.sendmail(static_email, email, message)
        time.sleep(0.35)
        print(f'Message were sent from {static_email} to {email}')
    else:
        time.sleep(0.75)
        print('Thank you')
    exit()


def whileloopforlinks(username,email,namefor): #Function with input data for parsing. Takes URL and Username
    T = True
    i = 1
    print('Write >> STOP << to exit program!')

    while T == True: # Loop for adding URL
        URL = input(f'{i}: Paste your URL here: ')

        if URL != 'STOP': # Adding URL before STOP in prompt
            bf_pre_process(URL)
            i += 1

        if URL == 'STOP': # STOP loop for adding URL`S
            time.sleep(1.5)
            print('Thank you!')
            time.sleep(1.0)
            yesno = input('Do you want to see data? [YES/NO]: ')

            if yesno == 'YES':
                time.sleep(1.5)
                show_df(username) # Function which update CSV file
                time.sleep(1.5)
                showcsvforuser(namefor,username,email)
                T = False

            if yesno == 'NO':
                time.sleep(1.5)
                show_df(username) # Function which update CSV file
                T = False

def nextstep1():
    username = input('Write your name, if you need help write HELP: ')
    with open('users.csv', 'r', newline='',encoding='utf-8') as user_data:
        reader = csv.reader(user_data)
        for line in reader:
            if line != []:
                useR, Id, email = line
                USERS.append(useR)
                IDS.append(Id)
                EMAILS.append(email)
    ifuserexist(USERS,IDS,EMAILS,username)

def ifuserexist(USERS,IDS,EMAILS,username):
    if username == 'HELP':
        print('Thank for using HELP function :) Below you can find all users existing in our DataBase\n')
        time.sleep(1.0)
        print(f'{USERS}\nPlease select one of this user below\nIf you don`t find your username type NEWUSER in chat\n')
        time.sleep(1.0)
        username = input('Write your name, if you need help write HELP: ')
        if username in USERS:
             userid = USERS.index(username)
             namefor = username
             username = IDS[userid]
             email = EMAILS[userid]
             decision = input("If you want to add new data write NEW, if you want to see existing data write DATA: ")
             if decision == 'NEW':
                 whileloopforlinks(username,email,namefor)
             if decision == 'DATA':
                 showcsvforuser(namefor,username,email)
    if username in USERS:
        userid = USERS.index(username)
        print('Your username in users\n')
        namefor = username
        username = IDS[userid]
        email = EMAILS[userid]
        print(username)
        decision = input("If you want to add new data write NEW, if you want to see existing data write DATA: ")
        if decision == 'NEW':
            whileloopforlinks(username,email,namefor)
        if decision == 'DATA':
            showcsvforuser(namefor,username,email)

    if username not in USERS or username == 'NEWUSER':
        username = input('Write new username there: ')
        namefor = username
        specialID = random.randint(1, 999999999)
        email = input('Write your email here: ')
        with open('users.csv', mode='a', encoding='utf-8') as user_data:
            user_writer = csv.writer(user_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            user_writer.writerow([username, specialID, email])
            user_data.close()
        print(' ')
        print(f'users.csv file was succesfully updated with new data with |{username}|\nNick with special ID |{specialID}|')
        decision = input("If you want to add new data write NEW, if you want to see existing data write DATA: ")
        username = specialID
        if decision == 'NEW':
            whileloopforlinks(username,email,namefor)
        if decision == 'DATA':
            showcsvforuser(namefor,username,email)



nextstep1()
