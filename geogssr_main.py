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

        #tk window creation
        self.root_tk = tk.Tk()
        self.root_tk.geometry(f"{1500}x{700}")
        self.root_tk.title("map_view_example.py")
        
        self.file = '/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\countries.csv'
        self.flags_folder = "/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\Flags/Flags_png/"
        self.neighbours_file = '/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\country_neighbours.json'
        
        self.light_tile = "https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"
        self.dark_tile = "https://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png"

        self.rules_text = 'description jeu'
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
        self.intro_window = tk.Toplevel(self.root_tk, bg=self.bg_color)
        self.intro_window.grab_set()
        

        self.intro_label = tk.Label(self.intro_window, text='Welcome to Geoguessr !', bg=self.bg_color, fg='white', font='Arial 20 bold')
        self.rules_textbox = tk.Text(self.intro_window, font = 'Arial 15', bg=self.bg_color, fg=self.fg_color)
        self.strat_game = tk.Button(self.intro_window, text='Start game', font='Arial 20 bold', bg=self.bg_color, fg=self.fg_color, command=self.intro_window.destroy)

        self.intro_label.pack()
        self.rules_textbox.pack()
        self.strat_game.pack()
        self.rules_textbox.insert(tk.END,self.rules_text)


    def create_widgets(self):

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
        if self.islands:
            self.islands = False
            self.islands_label.set('Islands : OFF')
        else:
            self.islands = True
            self.islands_label.set('Islands : ON')


    def close_difficulty_menu(self):

        self.current_time = time.time()
        self.time_diff = datetime.timedelta(seconds = int(self.current_time- self.pause_time))
        self.start_time = self.start_time + self.time_diff.seconds
        self.timer = True
        self.update_clock()
        self.difficulty_window.destroy()
        
    def update_theme(self):
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


    #handles a click on the map ==> checks if country is the right one, displays a new country if yes
    def add_marker_event(self, event):

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

    #load csv file with country names/codes in a dictionnary
    def load_data(self, file):
            with open(file, newline = "") as csvfile:
                reader = csv.reader(csvfile, delimiter = ",")
                data = {}
                for country, country_code in reader:
                    if country_code not in data:
                        data[country_code] = country
            return data
    
    
    #load json file with countries' 2-letter code assigned to a list of the names of neighbouring countries
    def load_data_neighbours(self,file):
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
        max_flag_width = self.max_flag_width
        width = flag.width()
        if width > max_flag_width:
            return max_flag_width
        return width

    #picks a random flag
    def random_flag(self):
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


    #displays new flag
    def country_display(self, country_code):        
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
        self.hint_text = self.data_neighbours[self.current_country_code.lower()]
        if self.hint_text:
            self.hint_text = f"{self.current_country}'s neighbors are : \n{self.hint_text}\n"
            self.hint_textbox.insert(tk.END, self.hint_text)
        else:
            self.hint_text = "Looks like this country's an island..."
            self.hint_textbox.insert(tk.END, self.hint_text)


    def end_of_game(self):
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



