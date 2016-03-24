from lxml import etree
from lxml import html
import requests
DEBUG = False
DOWNLOAD = False
OFFLINE_MODE = False
characters = []
pages = []

moveset_arrays = ["Jabs", "Dash Attacks", "Tilts", "Smashes", "Aerials",
                  "Grabs", "Throws", "Dodges"]
all_groundmove_types = ["Jab", "Attack", "tilt", "smash"]
all_move_types = ["Jab", "tilt", "smash", "air", "Attack", "Dash", "Rapid", "Grab", "throw", "dodge", "Roll"]

#TODO: They spelled "dependent" wrong on Kirby's page...

#Simple class structures for storing frame data for moves

class Move:
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
        self.weight = weight
        self.intangibility = intangibility
        self.notes = notes        

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
                "\n         Weight Dependent?: " + self.weight + \
                "\n         Intangibility: " + self.intangibility + \
                "\n         Notes: " + self.notes + \
                "\n\n"  
    
class GroundMove(Move):
    def __init__(self, name, hitbox, faf, base_dmg, angle, bkb_wbkb, kbg):
        self.name = name
        self.hitbox = hitbox
        self.faf = faf
        self.base_dmg = base_dmg
        self.angle = angle
        self.bkb_wbkb = bkb_wbkb
        self.kbg = kbg
        self.landing_lag = "N/A"
        self.autocancel = "N/A"
        self.weight = "N/A"
        self.intangibility = "N/A"
        self.notes = "N/A"       

class Aerial(Move):
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
        self.weight = "N/A"
        self.intangibility = "N/A"
        self.notes = "N/A"               

class Grab(Move):
    def __init__(self, name, hitbox, faf):
        self.name = name
        self.hitbox = hitbox
        self.faf = faf
        self.base_dmg = "N/A"
        self.angle = "N/A"
        self.bkb_wbkb = "N/A"
        self.kbg = "N/A"
        self.landing_lag = "N/A"
        self.autocancel = "N/A"
        self.weight = "N/A"
        self.intangibility = "N/A"
        self.notes = "N/A"         

class Throw(Move):
    def __init__(self, name, weight, base_dmg, angle, bkb, kbg):
        self.name = name
        self.hitbox = "N/A"
        self.faf = "N/A"
        self.base_dmg = base_dmg
        self.angle = angle
        self.bkb_wbkb = bkb
        self.kbg = kbg     
        self.landing_lag = "N/A"
        self.autocancel = "N/A"
        self.weight = weight
        self.intangibility = "N/A"
        self.notes = "N/A"           

class Dodge(Move):
    def __init__(self, name, intangibility, faf, notes = "-"):
        self.name = name
        self.hitbox = "N/A"
        self.faf = faf
        self.base_dmg = "N/A"
        self.angle = "N/A"
        self.bkb_wbkb = "N/A"
        self.kbg = "N/A"
        self.landing_lag = "N/A"
        self.autocancel = "N/A"
        self.weight = "N/A" 
        self.intangibility = intangibility
        self.notes = notes
               

class Special(Move):
    def __init__(self, name, hitbox, faf, base_dmg, angle, bkb_wbkb, kbg):
        self.name = name
        self.hitbox = hitbox
        self.faf = faf
        self.base_dmg = base_dmg
        self.angle = angle
        self.bkb_wbkb = bkb_wbkb
        self.kbg = kbg
        self.landing_lag = "N/A"
        self.autocancel = "N/A"
        self.weight = "N/A"
        self.intangibility = "N/A"
        self.notes = "N/A"     
    
class Moveset:
    def __init__(self, character_name, moveset):
        self.character_name = character_name
        self.moveset = moveset
        self.move_dict = {}
        self.jabs = []
        self.dash_attacks = []
        self.tilts = []
        self.smashes = []
        self.aerials = []
        self.grabs = []
        self.throws = []
        self.dodges = []
        self.specials = []

    def __str__(self):
        moveset_str = self.character_name + ":\n"
        
        moveset_str += "   Jab Attacks:\n"
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

        moveset_str += "   Special Attacks:\n"
        for move in self.specials:
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
        elif className(move) == "Special": self.specials.append(move)
        elif className(move) == "list":
            if DEBUG: print "ignoring empty data..."
            return
        else: raise ValueError("ERROR!!! invalid move")
        self.move_dict[move.name] = move


