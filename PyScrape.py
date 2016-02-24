from lxml import etree
from lxml import html
from collections import Counter
import requests
import random

directions = ["F", "U", "D", "B"]
jabs = ["Jab " + str(num) for num in range(1,4)] + ["Jab", "Rapid Jab", "Rapid Jab Finisher"]
tilts = [direction + "tilt" for direction in directions[:-1]]
smashes = [direction + "smash" for direction in directions[:-1]]
ground_moves = jabs + tilts + smashes
aerials = [direction + "air" for direction in directions] + ["Nair"]

attacks = ground_moves + aerials + ["Dash Attack"]

grabs = ["Grab", "Standing Grab", "Dash Grab", "Pivot Grab"]
throws = [direction + "throw" for direction in directions]
dodges = ["Spotdodge", "Forward Roll", "Back Roll", "Airdodge"]

all_moves = attacks + grabs + throws + dodges
print attacks

#TODO: They spelled "dependent" wrong on Kirby's page.

class GroundMove:
    def __init__(self, name, hitbox, faf, base_dmg, angle, bkb_wbkb, kbg):
        self.name = name
        self.hitbox = hitbox
        self.faf = faf
        self.base_dmg = base_dmg
        self.angle = angle
        self.bkb_wbkb = bkb_wbkb
        self.kbg = kbg

class Aerial:
    def __init__(self, name, hitbox, faf, base_dmg, angle, bkb_wbkb, kbg, landing_lag, autocancel):
        self.name = name
        self.hitbox = hitbox
        self.faf = faf
        self.base_dmg = base_dmg
        self.angle = angle
        self.bkb_wbkb = bkb_wbkb
        self.kbg = kbg
        self.landing_lag = landing_lag
        self.autocancel = autocancel

class Grab:
    def __init__(self, name, hitbox, faf):
        self.name = name
        self.hitbox = hitbox
        self.faf = faf

class Throw:
    def __init__(self, name, weight, base_dmg, angle, bkb, kbg):
        self.name = name
        self.weight = weight
        self.base_dmg = base_dmg
        self.angle = angle
        self.bkb = bkb
        self.kbg = kbg

class Dodge:
    def __init__(self, name, intangibility, faf, notes = "-"):
        self.name = name
        self.intangibility = intangibility
        self.faf = faf
        self.notes = notes

class Moveset:
    def __init__(self, character_name):
        self.character_name = character_name
        self.jabs = []
        self.dash_attacks = []
        self.tilts = []
        self.smashes = []
        self.aerials = []
        self.grabs = []
        self.throws = []
        self.dodges = []
        
    def addMove(self, move):
        if moveType(move) == "GroundMove":
            if "Jab" in move.name: self.jabs.append(move)
            elif "Dash" in move.name: self.dash_attacks.append(move)
            elif "tilt" in move.name: self.tilts.append(move)
            elif "smash" in move.name: self.smashes.append(move)
            else: print "ERROR!!! invalid ground move"
        elif moveType(move) == "Aerial": self.aerials.append(move)
        elif moveType(move) == "Grab": self.grabs.append(move)
        elif moveType(move) == "Throw": self.throws.append(move)
        elif moveType(move) == "Dodge": self.dodges.append(move)
        elif moveType(move) == "list": print "ignoring empty data..."
        else: print "ERROR!!! invalid move"
            
def moveType(move_instance):
    return move_instance.__class__.__name__

def get_pages():
    page = requests.get('http://kuroganehammer.com/Smash4/')
    root = html.fromstring(page.content)
    html_scrape = etree.HTML(page.content)
    result = etree.tostring(html_scrape, pretty_print=True, method="html")
    stuff = root.xpath('//a')
    characters = [element.attrib['alt'] for element in root.xpath('//img')][1:-1]
    characters.remove("Mii Fighters")
    #TODO: Something about Mii fighter
    pages = ['http://kuroganehammer.com' + element.attrib['href'] for element in root.xpath('//tbody//td//a') if element.attrib['href'] != '/Smash4/Mii']
    #print characters
    #print pages
    #print result
    return characters, pages

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
    terms_to_remove = ["Statistic", "Value/Rank", "Attacks",
              'Hitbox Active', 'FAF', 'Angle',
              'BKB/WBKB', 'KBG', 'BKB', 'Base Dmg.',
              'Miscellaneous', 'Intangibility', 'Notes',
              'Landing Lag', 'Autocancel', 'Grabs', 'Throws',
              'Weight Dependent?', 'Weight Dependant?', 'Base Dmg. (+SD)']
    moveset = []
    counter_to_special_moves = 0
    for move in moves:
        if move not in terms_to_remove:
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

def isMove(datum):
    for move in all_moves:
        if move in datum and datum[0].isdigit() is False: return True
    print datum
    return False

def isDodge(datum):
    if datum in dodges: return True
    else: return False

def isGrab(datum):
    if datum in grabs: return True
    else: return False
    
def parse_frame_data(character_name, frame_data):
    move_data = []
    move_name = ""
    allMoves = Moveset(character_name)
    for datum in frame_data:
        if isMove(datum):
            newMove = []
            data_len = len(move_data)
            if data_len == 0: print "Starting data parsing..."
            elif data_len == 3 and isGrab(move_name): newMove = Grab(*move_data)
            elif (data_len == 3 and isDodge(move_name)) or data_len == 4: newMove = Dodge(*move_data)
            elif data_len == 6: newMove = Throw(*move_data)
            elif data_len == 7: newMove = GroundMove(*move_data)
            elif data_len == 9: newMove = Aerial(*move_data)
            else:
                print "ERROR!!!! invalid amount of frame data for move. counted", data_len, "data strings!"
                return allMoves
            allMoves.addMove(newMove)
            print "Added " + "nothing" if data_len == 0 else move_data[0] + ", now parsing", datum
            move_name = datum
            move_data = [datum]
        else:
            move_data.append(datum)
    return allMoves

def trim_frame_data(raw_frame_data):
    new_frame_data = []
    stripped_data = []
    clean_stripped_data = []
    for data in raw_frame_data:
        new_data = [item.strip() for item in data.split('\r\n')]
        stripped_data += new_data
    print "PRINTING STRIPPED DATA..."
    print stripped_data
    print "\n\n\n"
    replace_empty = False
    rapid_jab_data_counter = 0
    for datum in stripped_data:
        if "Rapid Jab" in datum:
            replace_empty = True
            rapid_jab_data_counter = 0
        elif isMove(datum):
            replace_empty = False
        elif replace_empty:
            rapid_jab_data_counter += 1
            if rapid_jab_data_counter > 6:
                replace_empty = False
        clean_stripped_data.append("?" if replace_empty and datum == "" else datum)
    new_frame_data = filter(None, clean_stripped_data)
    print "PRINTING CLEAN STRIPPED DATA..."
    print new_frame_data
    print "\n\n\n"
    
    return get_moveset(new_frame_data)

characters, pages = get_pages()
page = random.choice(pages)
character = characters[pages.index(page)]
moveset, frame_data = get_frame_data(page)
parsed_moveset = parse_frame_data(character, frame_data)
