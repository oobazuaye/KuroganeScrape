import Tix as tk
import PyScrape
from PIL import Image, ImageTk
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
        centerWindow(parent, 500,560)
        self.parent = parent
        bg_color = "white"
        self.config(bg=bg_color)
        kurogane_logo_image = ImageTk.PhotoImage(Image.open("images/app/kh_logo.png"))
        smash_logo_image = ImageTk.PhotoImage(Image.open("images/app/smash_logo.png"))
        kurogane_logo = tk.Label(self, image=kurogane_logo_image, bg=bg_color)
        kurogane_logo.pack(side="top")
        kurogane_logo.image = kurogane_logo_image
        smash_logo = tk.Label(self, image=smash_logo_image, bg=bg_color)
        smash_logo.pack(side="top")
        smash_logo.image = smash_logo_image
        title_label = tk.Label(self, text="Kurogane Scraper v1.0.0", font=TITLE_FONT, bg=bg_color, fg="blue")
        title_label.pack(side="top", fill="x", pady=10)
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
        centerWindow(parent, 680, 800)
        self.parent = parent
        self.prev_page = prev_page
        addScrollBar(self)
        expandContainer(self)
        self.characters, _ = PyScrape.get_pages()
        self.selected_characters = []
        self.character_buttons = {}
        label = tk.Label(self.frame, text="Select Characters to Compare", font=TITLE_FONT)
        label.grid(row=0, column=0, columnspan=5, sticky="nsew", pady=20, padx=60)
        row = 1
        col = 0
        for character in self.characters:
            photo = ImageTk.PhotoImage(Image.open("images/app/" + character + ".png").resize((100, 100), Image.ANTIALIAS))
            button = tk.Button(self.frame, text=character,
                               command=lambda char = character:
                               self.addchar(char), image=photo,
                               bg="steel blue",
                               compound="bottom")
            button.image = photo
            self.character_buttons[character] = button
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
            col += 1
            if col == 5:
                row += 1
                col = 0
                
        addCompareButton(self, "COMPARE SELECTED CHARACTERS", row, 4)
        addBackButton(self, row)

    def addchar(self, character):
        if character not in self.selected_characters:
            self.selected_characters.append(character)
            self.character_buttons[character].config(relief=tk.SUNKEN, bg="red", fg="yellow")            
        else:
            self.selected_characters.remove(character)
            self.character_buttons[character].config(relief=tk.RAISED, bg="steel blue")
        
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
        parent.minsize(640,640)
        self.parent = parent
        self.prev_page = prev_page
        addScrollBar(self)
        expandContainer(self)
        self.selected_moves = []
        self.move_buttons = {}
        
        col_start = -3
        bottom_row = 2
        for moveset_obj in movesets:
            col_start += 3
            col = col_start
            photo = ImageTk.PhotoImage(Image.open("images/app/" + moveset_obj.character_name + ".png"))
            char_label = tk.Label(self.frame, image=photo, font=TITLE_FONT_2)
            char_label.grid(row=1, column=col, columnspan=2, sticky="nsew", pady=20)
            char_label.image=photo
            row = 2
            colors = ["sea green", "purple", "steel blue"]
            color_idx = 0
            for moveset_group in moveset_obj.moveset:
                color = colors[color_idx]
                for move in moveset_group:
                    button = tk.Button(self.frame, text=move,
                                       command=lambda obj=moveset_obj, mv=move:self.addmove(obj, mv),
                                       bg="white", fg = color)
                    self.move_buttons[(moveset_obj.character_name, move)] = button
                    button.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)
                    col += 1
                    if col - col_start == 2:
                        row += 1
                        col = col_start
                color_idx += 1
            bottom_row = max(row, bottom_row)

        label = tk.Label(self.frame, text="Select Moves to Compare", font=TITLE_FONT)
        label.grid(row=0, column=col_start / 2, columnspan=5, sticky="nsew", pady=20)
        
        addCompareButton(self, "COMPARE SELECTED MOVES", bottom_row, col_start + 1)
        addBackButton(self, bottom_row)

    def addmove(self, char_moveset, move):
        char_move_tuple = (char_moveset, move)
        button_tuple = (char_moveset.character_name, move)
        if char_move_tuple not in self.selected_moves:
            self.selected_moves.append(char_move_tuple)
            self.move_buttons[button_tuple].config(relief=tk.SUNKEN, bg="red")            
        else:
            self.selected_moves.remove(char_move_tuple)
            self.move_buttons[button_tuple].config(relief=tk.RAISED, bg="white")
                
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
            datum_label.grid(row=row, column=0, sticky="nsew", padx=30)
            row += 1

        col = 1
        for moveset_obj, move_name in selected_moves:
            move_obj = moveset_obj.move_dict[move_name]
            char_name = moveset_obj.character_name
            self.displayMove(move_obj, char_name, col)
            col += 1
            
        label = tk.Label(self.frame, text="Moveset Frame Data Comparison", font=TITLE_FONT)
        label.grid(row=0, column=max(0, (col - 2) / 2), columnspan=3, sticky="nsew", pady=20)
        
        addCompareButton(self, "START OVER", row, col - 1)
        addBackButton(self, row)

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
            
    def submit(self):
        self.grid_forget()
        self.destroy()
        self.prev_page.prev_page.prev_page.grid()
        #centerWindow(self.parent, 500,560)
    
def addScrollBar(parent):
    parent.canvas = tk.Canvas(parent, borderwidth=0)
    parent.frame = tk.Frame(parent.canvas)
        
    parent.vscrollbar = tk.Scrollbar(parent, orient="vertical", command=parent.canvas.yview)
    parent.hscrollbar = tk.Scrollbar(parent, orient="horizontal", command=parent.canvas.xview)
    parent.canvas.configure(yscrollcommand=parent.vscrollbar.set, xscrollcommand=parent.hscrollbar.set)
    parent.canvas.bind_all("<MouseWheel>", lambda event: parent.canvas.yview_scroll(-1*(event.delta/120), "units"))

    parent.vscrollbar.grid(row=0, column=MAX_COLUMN, sticky="nsew")
    parent.hscrollbar.grid(row=MAX_ROW, column=0, sticky="nsew")
    
    parent.canvas.create_window(0, 0, window=parent.frame, anchor="nw", tags="parent.frame")
    parent.canvas.grid(row=0, column=0, sticky="nsew")
    parent.frame.bind("<Configure>", lambda event: parent.canvas.configure(scrollregion=parent.canvas.bbox("all")))
    
def addCompareButton(parent, labeltext, row, last_col):
    submitbutton = tk.Button(parent.frame, text=labeltext,
                             command=parent.submit, bg="green",
                             font = LABEL_FONT)
    submitbutton.grid(row=row+1, column=1, columnspan=max(1, last_col-1), sticky="nsew", pady=20)
    
def addBackButton(parent, row):
    backbutton = tk.Button(parent.frame, text="BACK", command=lambda: back(parent), bg="orange", width=10)
    backbutton.grid(row=row+2, column=0, sticky="w", pady=5)
    
def back(parent):
    parent.grid_forget()
    parent.destroy()
    parent.prev_page.grid()

def expandContainer(container):
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)

def centerWindow(root, height, width):
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (width/2)
    y = (hs/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def Run():
    root = tk.Tk()
    root.wm_title("Kurogane Scraper v1.0.0")
    app = ScrapeGUI(root)
    root.mainloop()


if __name__ == '__main__':
    Run()
    