def className(instance):
    ''' Returns class name of object as string'''
    return instance.__class__.__name__

def scrapePage(character):
    ''' Returns the parsed moveset of a given character
        as a Moveset instance '''
    if len(characters) == 0 or len(pages) == 0:
        get_pages()
    moveset, frame_data = get_frame_data(pages[characters.index(character)])
    parsed_moveset = parse_frame_data(character, frame_data, moveset)
    return parsed_moveset

def scrapeAllPages():
    ''' Returns the parsed movesets for all characters
        as a dictionary of Moveset instance"so s '''
    all_movesets = {}
    if len(characters) == 0 or len(pages) == 0:
        get_pages()
        
    for character in characters:
        char_scrape = scrapePage(character)
        all_movesets[character] = char_scrape
    return all_movesets
    
def get_pages():
    ''' Gets all character names and corresponding URLs from
        the KuroganeHammer Smash4 homepage, or from a text file
        if in offline mode '''
    print "RUNNING IN " + ("OFFLINE MODE" if OFFLINE_MODE else "ONLINE MODE")
    global pages
    global characters
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

def get_frame_data(char_url):
    ''' Takes a given character's URL or name, and returns
        frame data as an array of strings
        (reads data from HTML text file dump if in offline mode) '''

    if len(characters) == 0 or len(pages) == 0:
        get_pages()
        
    if char_url in pages:
        url = char_url
    else:
        if char_url in characters:
            url = pages[characters.index(char_url)]
        else:
            raise ValueError("URL or character name does not exist!")
        

            
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
    frame_data = []
    for table_num in xrange(2,5):
        frame_table = root.xpath('//table[position()=' + str(table_num) + ']//th | ' +
                                '//table[position()=' + str(table_num) + ']//td')
        frame_table = [element.text_content() for element in frame_table]
        frame_data.append(frame_table)
    clean_frame_data = trim_frame_data(frame_data)
    
    if DEBUG:
        for x in frame_data: print x
    moveset = root.xpath('//table[position()!=1]//th')
    moveset = [element.text_content() for element in moveset]
    clean_moveset = trim_non_move_name(moveset)
    return clean_moveset, clean_frame_data
    #return clean_frame_data

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

def move_gen(move_data):
    data_len = len(move_data)
    if data_len == 0: return []
    else: move_name = move_data[0]
    
    if data_len == 3 and isGrab(move_name): newMove = Grab(*move_data)
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
    return newMove

