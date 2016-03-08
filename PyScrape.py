from lxml import etree
from lxml import html
#import FrameDataGUI
import requests
DEBUG = False
DOWNLOAD = False
OFFLINE_MODE = True
characters = []
pages = []

moveset_arrays = ["Jabs", "Dash Attacks", "Tilts", "Smashes", "Aerials",
                  "Grabs", "Throws", "Dodges"]
all_groundmove_types = ["Jab", "Attack", "tilt", "smash"]
all_move_types = ["Jab", "tilt", "smash", "air", "Attack", "Dash", "Rapid", "Grab", "throw", "dodge", "Roll"]

#TODO: They spelled "dependent" wrong on Kirby's page...

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

def scrapePage(character):
    ''' Returns the parsed moveset of a given character
        as a Moveset instance '''
    frame_data = get_frame_data(pages[characters.index(character)])
    parsed_moveset = parse_frame_data(character, frame_data)
    return parsed_moveset

def scrapeAllPages():
    ''' Returns the parsed movesets for all characters
        as a dictionary of Moveset instances '''
    all_movesets = {}
    for character in characters:
        char_scrape = scrapePage(character)
        all_movesets[character] = char_scrape
    return all_movesets
    
def get_pages():
    ''' Gets all character names and corresponding URLs from
        the KuroganeHammer Smash4 homepage, or from a text file
        if in offline mode '''
    print "RUNNING IN " + ("OFFLINE MODE" if OFFLINE_MODE else "ONLINE MODE")
    if OFFLINE_MODE:
        with open("characters.txt", 'r') as character_file:
            characters = [character.rstrip('\n') for character in character_file]

        with open("pages.txt", 'r') as page_file:
            pages = [page.rstrip('\n') for page in page_file]
    else:
        main_page = requests.get('http://kuroganehammer.com/Smash4/')
        root = html.fromstring(main_page.content)
        characters = [element.attrib['alt'] for element in root.xpath('//img')][1:-1]
        characters.remove("Mii Fighters")
        pages = ['http://kuroganehammer.com' + element.attrib['href'] for element in root.xpath('//tbody//td//a')]
        pages.remove('http://kuroganehammer.com/Smash4/Mii')

        #Current solution for Mii Fighter page redirect, may need to be changed if Mii fighter page changes
        mii_page = requests.get('http://kuroganehammer.com/Smash4/Mii')
        mii_root = html.fromstring(mii_page.content)
        mii_characters = [element.text_content() for element in mii_root.xpath('//a') if "Mii" in element.text_content()]
        mii_pages = ['http://kuroganehammer.com' + element.attrib['href'] for element in mii_root.xpath('//h1//a')]

        characters += mii_characters
        pages += mii_pages

        if DOWNLOAD:
            with open("characters.txt", 'w') as character_file:
                for character in characters: character_file.write(character + '\n')
                
            with open("pages.txt", 'w') as page_file:
                for page in pages: page_file.write(page + '\n')
                
    #print characters
    #print pages
    #print result
    return characters, pages

def get_frame_data(url):
    ''' Takes a given character's URL, and returns
        frame data as an array of strings
        (reads data from HTML text file dump if in offline mode) '''
    if OFFLINE_MODE:
        with open(characters[pages.index(url)] + ".txt", "r") as frame_data_file:
            html_string = frame_data_file.read()
        root = html.fromstring(html_string)
    else:
        page = requests.get(url)
        root = html.fromstring(page.content)
        if DOWNLOAD:
            html_scrape = etree.HTML(page.content)
            html_string = etree.tostring(html_scrape, pretty_print=True, method="html")
            with open(characters[pages.index(url)] + ".txt", "w") as frame_data_file:
                frame_data_file.write(html_string)

    # XPath to get all move names and data entries in tables from
    # 2nd and 3rd tables; ignores the statistic table and special moves table
    frame_data = root.xpath('//table[position()=2 or position()=3]//th | ' +
                            '//table[position()=2 or position()=3]//td')
    frame_data = [element.text_content() for element in frame_data]
    clean_frame_data = trim_frame_data(frame_data)
    if DEBUG:
        for x in frame_data: print x
    #moveset = root.xpath('//table[position()=2 or position()=3]//th')
    #return moveset, clean_frame_data
    return clean_frame_data

def isMove(datum):
    for move in all_move_types:
        if move in datum and datum[0].isdigit() is False: return True
    if DEBUG: print datum
    return False

def isDodge(datum):
    if "dodge" in datum or "Roll" in datum and datum[0].isdigit() is False: return True
    else: return False

def isGrab(datum):
    if "Grab" in datum and datum[0].isdigit() is False: return True
    else: return False

def isThrow(datum):
    if "throw" in datum and datum[0].isdigit() is False: return True
    else: return False
    
def isGroundMove(datum):
    for move in all_groundmove_types:
        if move in datum and datum[0].isdigit() is False: return True
    return False

def isAerial(datum):
    if "air" in datum and datum[0].isdigit() is False: return True
    else: return False
    
def parse_frame_data(character_name, frame_data):
    '''Goes through a clean array of frame data strings and parses it
        into objects for the respective move type, and pushes them to
        a Moveset object. Returns the final Moveset object'''
    move_data = []
    move_name = ""
    
    #Create a moveset object for the given character
    allMoves = Moveset(character_name) 
    for datum in frame_data:
        # Iterates through frame data, and once a move name has been found,
        # starts collecting the following data until
        # another move name has been found. The collected move data
        # is then put into an appropriate Move object, based on
        # amount of data collected and a check of the move type
        if isMove(datum):
            newMove = []
            data_len = len(move_data)
            if data_len == 0: print "Starting data parsing for " + character_name + "..."
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
    ''' Takes scraped HTML page, strips non-move words from page,
        and cuts out empty strings.
        Also replaces the unfortunate blank spaces in some pages'
        frame data with question marks (blank spaces for data
        that appears to have not yet been discovered) '''
    new_frame_data = []
    stripped_data = []
    
    # Strip non-move words from scraped page
    terms_to_remove = ["Statistic", "Value/Rank", "Attacks",
              'Hitbox Active', 'FAF', 'Angle',
              'BKB/WBKB', 'KBG', 'BKB', 'Base Dmg.',
              'Miscellaneous', 'Intangibility', 'Notes',
              'Landing Lag', 'Autocancel', 'Grabs', 'Throws',
              'Weight Dependent?', 'Weight Dependant?', 'Base Dmg. (+SD)',
              'Useless Tractor Beams']
    new_frame_data = []
    for move in raw_frame_data:
        if move not in terms_to_remove: stripped_data += [move.encode('utf-8')]

    # The following for loop is for replacing the
    # empty frame data for some characters' attacks
    # with '?', so that the amount of data per attack (6 or 8 strings)
    # stays consistent
    replace_empty = False
    frame_data_counter = 0
    for datum in stripped_data:
        if isGroundMove(datum):
            replace_empty = True
            frame_data_counter = 6
        elif isAerial(datum):
            replace_empty = True
            frame_data_counter = 8
        elif isMove(datum):
            replace_empty = False
        elif replace_empty:
            frame_data_counter -= 1
            if frame_data_counter < 0:
                replace_empty = False
        new_frame_data.append("?" if replace_empty and datum == "" else datum)
    new_frame_data = filter(None, new_frame_data) #Remove all remaining empty strings
    if DEBUG:
        print "PRINTING CLEAN STRIPPED DATA..."
        print new_frame_data
        print "\n\n\n"
    
    return new_frame_data

#characters, pages = get_pages()
#movesets = scrapeAllPages()
#FrameDataGUI.Run(characters)
