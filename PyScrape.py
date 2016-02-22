from lxml import etree
from lxml import html
from collections import Counter
import requests
import random

directions = ["F", "U", "D", "B"]
tilts = [direction + "tilt" for direction in directions[:-1]]
aerials = [direction + "air" for direction in directions]
smashes = [direction + "smash" for direction in directions[:-1]]
jabs = ["Jab " + str(num) for num in range(1,4)] + ["Rapid Jab", "Rapid Jab Finisher"]

attacks = tilts + aerials + smashes + jabs
print attacks

def get_pages():
    page = requests.get('http://kuroganehammer.com/Smash4/')
    root = html.fromstring(page.content)
    html_scrape = etree.HTML(page.content)
    result = etree.tostring(html_scrape, pretty_print=True, method="html")
    stuff = root.xpath('//a')
    characters = [element.attrib['alt'] for element in root.xpath('//img')][1:-1]
    #TODO: Something about Mii fighter
    pages = ['http://kuroganehammer.com' + element.attrib['href'] for element in root.xpath('//tbody//td//a') if element.attrib['href'] != '/Smash4/Mii']
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
    clean_frame_data = trim_frame_data(frame_data)
    moveset = root.xpath('//th')
    moveset = [element.text_content() for element in moveset]
    for x in frame_data: print x
    #clean_movset = [k for k,v in Counter(moveset).items() if v==1]
    clean_moveset = get_moveset(moveset)
    return clean_moveset, clean_frame_data
    #for x in moveset: print x
    #for x in clean_moveset: print x

def get_moveset(moves):
    remove = ["Statistic", "Value/Rank", "Attacks",
              'Hitbox Active', 'FAF', 'Angle',
              'BKB/WBKB', 'KBG', 'BKB', 'Base Dmg.',
              'Miscellaneous', 'Intangibility', 'Notes',
              'Landing Lag', 'Autocancel', 'Grabs', 'Throws',
              'Weight Dependent?', 'Base Dmg. (+SD)']
    moveset = []
    counter_to_special_moves = 0
    for move in moves:
        if move not in remove:
            moveset += [move]
            
        # "Attacks" starts off 3 tables, the 3rd of which is
        # Special Moves...which we don't want.
        if move == 'Attacks':
            counter_to_special_moves += 1
        if counter_to_special_moves == 3:
        #Return once we're at the special moves section
            return moveset
    print "Shouldn't reach here..."
    return moveset

def trim_frame_data(raw_frame_data):
    new_frame_data = []
    for data in raw_frame_data:
        new_data = filter(None, [item.strip() for item in data.split('\r\n')])
        new_frame_data += new_data
    return new_frame_data
    
pages = get_pages()
character = random.choice(pages)
moveset, frame_data = get_frame_data(character)