def parse_frame_data(character_name, frame_data, moveset):
    '''Goes through a clean array of frame data strings and parses it
        into objects for the respective move type, and pushes them to
        a Moveset object. Returns the final Moveset object'''
    
    ground_frame_data = frame_data[0]
    aerial_frame_data = frame_data[1]
    special_frame_data = frame_data[2]
    #Create a moveset object for the given character
    allMoves = Moveset(character_name, moveset)
    print "Starting data parsing for " + character_name + "..."
    move_data = []
    move_name = ""
    for datum in ground_frame_data:
        # Iterates through frame data, and once a move name has been found,
        # starts collecting the following data until
        # another move name has been found. The collected move data
        # is then put into an appropriate Move object, based on
        # amount of data collected and a check of the move type
        if isMove(datum):
            newMove = move_gen(move_data)
            allMoves.addMove(newMove)
            if DEBUG: print "Added " + ("nothing" if data_len == 0 else move_name) + ", now parsing", datum
            move_name = datum
            move_data = [datum]
        else:
            move_data.append(datum)

    #Capture the last move of the array
    newMove = move_gen(move_data)
    allMoves.addMove(newMove)
    
    move_data = []
    move_name = ""
    for datum in aerial_frame_data:
        # Iterates through frame data, and once a move name has been found,
        # starts collecting the following data until
        # another move name has been found. The collected move data
        # is then put into an appropriate Move object, based on
        # amount of data collected and a check of the move type
        if isMove(datum):
            newMove = move_gen(move_data)
            allMoves.addMove(newMove)
            if DEBUG: print "Added " + "nothing" if data_len == 0 else move_name + ", now parsing", datum
            move_name = datum
            move_data = [datum]
        else:
            move_data.append(datum)

    #Capture the last move of the array
    newMove = move_gen(move_data)
    allMoves.addMove(newMove)
    
    move_data = []
    move_name = ""
    for idx in range(len(special_frame_data)):
        # Iterates through frame data, and once a move name has been found,
        # starts collecting the following data until
        # another move name has been found. The collected move data
        # is then put into an appropriate Move object, based on
        # amount of data collected and a check of the move type
        datum = special_frame_data[idx]
        if idx % 7 == 0:
            newMove = []
            data_len = len(move_data)
            if data_len == 0: pass
            elif data_len == 7: newMove = Special(*move_data)
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
            
    #Capture the last move of the array
    newMove = Special(*move_data)
    allMoves.addMove(newMove)
    
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
    stripped_data = []
    for table in raw_frame_data:
        stripped_table = []
        for move in table:
            if move not in terms_to_remove: stripped_table += [move.encode('utf-8')]
        stripped_data += [stripped_table]

    # The following for loop is for replacing the
    # empty frame data for some characters' attacks
    # with '?', so that the amount of data per attack (6 or 8 strings)
    # stays consistent
    replace_empty = False
    frame_data_counter = 0
    new_ground_frame_data = []
    for datum in stripped_data[0]:
        if isGroundMove(datum):
            replace_empty = True
            frame_data_counter = 6
        elif isMove(datum):
            replace_empty = False
        elif replace_empty:
            frame_data_counter -= 1
            if frame_data_counter < 0:
                replace_empty = False
        new_ground_frame_data.append("?" if replace_empty and datum == "" else datum)
    new_frame_data += [filter(None, new_ground_frame_data)] #Remove all remaining empty strings

    new_frame_data += [map(lambda datum: "?" if datum == "" else datum, stripped_data[1])]
    new_frame_data += [map(lambda datum: "?" if datum == "" else datum, stripped_data[2])]
    if DEBUG:
        print "PRINTING CLEAN STRIPPED DATA..."
        print new_frame_data
        print "\n\n\n"
    
    return new_frame_data

def trim_non_move_name(raw_moveset):
    ''' Takes scraped HTML page, and strips non-move words from page '''
    # Strip non-move words from scraped page
    terms_to_remove = ["Statistic", "Value/Rank", "Attacks",
              'Hitbox Active', 'FAF', 'Angle',
              'BKB/WBKB', 'KBG', 'BKB', 'Base Dmg.',
              'Miscellaneous', 'Intangibility', 'Notes',
              'Landing Lag', 'Autocancel', 'Grabs', 'Throws',
              'Weight Dependent?', 'Weight Dependant?', 'Base Dmg. (+SD)',
              'Useless Tractor Beams']
    clean_moveset = []
    for move in raw_moveset:
        if move not in terms_to_remove: clean_moveset += [move.encode('utf-8')]
        
    if DEBUG:
        print "PRINTING CLEAN MOVESET..."
        print clean_moveset
        print "\n\n\n"
    
    return clean_moveset

def character_sort(characters):
    characters.sort()
    for mii_fighter in ["Mii Swordfighter", "Mii Brawler", "Mii Gunner"]:
        if mii_fighter in characters:
            characters.remove(mii_fighter)
            characters.append(mii_fighter)
    
#characters, pages = get_pages()
#movesets = scrapeAllPages()
#FrameDataGUI.Run(characters)
