from lxml import etree
from lxml import html
from collections import Counter
import requests
import random


def get_pages():
    page = requests.get('http://kuroganehammer.com/Smash4/')
    root = html.fromstring(page.content)
    html_scrape = etree.HTML(page.content)
    result = etree.tostring(html_scrape, pretty_print=True, method="html")
    stuff = root.xpath('//a')
    characters = [element.attrib['alt'] for element in root.xpath('//img')][1:-1]
    pages = ['http://kuroganehammer.com' + element.attrib['href'] for element in root.xpath('//tbody//td//a')]
    #print characters
    #print pages
    #print result
    return pages

def get_frame_data(url):
    page = requests.get(url)
    root = html.fromstring(page.content)
    frame_data = root.xpath('//table[@id != "AutoNumber3"]')[1:]
    #frame_data = frame_data.xpath('//<table[@width() > 600]')
    frame_data = [element.text_content() for element in frame_data]
    moveset = root.xpath('//th')
    moveset = [element.text_content() for element in moveset]
    clean_moveset = [k for k,v in Counter(moveset).items() if v==1]
    for x in frame_data: print x
    #for x in moveset: print x
    #for x in clean_moveset: print x

pages = get_pages()
character = random.choice(pages)
get_frame_data(character)
