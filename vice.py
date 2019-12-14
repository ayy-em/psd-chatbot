from bs4 import BeautifulSoup
import requests
import datetime
import lxml


def get_caption_and_image():
    # New topic every day
    what_list = ['tech', 'music', 'food', 'drugs', 'entertainment', 'health', 'news']
    number = datetime.date.today().weekday()
    what = what_list[number]
    # gets a list from scraping from a function below
    list_vice = get_vice_theme(what)
    # Tear the list apart to compile string once again & get an image
    vice_final_img_url = list_vice[4]
    vice_final_content_string = '*' + list_vice[0] + '* \n\n' + list_vice[1] + '\n[Read the article by ' + list_vice[2] + 'here.](' + list_vice[3] + ')'
    list_to_return_to_main = [vice_final_content_string, vice_final_img_url]
    # returns a list(caption_string, image_url_to_post)
    return list_to_return_to_main


def get_vice_theme(theme):
    print('Trying to post vice ' + theme)
    # I know this part is horrible, but fuck it
    # could just append theme to url, make a dict, yea yeah
    if theme == 'tech':
        page = requests.get('https://www.vice.com/en_us/section/tech')
        vice_emoji = '💻'
    elif theme == 'music':
        page = requests.get('https://www.vice.com/en_us/section/music')
        vice_emoji = '🎵'
    elif theme == 'food':
        page = requests.get('https://www.vice.com/en_us/section/food')
        vice_emoji = '🥐'
    elif theme == 'drugs':
        page = requests.get('https://www.vice.com/en_us/section/drugs')
        vice_emoji = '💊'
    elif theme == 'entertainment':
        page = requests.get('https://www.vice.com/en_us/section/entertainment')
        vice_emoji = '💃'
    elif theme == 'health':
        page = requests.get('https://www.vice.com/en_us/section/health')
        vice_emoji = '🏥'
    elif theme == 'news':
        page = requests.get('https://www.vice.com/en_us/section/news')
        vice_emoji  = '📰'
    # Start scraping: soup -> navigate thru page, find what we need, blah blah
    soup = BeautifulSoup(page.content, 'lxml')
    tech_main = soup.find('div', class_='sections-lede__head')
    sect = tech_main.section
    div_title = sect.find('div', class_='sections-card__content').div.div
    by_desc = div_title.find_all('p')
    vice_tech_url = sect.find('source')['srcset']
    vice_tech_url_index = vice_tech_url.find('?')
    vice_tech_final_title = sect.find('div', class_='sections-card__content').div.div.div.text
    vice_tech_final_desc = by_desc[0].text + '\n\nPublished in #' + theme.title() + ' ' + vice_emoji
    vice_tech_final_author = div_title.find('span').text
    vice_tech_final_img_url = vice_tech_url[:vice_tech_url_index]
    article_base_url = 'https://vice.com'
    article_url = div_title.find('a')['href']
    vice_tech_final_article_url = article_base_url + article_url
    # returns exactly what it says, 5 items
    return vice_tech_final_title, vice_tech_final_desc, vice_tech_final_author, vice_tech_final_article_url, vice_tech_final_img_url
