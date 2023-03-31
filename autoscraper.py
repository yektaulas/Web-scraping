import os

import requests
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator(service_urls=['translate.googleapis.com'])
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/75.0.3770.80 Safari/537.36'}
URL = 'https://www.classcentral.com/'
httpx = requests.get(URL, headers=headers)
soup = BeautifulSoup(httpx.content, 'html.parser')


html_files = []


def simple_tag_iterator(single_page):
    for tag in soup.find_all(
            ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'button', 'a', 'strong',
             'label']):  # Mention HTML tag names here.
        if tag.string is not None:
            translated_text = translator.translate(tag.string.text, dest='hindi').text
            tag.string.string.replace_with(translated_text)
        else:
            try:
                for i in tag.strings:
                    if len(i) > 1:
                        translated_text = translator.translate(i.text, dest='hindi').text
                        i.string.replace_with(translated_text)
                    else:
                        continue
            except:
                pass
    custom_tags_iterator()
    with open(single_page, "w",
              encoding='utf-8') as file:
        file.write(str(soup.prettify()))


def custom_tags_iterator():
    try:
        page_content = soup.find('input', attrs={'type': 'search'})
        translated_text = translator.translate(page_content['placeholder'], dest='hindi').text
        page_content['placeholder'] = translated_text
        custom_p_tags = soup.find_all('p')
        for p in custom_p_tags:
            if p.strong is not None:
                p.strong.decompose()
                for p_string in p:
                    translated_text = translator.translate(p_string.text, dest='hindi').text
                    p_string.string.replace_with(translated_text)
            elif p.a is not None:
                p.a.decompose()
                for p_string in p:
                    translated_text = translator.translate(p_string.text, dest='hindi').text
                    p_string.string.replace_with(translated_text)
    except:
        pass


for single_page in html_files:
    offline_website = open(single_page, "r")
    soup = BeautifulSoup(offline_website, 'html.parser')
    simple_tag_iterator(single_page)

