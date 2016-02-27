from lxml import etree
from lxml import html
from collections import Counter
import requests
import random
DEBUG = False

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
all_groundmove_types = ["Jab", "Attack", "tilt", "smash"]
all_move_types = ["Jab", "tilt", "smash", "air", "Attack", "Dash", "Rapid", "Grab", "throw", "dodge", "Roll"]
if DEBUG: print attacks

#TODO: They spelled "dependent" wrong on Kirby's page.

#Simple class structures for storing frame data for moves
class GroundMove:
    def __init__(self, name, hitbox, faf, base_dmg, angle, bkb_wbkb, kbg):
        self.name = name
        self.hitbox = hitbox
        self.faf = faf
        self.base_dmg = base_dmg
        self.angle = angle
        self.bkb_wbkb = bkb_wbkb
        self.kbg = kbg

    def __str__(self):
        return  "      " + self.name + \
                "\n         Hitbox: " + self.hitbox + \
                "\n         FAF: " + self.faf + \
                "\n         Base Damage: " + self.base_dmg + \
                "\n         Angle: " + self.angle + \
                "\n         BKB/WBKB: " + self.bkb_wbkb + \
                "\n         KBG: " + self.kbg + \
                "\n\n"        

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

    def __str__(self):
        return  "      " + self.name + \
                "\n         Hitbox: " + self.hitbox + \
                "\n         FAF: " + self.faf + \
                "\n         Base Damage: " + self.base_dmg + \
                "\n         Angle: " + self.angle + \
                "\n         BKB/WBKB: " + self.bkb_wbkb + \
                "\n         KBG: " + self.kbg + \
                "\n         Landing Lag: " + self.landing_lag + \
                "\n         Autocancel: " + self.autocancel + \
                "\n\n"        

class Grab:
    def __init__(self, name, hitbox, faf):
        self.name = name
        self.hitbox = hitbox
        self.faf = faf

    def __str__(self):
        return  "      " + self.name + \
                "\n         Hitbox: " + self.hitbox + \
                "\n         FAF: " + self.faf + \
                "\n\n"

class Throw:
    def __init__(self, name, weight, base_dmg, angle, bkb, kbg):
        self.name = name
        self.weight = weight
        self.base_dmg = base_dmg
        self.angle = angle
        self.bkb = bkb
        self.kbg = kbg
        
    def __str__(self):
        return  "      " + self.name + \
                "\n         Weight Dependent?: " + self.weight + \
                "\n         Base Damage: " + self.base_dmg + \
                "\n         Angle: " + self.angle + \
                "\n         BKB: " + self.bkb + \
                "\n         KBG: " + self.kbg + \
                "\n\n"

class Dodge:
    def __init__(self, name, intangibility, faf, notes = "-"):
        self.name = name
        self.intangibility = intangibility
        self.faf = faf
        self.notes = notes

    def __str__(self):
        return  "      " + self.name + \
                "\n         Intangibility: " + self.intangibility + \
                "\n         FAF: " + self.faf + \
                "\n         Notes: " + self.notes + \
                "\n\n"

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

    def __str__(self):
        moveset_str = self.character_name + ":\n"
        
        moveset_str += "   Jabs:\n"
        for move in self.jabs:
            moveset_str += str(move)

        moveset_str += "   Dash Attack(s):\n"
        for move in self.dash_attacks:
            moveset_str += str(move)

        moveset_str += "   Tilt Attacks:\n"
        for move in self.tilts:
            moveset_str += str(move)

        moveset_str += "   Smash Attacks:\n"
        for move in self.smashes:
            moveset_str += str(move)

        moveset_str += "   Aerial Attacks:\n"
        for move in self.aerials:
            moveset_str += str(move)

        moveset_str += "   Grabs:\n"
        for move in self.grabs:
            moveset_str += str(move)

        moveset_str += "   Throws:\n"
        for move in self.throws:
            moveset_str += str(move)

        moveset_str += "   Dodges:\n"
        for move in self.dodges:
            moveset_str += str(move)
          
        return moveset_str
        
    def addMove(self, move):
        if className(move) == "GroundMove":
            if "Jab" in move.name: self.jabs.append(move)
            elif "Dash" in move.name: self.dash_attacks.append(move)
            elif "tilt" in move.name: self.tilts.append(move)
            elif "smash" in move.name: self.smashes.append(move)
            else: raise ValueError("ERROR!!! invalid ground move")
        elif className(move) == "Aerial": self.aerials.append(move)
        elif className(move) == "Grab": self.grabs.append(move)
        elif className(move) == "Throw": self.throws.append(move)
        elif className(move) == "Dodge": self.dodges.append(move)
        elif className(move) == "list":
            if DEBUG: print "ignoring empty data..."
        else: raise ValueError("ERROR!!! invalid move")


def className(instance):
    ''' Returns class name of object as string'''
    return instance.__class__.__name__

def get_pages():
    main_page = requests.get('http://kuroganehammer.com/Smash4/')
    root = html.fromstring(main_page.content)
    #code for pretty printing
    #html_scrape = etree.HTML(main_page.content)
    #result = etree.tostring(html_scrape, pretty_print=True, method="html")
    characters = [element.attrib['alt'] for element in root.xpath('//img')][1:-1]
    characters.remove("Mii Fighters")
    pages = ['http://kuroganehammer.com' + element.attrib['href'] for element in root.xpath('//tbody//td//a')]
    pages.remove('http://kuroganehammer.com/Smash4/Mii')

    #Current solution for Mii Fighter page redirect, may need to be changed if Mii fighter page changes
    mii_page = requests.get('http://kuroganehammer.com/Smash4/Mii')
    mii_root = html.fromstring(mii_page.content)
    mii_characters = [element.text_content() for element in mii_root.xpath('//a') if "Mii" in element.text_content()]
    mii_pages = ['http://kuroganehammer.com' + element.attrib['href'] for element in root.xpath('//h1//a')]

    characters += mii_characters
    pages += mii_pages
    #print characters
    #print pages
    #print result
    return characters, pages

