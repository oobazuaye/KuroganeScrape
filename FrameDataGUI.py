import Tkinter as tk
TITLE_FONT = ("Helvetica", 18, "bold")

class ScrapeGUI:
    def __init__(self, main, characters):
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
        self.start = StartPage(main, characters)
        self.start.grid(row=0, column=0, sticky="nsew")

class StartPage(tk.Frame):
    def __init__(self, parent, characters):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.characters = characters
        label = tk.Label(self, text="Kurogane Scraper v1.0.0", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        begin = tk.Button(self, text="Begin", command=self.select_character)
        begin.pack(side="bottom")

    def select_character(self):
        select = CharacterSelect(self.parent, self, self.characters)
        self.grid_remove()
        select.grid(row=0, column=0, sticky="nsew")
        #select.tkraise()

class CharacterSelect(tk.Frame):
    def __init__(self, parent, startpage, characters):
        tk.Frame.__init__(self, parent)
        self.startpage = startpage
        self.characters = characters
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
        for character in characters:
            button_index = characters.index(character)
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
        #self.controller.show_frame("MoveSelect")

    def back(self):
        self.grid_forget()
        self.destroy()
        self.startpage.grid()
        
'''   
class MoveSelect(tk.Frame):
    def __init__(self, parent, controller, characters):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selected_characters = []
        self.character_buttons = []
        label = tk.Label(self, text="Select characters to compare", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        allchars = tk.Button(self, text="Compare All Characters", command=lambda: self.submit(characters))
        for character in characters:
            button_index = characters.index(character)
            button = tk.Button(self, text=character, command=lambda: self.addchar(character, button_index))
            self.character_buttons.append(button)
            button.pack()
        submitbutton = tk.Button(self, text="Compare Selected Characters",
                                 command=lambda: self.submit(selected_characters))
        submitbutton.pack(side="bottom")

    def addchar(self, character, button_index):
        if character not in self.selected_characters:
            self.selected_characters.append(character)
            self.character_buttons[button_index].config(relief=RAISED)            
        else:
            self.selected_characters.remove(character)
            self.character_buttons[button_index].config(relief=SUNKEN)
        
    def submit(self, characters):
        characters.sort()    
'''
def Run(characters):
    root = tk.Tk()
    app = ScrapeGUI(root, characters)
    root.mainloop()

'''
if __name__ == '__main__':
    Run()
'''   
    
