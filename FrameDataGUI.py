import Tix as tk
import PyScrape
TITLE_FONT = ("Helvetica", 32, "bold")
TITLE_FONT_2 = ("Helvetica", 18, "bold")
MAX_COLUMN = 10
MAX_ROW = 10
class ScrapeGUI:
    def __init__(self, main):
        """
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (StartPage, CharacterSelect, MoveSelect):
            page_name = page.__name__
            frame = page(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        """
        expandContainer(main)
    
        self.start = StartPage(main)
        self.start.grid(row=0, column=0, sticky="nsew")

class StartPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        label = tk.Label(self, text="Kurogane Scraper v1.0.0", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        begin_online = tk.Button(self, text="Begin in Online Mode (scrape data from website)", command=lambda: self.select_character("online"))
        begin_offline = tk.Button(self, text="Begin in Offline Mode (use stored data)", command=lambda: self.select_character("offline"))
        #begin.pack(side="bottom")
        begin_online.pack()
        begin_offline.pack()

    def select_character(self, mode):
        if mode == "online":
            PyScrape.OFFLINE_MODE = False
        elif mode == "offline":
            PyScrape.OFFLINE_MODE = True
        else:
            raise ValueError("Invalid mode selection")
        char_select = CharacterSelect(self.parent, self)
        self.grid_remove()
        char_select.grid(row=0, column=0, sticky="nsew")
        #select.tkraise()
        
class CharacterSelect(tk.Frame):
    def __init__(self, parent, prev_page):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.prev_page = prev_page
        addScrollBar(self)
        expandContainer(self)
        self.characters, _ = PyScrape.get_pages()
        self.def_color = parent.cget("bg")
        self.selected_characters = []
        self.character_buttons = {}
        label = tk.Label(self.frame, text="Select 2 characters to compare", font=TITLE_FONT)
        label.grid(row=0, column=2, sticky="nsew", pady=20)
        #label.pack(side="top", fill="x", pady=10)
        #allchars.pack(side="top")
        row = 1
        col = 0
        for character in self.characters:
            button = tk.Button(self.frame, text=character,
                               command=lambda char = character:
                               self.addchar(char))
            self.character_buttons[character] = button
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
            #button.pack()
            col += 1
            if col == 5:
                row += 1
                col = 0
                
        
        submitbutton = tk.Button(self.frame, text="Compare Selected Characters",
                                 command=self.submit)
        submitbutton.grid(row=row+1, column=2, stick="nsew", pady=20)
        
        backbutton = tk.Button(self.frame, text="Back", command=lambda: back(self))
        backbutton.grid(row=row+2, column=0, sticky="nsew", pady=5)
        #submitbutton.pack(side="bottom")

    def addchar(self, character):
        if character not in self.selected_characters:
            self.selected_characters.append(character)
            self.character_buttons[character].config(relief=tk.SUNKEN, bg="red")            
        else:
            self.selected_characters.remove(character)
            self.character_buttons[character].config(relief=tk.RAISED, bg = self.def_color)

        if len(self.selected_characters) > 2:
            oldest_char = self.selected_characters[0]
            self.character_buttons[oldest_char].config(relief=tk.RAISED, bg = self.def_color)
            self.selected_characters.remove(oldest_char)
        
        
    def submit(self):
        if len(self.selected_characters ) < 2:
            return
        PyScrape.character_sort(self.selected_characters)
        print self.selected_characters
        char1_moveset = PyScrape.scrapePage(self.selected_characters[0])
        char2_moveset = PyScrape.scrapePage(self.selected_characters[1])
        move_select = MoveSelect(self.parent, self,
                                 char1_moveset, char2_moveset)
        self.grid_remove()
        move_select.grid(row=0, column=0, sticky="nsew")


class MoveSelect(tk.Frame):
    def __init__(self, parent, prev_page, char1_framedata, char2_framedata):
        tk.Frame.__init__(self, parent)  
        self.parent = parent
        self.prev_page = prev_page
        addScrollBar(self)
        expandContainer(self)
        char1 = char1_framedata.character_name
        char2 = char2_framedata.character_name
        self.char1_framedata = char1_framedata
        self.char2_framedata = char2_framedata
        self.def_color = parent.cget("bg")
        self.selected_moves = []
        self.move_buttons = {}
        label = tk.Label(self.frame, text="Select moves to compare", font=TITLE_FONT)
        label.grid(row=0, column=2, sticky="nsew", pady=20)

        char1_label = tk.Label(self.frame, text=char1, font=TITLE_FONT_2)
        char1_label.grid(row=1, column=0, sticky="nsew", pady=20)
        char2_label = tk.Label(self.frame, text=char2, font=TITLE_FONT_2)
        char2_label.grid(row=1, column=3, sticky="nsew", pady=20)
        #label.pack(side="top", fill="x", pady=10)
        #allchars.pack(side="top")
        row = 2
        col = 0
        for move in char1_framedata.moveset:
            button = tk.Button(self.frame, text=move,
                               command=lambda moveset = char1_framedata, move_name = move:
                               self.addmove(moveset, move_name))
            self.move_buttons[(char1, move)] = button
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
            #button.pack()
            col += 1
            if col == 2:
                row += 1
                col = 0
        bottom_row = row

        col = 3
        row = 2
        for move in char2_framedata.moveset:
            button = tk.Button(self.frame, text=move,
                               command=lambda moveset = char2_framedata, move_name = move:
                               self.addmove(moveset, move_name))
            self.move_buttons[(char2, move)] = button
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
            #button.pack()
            col += 1
            if col == 5:
                row += 1
                col = 3

        row = max(row, bottom_row)
        submitbutton = tk.Button(self.frame, text="Compare Selected Moves",
                                 command=self.submit)
        submitbutton.grid(row=row+1, column=2, stick="nsew", pady=20)
        
        backbutton = tk.Button(self.frame, text="Back", command=lambda: back(self))
        backbutton.grid(row=row+2, column=0, sticky="nsew", pady=5)
        #submitbutton.pack(side="bottom")

    def addmove(self, char_moveset, move):
        char_move_tuple = (char_moveset, move)
        button_tuple = (char_moveset.character_name, move)
        if char_move_tuple not in self.selected_moves:
            self.selected_moves.append(char_move_tuple)
            self.move_buttons[button_tuple].config(relief=tk.SUNKEN, bg="red")            
        else:
            self.selected_moves.remove(char_move_tuple)
            self.move_buttons[button_tuple].config(relief=tk.RAISED, bg = self.def_color)

        if len(self.selected_moves) > 2:
            oldest_char_move = self.selected_moves[0]
            oldest_button_tuple = (oldest_char_move[0].character_name, oldest_char_move[1])
            self.move_buttons[oldest_char_move].config(relief=tk.RAISED, bg = self.def_color)
            self.selected_moves.remove(oldest_char_move)
                
    def submit(self):
        if len(self.selected_moves) < 2:
            return
        print self.selected_moves

        data_display = DataDisplay(self.parent, self,
                                   self.selected_moves[0],
                                   self.selected_moves[1])
        self.grid_remove()
        move_select.grid(row=0, column=0, sticky="nsew")
        
class DataDisplay(tk.Frame):
    def __init__(self, parent, prev_page, move1, move2):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.prev_page = prev_page
        addScrollBar(self)
        expandContainer(self)
        self.def_color = parent.cget("bg")
        label = tk.Label(self.frame, text="Moveset Frame Data Comparison", font=TITLE_FONT)
        label.grid(row=0, column=2, sticky="nsew", pady=20)
        #label.pack(side="top", fill="x", pady=10)
        #allchars.pack(side="top")
        row = 1
        col = 0
        for move in self.moves:
            button_index = self.moves.index(move)
            button = tk.Button(self.frame, text=move,
                               command=lambda move_name = move, index = button_index:
                               self.addmove(move_name, index))
            self.move_buttons.append(button)
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
            #button.pack()
            col += 1
            if col == 5:
                row += 1
                col = 0
        submitbutton = tk.Button(self.frame, text="Compare Selected Moves",
                                 command=self.submit)
        submitbutton.grid(row=row+1, column=2, stick="nsew", pady=20)
        allmoves = tk.Button(self.frame, text="Compare All Moves", command=self.submit)
        allmoves.grid(row=row+2, column=2, sticky="nsew", pady=10)
        backbutton = tk.Button(self.frame, text="Back", command=lambda: back(self))
        backbutton.grid(row=row+3, column=0, sticky="nsew", pady=5)
        #submitbutton.pack(side="bottom")

    
def addScrollBar(parent):
    parent.canvas = tk.Canvas(parent, borderwidth=0)
    parent.frame = tk.Frame(parent.canvas)
        
    parent.vscrollbar = tk.Scrollbar(parent, orient="vertical", command=parent.canvas.yview)
    parent.hscrollbar = tk.Scrollbar(parent, orient="horizontal", command=parent.canvas.xview)
    parent.canvas.configure(yscrollcommand=parent.vscrollbar.set, xscrollcommand=parent.hscrollbar.set)

    parent.vscrollbar.grid(row=0, column=5, sticky="nsew")
    parent.hscrollbar.grid(row=MAX_ROW, column=0, sticky="nsew")
    
    parent.canvas.create_window(0, 0, window=parent.frame, anchor="nw", tags="parent.frame")
    parent.canvas.grid(row=0, column=0, sticky="nsew")
    parent.frame.bind("<Configure>", lambda event: parent.canvas.configure(scrollregion=parent.canvas.bbox("all")))

def back(parent):
    parent.grid_forget()
    parent.destroy()
    parent.prev_page.grid()

def expandContainer(container):
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)
        
def Run():
    root = tk.Tk()
    app = ScrapeGUI(root)
    root.mainloop()


if __name__ == '__main__':
    Run()
    
