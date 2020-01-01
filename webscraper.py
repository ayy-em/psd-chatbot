import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import date, datetime


# entry from main for a daily msg to group chat
def get_daily_psdlk_msg():
    w_text = get_weather_for_posidelki()
    f_text = get_football_for_posidelki()
    n_text = get_news_ru()
    cs_text = w_text + f_text + n_text
    return cs_text


# returns weather string for psdlk
def get_weather_for_posidelki():
    # returns weather string
    dtnow = datetime.now()
    str_todayy = str(dtnow.day) + '/' + str(dtnow.month) + '/' + str(dtnow.year)
    ult_fin_hi = '\nСегодня ' + str_todayy + ' и мы в новом десятилетии.'
    # returns a big string
    megaweatherstring = 'Утро доброе.' + ult_fin_hi + '\n\n\t*Погода:*\n' +  get_weather_city('Moscow', 'RU') + get_weather_city('Amsterdam', 'RU') + get_weather_city('Sochi', 'RU') + '\n'
    return megaweatherstring


# given a city and a language to return a string in, does it
def get_weather_city(city, language):
    if city == 'Moscow':
        city_str = '*Москва*'
        city_url = 'https://yandex.ru/pogoda/moscow'
    elif city == 'Amsterdam':
        city_str = '*Амстердам*'
        city_url = 'https://yandex.ru/pogoda/amsterdam'
    elif city == 'Sochi':
        city_str = '*Сочи*'
        city_url = 'https://yandex.ru/pogoda/sochi'
    # scrape that shit from yandex weather
    page = requests.get(city_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    div_days = soup.find_all('div', class_='swiper-wrapper')[1]
    div_temp = div_days.find(text=re.compile('Сегодня'))
    div_today = div_temp.parent.parent
    div_c = list(div_today.children)
    dnem = div_c[3]
    nochu = div_c[4]
    dojd_ili_net = div_c[5].text
    dnem_list = list(dnem.children)
    nochu_list = list(nochu.children)
    nochu_string = nochu_list[1].text + nochu_list[2].text
    dnem_string = dnem_list[1].text + dnem_list[2].text
    # dictionaries used for emoji
    oblaka = ['Малооблачно', 'Облачно с прояснениями']
    sunshine = ['Ясно']
    pasmurno = ['Пасмурно']
    dojd = ['Дождь', 'Небольшой дождь']
    snow = ['Снегопад', 'Снег', 'Небольшой снег']
    if dojd_ili_net in oblaka:
        emoji = '⛅'
    elif dojd_ili_net in sunshine:
        emoji = '🌝'
    elif dojd_ili_net in pasmurno:
        emoji = '🌥'
    elif dojd_ili_net in dojd:
        emoji = '🌧'
    elif dojd_ili_net in snow:
        emoji = '❄️'
    else:
        emoji = '🌡️'
    ult_text = '\t\t' + city_str + ': ' + emoji + ' ' + dojd_ili_net + ', ' + dnem_string + ', ночью: ' + nochu_string + '.\n'
    # but if the language is english, then its from bot, then another string
    if language == 'EN':
        ult_text = get_weather_en(city)
    # returns a string
    return ult_text


# invoked by get_weather_city(city, 'EN')
def get_weather_en(city_to_look_up):
    # get weather token from os env
    weather_token = os.environ["WEATHERBIT_API_KEY"]
    r = requests.get("https://api.weatherbit.io/v2.0/current?city=" + str(city_to_look_up) + "&key=" + str(weather_token))
    # turn the thing into a json and compile a megastring
    json_weather = r.json()
    text_part_reply_one = "It is "
    text_part_reply_two = " C in " + str(city_to_look_up) + " now with "
    text_part_reply_two_two = ".\n\tSunrise today: "
    text_part_reply_three = "\n\tSunset today: "
    text_part_reply_four = "\n\tPrecipitation rate (mm/hr): "
    temp_c = json_weather["data"][0]["temp"]
    desc = json_weather["data"][0]["weather"]["description"]
    sunrise = json_weather["data"][0]["sunrise"]
    sunset = json_weather["data"][0]["sunset"]
    precipitation = json_weather["data"][0]["precip"]
    # create a megastring and return it
    weather_reply = text_part_reply_one + str(temp_c) + text_part_reply_two + str(desc).lower() + text_part_reply_two_two + sunrise + text_part_reply_three + sunset + text_part_reply_four + str(precipitation)
    return weather_reply


def get_football_for_posidelki():
    megafootballstring = '*Футбол:*\n\t\t' + get_football_team('Spartak') + '\n\t\t' + get_football_team('Zenit')
    return megafootballstring


def get_football_team(team):
    # gets the team's name, returns string with next game
    if team == 'Spartak':
        team_url = 'https://www.sports.ru/spartak/'
        emoji_ftbl = '🐷 '
    elif team == 'Zenit':
        team_url = 'https://www.sports.ru/zenit/'
        emoji_ftbl = '💰 '
    page_f = requests.get(team_url)
    # here comes the scraping
    soup = BeautifulSoup(page_f.content, 'html.parser')
    main_lo = soup.find_all('div', class_='pageLayout')[0]
    scores = main_lo.find_all('div', class_='scores')[0]
    next_game_list = list(scores.children)
    so_game_tag = next_game_list[3]
    game_start = so_game_tag.find_all('meta')[0]
    gd = str(game_start)[20:25].replace('-', '.')
    gd_1 = gd[3:] + '.' + gd[:2]
    gs = str(game_start)[26:31]
    opponents = so_game_tag.find_all('meta')[1]
    opp_indx = str(opponents).find('"') + 1
    opp_indx_temp = opp_indx + 1
    opp_indx2 = str(opponents)[opp_indx_temp:].find('"') + opp_indx + 1
    opz = str(opponents)
    opp = opz[opp_indx:opp_indx2]
    # compile a reply string
    ult_football_text = emoji_ftbl + opp + ' @ ' + gd_1 + ' в ' + gs
    return ult_football_text


def get_news_ru():
    # told to get news, returns a mega-string called ult_news
    # first - rbc line
    url = 'https://www.rbc.ru/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tag_main_news = soup.find('a', class_="main__big__link js-yandex-counter")
    news_text = tag_main_news.text.rstrip().lstrip()
    news_link = tag_main_news['href']
    ult_news1 = '\t\t📰 ' + news_text + '. [- читать.](' + news_link + ')'
    # then football
    url2 = 'https://bombardir.ru/'
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    tag_main_news2 = soup2.find('div', class_='soc-block-f')
    news_list = list(tag_main_news2.find_all('span', class_='soc-text'))
    bbd_1 = news_list[0].text.strip()
    url_base = 'https://bombardir.ru/'
    bbd_1_a = url_base + news_list[0].a['href'].strip()
    ult_news2 = '\t\t⚽ ' + bbd_1 + ' [ - читать.](' + bbd_1_a + ')'
    # and lastly, news
    url3 = 'https://yandex.ru/news/rubric/computers?from=index'
    page3 = requests.get(url3)
    soup3 = BeautifulSoup(page3.content, 'html.parser')
    tg_tech_news = soup3.find('h2', class_='story__title')
    ya_news = tg_tech_news.text.strip()
    ya_link = 'https://yandex.ru' + tg_tech_news.a['href'].strip()
    ult_news3 = '\t\t🖥️ ' + ya_news + '[ - читать.](' + ya_link + ')'
    # compile a news string using rbc, bbd and yandex tech and return it
    ult_news = '\n\n*Новости:* \n' + ult_news1 + '\n' + ult_news2 + '\n' + ult_news3
    return ult_news
