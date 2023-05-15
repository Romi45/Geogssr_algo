import tkinter as tk
import tkintermapview
from geopy.geocoders import Nominatim
import csv
from random import randint
import json
import time 
import datetime
locator = Nominatim(user_agent='myGeocoder')





class Geogssr():

    def __init__(self):
        """
        initialises most of the attributes we will need for the game to take place;
        more importantly starts the timer and use our start up functions
        
        parameters:
        none
        ------
        returns:
        none
        """
        #tk window creation
        self.root_tk = tk.Tk()
        self.root_tk.geometry(f"{1500}x{700}")
        self.root_tk.title("map_view_example.py")
        
        self.file = '/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\countries.csv'
        self.flags_folder = "/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\Flags/Flags_png/"
        self.neighbours_file = '/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\country_neighbours.json'
        
        self.light_tile = "https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"
        self.dark_tile = "https://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png"

        self.rules_text = 'Welcome to geoguessr! \n\nIn this game, your goal is to click on the country corresponding to the flag appearing. To do so, use your mouse to navigate the map and locate the country (you can zoom in or out by scrolling the mouse).\n\nThere are three levels of difficulty, and you can select to play with or without islands (which are harder to locate). These setting are accesible by clicking on "Change difficulty" button of the main window. The 3 difficulty levels correspond to the amount of time you have to find each country: \n\n - 60s for the easiest\n - 30s for the medium \n - 10s for the hardest\n\nIf you are ever stuck, you can click on the hint button that will give you the neighbours of the country you are looking for.\nThe "Change theme" button also allows you to choose between a dark and light scheme.\n\nPress the button "Start Game" when you are ready !'
        self.data_neighbours = {}
        self.data = {}
        self.flag_labels = []
        self.difficulty_dic = {'Easy : 60 seconds per country':60,'Medium : 30 seconds per country':30,'Hard : 10 seconds per country':10}
        self.max_flag_width = 200
        self.current_country = 'Germany'
        self.current_country_code = 'DE'

        self.country_is_displayed = False
        self.timer = True
        self.intro_done = False
        self.islands = True
        self.theme = True
        self.start_time = time.time()
        self.current_time = time.time()
        self.time_diff = datetime.timedelta(seconds = (self.current_time-self.start_time))

        self.bg_color = '#212227'
        self.fg_color = '#FFEF9F'

        self.dark_theme = ['#212227','#FFEF9F']
        self.light_theme = ['#394867','#F1F6F9']

        self.difficulty = tk.StringVar()
        self.difficulty.set('Easy : 60 seconds per country')
        self.score = tk.IntVar()
        self.score.set(0)
        self.current_country_text = tk.StringVar()
        self.current_country_text.set(self.current_country.upper())
        self.islands_label = tk.StringVar()
        self.islands_label.set('Islands : ON')

        self.number_plays = tk.IntVar()
        self.number_plays.set(0)
        
        self.number_plays_display = tk.StringVar()
        self.number_plays_display.set(str(self.number_plays.get()) +'/10' )
        self.create_widgets()
        
       

        #startup functions
        self.data =  self.load_data(self.file)
        self.data_neighbours = self.load_data_neighbours(self.neighbours_file)
        self.country_display('de')
        time.sleep(1)
        

    def intro(self):
        """
        creates a page that welcomes the player and shows you the rule.
        
        parameters:
        none
        ------
        returns:
        none
        """
        self.intro_window = tk.Toplevel(self.root_tk, bg=self.bg_color)
        self.intro_window.grab_set()
        

        self.intro_label = tk.Label(self.intro_window, text='Welcome to Geoguessr !', bg=self.bg_color, fg='white', font='Arial 20 bold')
        self.rules_textbox = tk.Text(self.intro_window, font = 'Arial 15', bg=self.bg_color, fg=self.fg_color)
        self.start_game = tk.Button(self.intro_window, text='Start game', font='Arial 20 bold', bg=self.bg_color, fg=self.fg_color, command=self.intro_window.destroy)

        self.intro_label.pack()
        self.rules_textbox.pack()
        self.start_game.pack()
        self.rules_textbox.insert(tk.END,self.rules_text)


    def create_widgets(self):
        """
        puts in place the map as well as the UI that we provide the player;
        displaying thing such as their score, the flag of teh target country, etc...
        
        parameters:
        none
        ------
        returns:
        none
        """
        #creating 2 frames to place items inside
        self.frame_left = tk.Frame(self.root_tk, width = 300, height = 700, background=self.bg_color)
        self.frame_left.grid(row = 0, column=0)
        self.frame_left.pack_propagate(False)
        
        self.frame_right = tk.Frame(self.root_tk, width=1200, height = 700)
        self.frame_right.grid(row=0,column=1)
        self.frame_right.pack_propagate(False)

        #create the map widget with tkintermapview and sets map
        self.map_widget = tkintermapview.TkinterMapView(self.frame_right, width=1200, height=700, corner_radius=10)
        self.map_widget.set_tile_server("https://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png")

        #map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.add_left_click_map_command(self.add_marker_event)
        self.map_widget.pack(side=tk.LEFT)

        #create the score tracker at the top
        self.score_tracker_label = tk.Label(self.frame_right, textvariable = self.score, font='Arial 30 bold')
        self.score_tracker_label.place(bordermode=tk.OUTSIDE, x = (1200/2))

        #where's label
        self.label1 = tk.Label(self.frame_left, text="Where's", font = 'Arial 20 bold', bg =self.bg_color, fg='white',pady = 5 )
        self.label1.pack(fill='x')

        #country user is looking for
        self.current_country_display = tk.Label(self.frame_left, textvariable = self.current_country_text, font='Arial 15 bold', bg=self.bg_color, fg=self.fg_color,pady=20)
        self.current_country_display.pack(fill='x')
        

        #hint button
        self.hint_button = tk.Button(self.frame_left, text ='Hint', bg=self.bg_color,fg='white', font='Arial 20 bold', padx = '50', command=self.hint)
        self.hint_button.pack()


        #timer_label
        self.timer_label = tk.Label(self.frame_left, text=self.time_diff, font='Calibri 20 bold', bg = self.bg_color, fg=self.fg_color)
        self.timer_label.pack(fill='x')


        #hint textbox
        self.hint_textbox = tk.Text(self.frame_left, font = 'Arial 15 bold', bg=self.bg_color, fg=self.fg_color, height = 10)
        self.hint_textbox.pack()

        
        #number of plays label
        self.number_plays_label = tk.Label(self.frame_left, textvariable=self.number_plays_display, bg = self.bg_color, fg=self.fg_color, font = 'Arial 30 bold',pady=40)
        self.number_plays_label.pack()

        #select difficulty mode
        self.difficulty_change = tk.Button(self.frame_left, text = 'Change difficulty level', command=self.difficulty_toplevel, bg=self.bg_color, fg='white', font='Arial 15 bold')
        self.difficulty_change.pack()

        #select theme button
        self.select_theme = tk.Button(self.frame_left, text='Change Theme', font='Arial 15 bold',bg=self.bg_color, fg='white', command=self.update_theme)
        self.select_theme.pack()
        
        #quit button
        self.quit_button_mainframe = tk.Button(self.frame_left, text='Quit', font='Arial 15 bold', bg=self.bg_color,fg='white',command=self.root_tk.destroy)
        self.quit_button_mainframe.pack()
        

        self.intro()
        self.update_clock()
        


    def difficulty_toplevel(self):
        """
        pauses the timer and display a new window asking the player to choose a difficulty and if they want to play with islands or not;
        easy gives them 60  seconds per country, medium 30 and hard only 10.
        
        parameters:
        none
        ------
        returns:
        none
        """

        self.pause_time = self.current_time
        self.timer = False
        self.difficulty_window = tk.Toplevel(self.root_tk, bg=self.bg_color)
        self.difficulty_window.grab_set()
        self.label3 = tk.Label(self.difficulty_window, text='Choose your difficulty level :', font = 'Arial 20 bold', bg=self.bg_color, fg=self.fg_color)
        self.difficulty_options = tk.OptionMenu(self.difficulty_window, self.difficulty, 'Easy : 60 seconds per country','Medium : 30 seconds per country','Hard : 10 seconds per country')
        self.confirm_button = tk.Button(self.difficulty_window, text='Confirm', bg=self.bg_color, fg='white', font='Arial 15 bold', command=self.close_difficulty_menu)
        self.islands_button = tk.Button(self.difficulty_window, bg=self.bg_color, fg=self.fg_color, textvariable = self.islands_label, font='Arial 15 bold', command=self.change_islands_mode)
        self.label3.pack()
        self.difficulty_options.pack()
        self.islands_button.pack()
        self.confirm_button.pack()
    
    def change_islands_mode(self):
        """
        changes whether the player can have to guess island or not and adapts the label accordingly
        
        parameters:
        none
        ------
        returns:
        none
        """
        if self.islands:
            self.islands = False
            self.islands_label.set('Islands : OFF')
        else:
            self.islands = True
            self.islands_label.set('Islands : ON')


    def close_difficulty_menu(self):
        """
        unpauses the game, updates the clock/timer to insure no issues happen and close the window to choose the difficulty
        
        parameters:
        none
        ------
        returns:
        none
        """

        self.current_time = time.time()
        self.time_diff = datetime.timedelta(seconds = int(self.current_time- self.pause_time))
        self.start_time = self.start_time + self.time_diff.seconds
        self.timer = True
        self.update_clock()
        self.difficulty_window.destroy()
        
    def update_theme(self):
        """
        changes the theme color of the map, allowing to play in light or dark mode
        
        parameters:
        none
        ------
        returns:
        none
        """
        
        if self.theme:
            self.theme = False
            self.bg_color = self.light_theme[0]
            self.fg_color =self.light_theme[1]
            tile_server = self.light_tile
        else:
            self.theme = True
            self.bg_color = self.dark_theme[0]
            self.fg_color = self.dark_theme[1]
            tile_server = self.dark_tile
        self.frame_left.configure(background=self.bg_color)
        self.map_widget.set_tile_server(tile_server)
        for i in self.frame_left.winfo_children():
            try:
                i.configure(bg=self.bg_color, fg=self.fg_color)
            except:
                print('cant do it')

    def update_clock(self):
        """
        Handles the timer of the game, and insures that if the time is up, to change the flag to be guessed
        
        parameters:
        none
        ------
        returns:
        none
        """

        if self.intro_done:
            if self.timer:
                self.current_time = time.time()
                self.time_diff = datetime.timedelta(seconds=int(self.current_time-self.start_time))
                self.timer_label.config(text=self.time_diff)
            else:
                self.time_diff = datetime.timedelta(seconds=0)
        else: 
            try:
                self.intro_window.state()
            except:
                self.intro_done = True
                self.start_time = time.time()
        
        if self.time_diff.seconds >= self.difficulty_dic[self.difficulty.get()]:
                self.start_time = time.time()
                new_flag = self.random_flag()
                self.current_country_code = new_flag
                self.current_country = self.data[new_flag]
                self.current_country_text.set(self.current_country.upper())
                self.country_display(new_flag)
                self.hint_textbox.delete(1.0, tk.END)
        self.timer_label.after(1000, self.update_clock)

        
    def add_marker_event(self, event):
        """
        handles a click on the map, give the coordinates it corresponds to and prints the country it corresponds to for the player to see;
        if the click is on the right country, moves on to the next one otherwise does nothing
        
        parameters:
        event
        ------
        returns:
        none
        """
        location = locator.reverse((event[0], event[1]))
        country_code = location.raw['address']['country_code'].upper()
        country = self.data[country_code]
        if country == self.current_country:
            self.start_time = time.time() 
            self.score.set(self.score.get() + 1)
            new_flag = self.random_flag()
            self.current_country_code = new_flag
            self.current_country = self.data[new_flag]
            self.current_country_text.set(self.current_country.upper())
            self.country_display(new_flag)
            self.hint_textbox.delete(1.0, tk.END)

    
    def load_data(self, file):
        """
        load the csv file with country names/codes in a dictionnary
        
        parameters:
        file(.csv extension)
        ------
        returns:
        data(dictionary) = links the countris 2-letter code (key) to the country's actual name (value)
        """
            with open(file, newline = "") as csvfile:
                reader = csv.reader(csvfile, delimiter = ",")
                data = {}
                for country, country_code in reader:
                    if country_code not in data:
                        data[country_code] = country
            return data
    
    
    
    def load_data_neighbours(self,file):
        """
        load json file with countries' 2-letter code assigned to a list of the names of the neighbouring countries
        
        parameters:
        file(.json extension)
        ------
        returns:
        jsondata(dictionary) = links a country (key) to a list of it's neighboring countries (item)
        """
        jsondata= {}
        with open(file, 'r') as jsonfile:
            tmp = json.load(jsonfile)
            for i in tmp:
                str_list = ''
                for e in tmp[i]:
                    str_list += e[0] + ' '
                tmp[i] = str_list
                jsondata[i] = tmp[i]
        return jsondata
    

    #defines the size of the label depending on size of the displayed flag and a max threshold
    def label_size(self, flag):
        """
        adapts the size of the label flag depending on size of the displayed flag,
        makes sure it's not oversized
         
        parameters:
        flag(.png) =  image of a flag
        ------
        returns:
        width(int) = the width with which we display the flag
        """
        max_flag_width = self.max_flag_width
        width = flag.width()
        if width > max_flag_width:
            return max_flag_width
        return width

    #picks a random flag
    def random_flag(self):
        """
        picks a random country code that will be used to choose the next flag of the game randomly;
        if the number of rounds exceeds 10, ends the game
         
        parameters:
        none
        ------
        returns:
        country_code(string): the two letter code for a countries name
        """
        number = randint(0,len(self.data))
        countries = list(self.data.keys())
        self.number_plays.set(self.number_plays.get() + 1)
        self.number_plays_display.set(str(self.number_plays.get()) +'/10' )
        new_flag = countries[number]
        if not self.islands:
                print(self.data_neighbours[new_flag.lower()])
                print(len(self.data_neighbours[new_flag.lower()]))
                while len(self.data_neighbours[new_flag.lower()]) == 0:
                   new_flag = self.random_flag() 
        if self.number_plays.get() >= 10:
            self.end_of_game()
        return new_flag


    
    def country_display(self, country_code):
        """
        displays the new flag corresponding to the country selected by random_flag
         
        parameters:
        country_code(string): the two letter code for a countries name
        ------
        returns:
        none
        """
        country_code = country_code.lower()
        flag_path = self.flags_folder + country_code + ".png"
        self.img = tk.PhotoImage(file=flag_path)
        self.img = self.img.subsample(2,2)
        self.img_label = tk.Label(self.frame_right, image=self.img,height=100,bg='lightblue', border = None,width = self.label_size(self.img)-5)
        
        for i in self.flag_labels:
            i.destroy()
            self.flag_labels.pop()
        self.flag_labels.append(self.img_label)
        self.img_label.photo = self.img
        self.img_label.place(relx=0, rely=1.0, anchor='sw')


    def hint(self):
        """
        displays a hint for the player, in the form of the neighboring countries of the current target
        if the list of neighboring countries is empty, we tell the player to look for an island
         
        parameters:
        none
        ------
        returns:
        none
        """
        self.hint_text = self.data_neighbours[self.current_country_code.lower()]
        if self.hint_text:
            self.hint_text = f"{self.current_country}'s neighbors are : \n{self.hint_text}\n"
            self.hint_textbox.insert(tk.END, self.hint_text)
        else:
            self.hint_text = "Looks like this country's an island..."
            self.hint_textbox.insert(tk.END, self.hint_text)


    def end_of_game(self):
        """
        Is launched at the end of the game, recaps your score and ask you if you would like to play again.
         
        parameters:
        none
        ------
        returns:
        none
        """
        self.timer = False
        self.endgame_window = tk.Toplevel(self.root_tk, bg = self.bg_color)
        self.endgame_window.grab_set()
        endscore = str(self.score.get()) + '/10'
        self.label4 = tk.Label(self.endgame_window, text='Your final score is :', font='Arial 30 bold', bg=self.bg_color, fg='white')
        self.end_score = tk.Label(self.endgame_window, text=endscore, fg=self.fg_color, bg=self.bg_color, font='Arial 40 bold',pady=100)
        self.label4.pack()
        self.end_score.pack()
        self.restart_game_button = tk.Button(self.endgame_window, text = 'Start new game', bg=self.bg_color, fg='white', font='Arial 15 bold',command = self.restart_game)
        self.restart_game_button.pack()
        self.quit_button = tk.Button(self.endgame_window, text='Quit', font='Arial 15 bold', bg=self.bg_color,fg='white',command=self.root_tk.destroy)
        self.quit_button.pack()

        
    def restart_game(self):
        """
        relaunches a new game, in easy mode by default
         
        parameters:
        none
        ------
        returns:
        none
        """
        self.timer = True
        self.start_time = time.time()
        self.endgame_window.destroy()
        self.score.set(0)
        self.number_plays.set(0)
        self.number_plays_display.set(str(self.number_plays.get()) + '/10')
        self.difficulty.set('Easy : 60 seconds per country')


    






if __name__ == '__main__':
    Geogssr_window = Geogssr()
    Geogssr_window.root_tk.mainloop()


