import Tkinter as tk
import PyScrape
TITLE_FONT = ("Helvetica", 18, "bold")

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
        self.characters, _ = PyScrape.get_pages()
        self.def_color = parent.cget("bg")
        self.selected_characters = []
        self.character_buttons = []
        self.grid(padx=20, pady=20)
        label = tk.Label(self, text="Select characters to compare", font=TITLE_FONT)
        label.grid(row=0, column=2, sticky="nsew", pady=20)
        #label.pack(side="top", fill="x", pady=10)
        #allchars.pack(side="top")
        row = 1
        col = 0
        for character in self.characters:
            button_index = self.characters.index(character)
            button = tk.Button(self, text=character,
                               command=lambda char = character, index = button_index:
                               self.addchar(char, index))
            self.character_buttons.append(button)
            button.grid(row=row, column=col, sticky="ew", padx=10, pady=5)
            #button.pack()
            col += 1
            if col == 5:
                row += 1
                col = 0
        submitbutton = tk.Button(self, text="Compare Selected Characters",
                                 command=self.submit)
        submitbutton.grid(row=row+1, column=2, stick="nsew", pady=20)
        allchars = tk.Button(self, text="Compare All Characters", command=self.submit)
        allchars.grid(row=row+2, column=2, sticky="nsew", pady=10)
        backbutton = tk.Button(self, text="Back", command=self.back)
        backbutton.grid(row=row+3, column=0, sticky="nsew", pady=5)
        #submitbutton.pack(side="bottom")

    def addchar(self, character, button_index):
        if character not in self.selected_characters:
            self.selected_characters.append(character)
            self.character_buttons[button_index].config(relief=tk.SUNKEN, bg="red")            
        else:
            self.selected_characters.remove(character)
            self.character_buttons[button_index].config(relief=tk.RAISED, bg = self.def_color)
        
    def submit(self):
        self.selected_characters.sort()
        print self.selected_characters
        move_select = MoveSelect(self.parent, self)
        self.grid_remove()
        move_select.grid(row=0, column=0, sticky="nsew")

    def back(self):
        self.grid_forget()
        self.destroy()
        self.prev_page.grid()
        

class MoveSelect(tk.Frame):
    def __init__(self, parent, prev_page):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.prev_page = prev_page
        self.moves = PyScrape.moveset_arrays
        self.def_color = parent.cget("bg")
        self.selected_moves = []
        self.move_buttons = []
        self.grid(padx=20, pady=20)
        label = tk.Label(self, text="Select moves to compare", font=TITLE_FONT)
        label.grid(row=0, column=2, sticky="nsew", pady=20)
        #label.pack(side="top", fill="x", pady=10)
        #allchars.pack(side="top")
        row = 1
        col = 0
        for move in self.moves:
            button_index = self.moves.index(move)
            button = tk.Button(self, text=move,
                               command=lambda move_name = move, index = button_index:
                               self.addmove(move_name, index))
            self.move_buttons.append(button)
            button.grid(row=row, column=col, sticky="ew", padx=10, pady=5)
            #button.pack()
            col += 1
            if col == 5:
                row += 1
                col = 0
        submitbutton = tk.Button(self, text="Compare Selected Moves",
                                 command=self.submit)
        submitbutton.grid(row=row+1, column=2, stick="nsew", pady=20)
        allmoves = tk.Button(self, text="Compare All Moves", command=self.submit)
        allmoves.grid(row=row+2, column=2, sticky="nsew", pady=10)
        backbutton = tk.Button(self, text="Back", command=self.back)
        backbutton.grid(row=row+3, column=0, sticky="nsew", pady=5)
        #submitbutton.pack(side="bottom")

    def addmove(self, move, button_index):
        if move not in self.selected_moves:
            self.selected_moves.append(move)
            self.move_buttons[button_index].config(relief=tk.SUNKEN, bg="red")            
        else:
            self.selected_moves.remove(move)
            self.move_buttons[button_index].config(relief=tk.RAISED, bg = self.def_color)
        
    def submit(self):
        self.selected_moves.sort()
        print self.selected_moves
        self.grid_remove()

    def back(self):
        self.grid_forget()
        self.destroy()
        self.prev_page.grid() 

def Run():
    root = tk.Tk()
    app = ScrapeGUI(root)
    root.mainloop()


if __name__ == '__main__':
    Run()
    