def get_frame_data(url):
    '''Takes a given character URL with frame data, and returns
        moveset and frame data as arrays of strings'''
    page = requests.get(url)
    root = html.fromstring(page.content)
    frame_data = root.xpath('//table[@id != "AutoNumber3"]')[1:]
    #frame_data = frame_data.xpath('//<table[@width() > 600]')
    frame_data = [element.text_content() for element in frame_data]
    clean_frame_data = trim_frame_data(frame_data)
    moveset = root.xpath('//th')
    moveset = [element.text_content() for element in moveset]
    if DEBUG:
        for x in frame_data: print x
    #clean_movset = [k for k,v in Counter(moveset).items() if v==1]
    clean_moveset = get_moveset(moveset)
    return clean_moveset, clean_frame_data
    #for x in moveset: print x
    #for x in clean_moveset: print x

def get_moveset(moves):
    '''Used for stripping non-move words from scraped page'''
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
            moveset += [move.encode('utf-8')]
            
        # "Attacks" starts off 3 tables, the 3rd of which is
        # Special Moves...which we don't want.
        if move == 'Attacks':
            counter_to_special_moves += 1
        if counter_to_special_moves == 3:
        #Return once we're at the special moves section
            return moveset
    #print "Shouldn't reach here..."
    return moveset

def isMove(datum):
    for move in all_move_types:
        if move in datum and datum[0].isdigit() is False: return True
    if DEBUG: print datum
    return False

def isDodge(datum):
    #if datum in dodges: return True
    if "dodge" in datum or "Roll" in datum: return True
    else: return False

def isGrab(datum):
    #if datum in grabs: return True
    if "Grab" in datum: return True
    else: return False

def isThrow(datum):
    if "throw" in datum: return True
    else: return False
    
def isGroundMove(datum):
    for move in all_groundmove_types:
        if move in datum: return True
    return False

def isAerial(datum):
    if "air" in datum: return True
    else: return False
    
def parse_frame_data(character_name, frame_data):
    '''Goes through an clean array of frame data strings and parses it
        into objects for the respective move type, and pushes them to
        a Moveset object. Returns the final Moveset object'''
    move_data = []
    move_name = ""
    
    #Create a moveset object for the given character
    allMoves = Moveset(character_name) 
    for datum in frame_data:
        #Iterate through frame data, and once a move name has been found,
        # starts collecting the following data until
        # another move name has been found. The collected move data
        # is then put into an appropriate Move object, based on
        # amount of data collected and a check of the move name
        if isMove(datum):
            newMove = []
            data_len = len(move_data)
            if data_len == 0: print "Starting data parsing..."
            elif data_len == 3 and isGrab(move_name): newMove = Grab(*move_data)
            elif (data_len == 3 and isDodge(move_name)) or data_len == 4: newMove = Dodge(*move_data)
            elif data_len == 6 and isThrow(move_name): newMove = Throw(*move_data)
            elif data_len == 7 and isGroundMove(move_name): newMove = GroundMove(*move_data)
            elif data_len == 9 and isAerial(move_name): newMove = Aerial(*move_data)
            else:
                raise ValueError("ERROR!!!! invalid amount of frame data for " +
                                 move_name +
                                 ". counted " +
                                 str(data_len) +
                                 " data strings!")
                return allMoves
            allMoves.addMove(newMove)
            if DEBUG: print "Added " + "nothing" if data_len == 0 else move_name + ", now parsing", datum
            move_name = datum
            move_data = [datum]
        else:
            move_data.append(datum)
    return allMoves

def trim_frame_data(raw_frame_data):
    '''Takes scraped HTML page and cuts out all empty strings.
        Also replaces the unfortunate blank spaces in some pages'
        Rapid Jab frame data with question marks'''
    new_frame_data = []
    stripped_data = []
    clean_stripped_data = []
    for data in raw_frame_data:
        #split data by newlines, and strip html tags
        new_data = [item.strip() for item in data.split('\r\n')]
        stripped_data += new_data
    if DEBUG:
        print "PRINTING STRIPPED DATA..."
        print stripped_data
        print "\n\n\n"
    #The following for loop is for replacing the
    # empty frame data for some characters' Rapid Jabs or Dash attacks
    # with '?', so that the amount of data per attack (6 strings)
    # stays consistent
    replace_empty = False
    frame_data_counter = 0
    for datum in stripped_data:
        if isGroundMove(datum):
            replace_empty = True
            frame_data_counter = 0
        elif isMove(datum):
            replace_empty = False
        elif replace_empty:
            frame_data_counter += 1
            if frame_data_counter > 6:
                replace_empty = False
        clean_stripped_data.append("?" if replace_empty and datum == "" else datum)
    new_frame_data = filter(None, clean_stripped_data) #Remove all empty strings
    if DEBUG:
        print "PRINTING CLEAN STRIPPED DATA..."
        print new_frame_data
        print "\n\n\n"
    
    return get_moveset(new_frame_data)

characters, pages = get_pages()
page = random.choice(pages)
character = characters[pages.index(page)]
moveset, frame_data = get_frame_data(page)
parsed_moveset = parse_frame_data(character, frame_data)
