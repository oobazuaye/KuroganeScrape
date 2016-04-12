import Tix as tk
import PyScrape
TITLE_FONT = ("Helvetica", 32, "bold")
TITLE_FONT_2 = ("Helvetica", 18, "bold")
LABEL_FONT = ("Fixedsys", 12, "bold")
MAX_COLUMN = 100
MAX_ROW = 40
class ScrapeGUI:
    def __init__(self, main):
        
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
        row = 1
        col = 0
        for character in self.characters:
            button = tk.Button(self.frame, text=character,
                               command=lambda char = character:
                               self.addchar(char))
            self.character_buttons[character] = button
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
            col += 1
            if col == 5:
                row += 1
                col = 0
                
        
        submitbutton = tk.Button(self.frame, text="Compare Selected Characters",
                                 command=self.submit)
        submitbutton.grid(row=row+1, column=2, columnspan=3, sticky="nsew", pady=20)
        
        backbutton = tk.Button(self.frame, text="Back", command=lambda: back(self))
        backbutton.grid(row=row+2, column=0, sticky="nsew", pady=5)

    def addchar(self, character):
        if character not in self.selected_characters:
            self.selected_characters.append(character)
            self.character_buttons[character].config(relief=tk.SUNKEN, bg="red")            
        else:
            self.selected_characters.remove(character)
            self.character_buttons[character].config(relief=tk.RAISED, bg = self.def_color)
        
    def submit(self):
        if len(self.selected_characters ) < 1:
            return
        PyScrape.character_sort(self.selected_characters)
        print self.selected_characters
        movesets = []
        for character in self.selected_characters:
            movesets += [PyScrape.scrapePage(character)]
            
        move_select = MoveSelect(self.parent, self, movesets)
        self.grid_remove()
        move_select.grid(row=0, column=0, sticky="nsew")


class MoveSelect(tk.Frame):
    def __init__(self, parent, prev_page, movesets):
        tk.Frame.__init__(self, parent)  
        self.parent = parent
        self.prev_page = prev_page
        addScrollBar(self)
        expandContainer(self)
        self.def_color = parent.cget("bg")
        self.selected_moves = []
        self.move_buttons = {}
        
        col_start = -2
        bottom_row = 2
        for moveset_obj in movesets:
            col_start += 3
            col = col_start
            char_label = tk.Label(self.frame, text=moveset_obj.character_name, font=TITLE_FONT_2)
            char_label.grid(row=1, column=col, columnspan=2, sticky="nsew", pady=20)
            row = 2
            for move in moveset_obj.moveset:
                button = tk.Button(self.frame, text=move,
                                   command=lambda obj=moveset_obj, mv=move:self.addmove(obj, mv))
                self.move_buttons[(moveset_obj.character_name, move)] = button
                button.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
                col += 1
                if col - col_start == 2:
                    row += 1
                    col = col_start
            bottom_row = max(row, bottom_row)

        label = tk.Label(self.frame, text="Select Moves to Compare", font=TITLE_FONT)
        label.grid(row=0, column=col_start / 2, columnspan=5, sticky="nsew", pady=20)
        
        submitbutton = tk.Button(self.frame, text="Compare Selected Moves",
                                 command=self.submit)
        submitbutton.grid(row=bottom_row+1, column=2, stick="nsew", pady=20)
        
        backbutton = tk.Button(self.frame, text="Back", command=lambda: back(self))
        backbutton.grid(row=bottom_row+2, column=0, sticky="nsew", pady=5)

    def addmove(self, char_moveset, move):
        char_move_tuple = (char_moveset, move)
        button_tuple = (char_moveset.character_name, move)
        if char_move_tuple not in self.selected_moves:
            self.selected_moves.append(char_move_tuple)
            self.move_buttons[button_tuple].config(relief=tk.SUNKEN, bg="red")            
        else:
            self.selected_moves.remove(char_move_tuple)
            self.move_buttons[button_tuple].config(relief=tk.RAISED, bg = self.def_color)
                
    def submit(self):
        if len(self.selected_moves) < 1:
            return
        print self.selected_moves

        data_display = DataDisplay(self.parent, self,
                                   self.selected_moves)
        self.grid_remove()
        data_display.grid(row=0, column=0, sticky="nsew")
        
class DataDisplay(tk.Frame):
    def __init__(self, parent, prev_page, selected_moves):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.prev_page = prev_page
        addScrollBar(self)
        expandContainer(self)
        self.def_color = parent.cget("bg")

        
        row = 5
        
        for datum in PyScrape.all_data_types:
            datum_label = tk.Label(self.frame, text=datum, font=LABEL_FONT)
            datum_label.grid(row=row, column=1, sticky="nsew", padx=30)
            row += 1

        col = 2
        for moveset_obj, move_name in selected_moves:
            move_obj = moveset_obj.move_dict[move_name]
            char_name = moveset_obj.character_name
            self.displayMove(move_obj, char_name, col)
            col += 1
            
        label = tk.Label(self.frame, text="Moveset Frame Data Comparison", font=TITLE_FONT)
        label.grid(row=0, column=col / 2, columnspan=5, sticky="nsew", pady=20)
        
        restartbutton = tk.Button(self.frame, text="Start over",
                                 command=self.restart)
        restartbutton.grid(row=row+1, column=2, stick="nsew", pady=20)        
        backbutton = tk.Button(self.frame, text="Back", command=lambda: back(self))
        backbutton.grid(row=row+3, column=0, sticky="nsew", pady=5)

    def displayMove(self, move_obj, character_name, col):
        row = 5
        frame_data = move_obj.moveArray()
        move_name = move_obj.name
        print frame_data
        move_name_label = tk.Label(self.frame, text=character_name + "\n" + move_name, font=LABEL_FONT)
        move_name_label.grid(row=2, column=col, rowspan=3, sticky="nsew", pady=20)    
        for datum in frame_data: 
            entry = tk.Entry(self.frame)
            entry.insert(0, datum)
            entry.grid(row=row, column=col)
            entry.config(state='readonly')
            row += 1
            
    def restart(self):
        self.grid_forget()
        self.destroy()
        self.prev_page.prev_page.prev_page.grid()
    
def addScrollBar(parent):
    parent.canvas = tk.Canvas(parent, borderwidth=0)
    parent.frame = tk.Frame(parent.canvas)
        
    parent.vscrollbar = tk.Scrollbar(parent, orient="vertical", command=parent.canvas.yview)
    parent.hscrollbar = tk.Scrollbar(parent, orient="horizontal", command=parent.canvas.xview)
    parent.canvas.configure(yscrollcommand=parent.vscrollbar.set, xscrollcommand=parent.hscrollbar.set)

    parent.vscrollbar.grid(row=0, column=MAX_COLUMN, sticky="nsew")
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
    
