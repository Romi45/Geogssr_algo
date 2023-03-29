import tkinter as tk
import tkintermapview
import pyttsx3
from geopy.geocoders import Nominatim
import csv
from random import randint


locator = Nominatim(user_agent='myGeocoder')



#engine = pyttsx3.init()

class Geogssr():

    def __init__(self):
        
        self.file = '/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\countries.csv'
        self.flags_folder = "/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\Flags/Flags_png/"
        self.data = {}
        self.flag_labels = []
        self.max_flag_width = 200
        self.current_country = 'Germany'
        self.score = 0
        self.country_is_displayed = False
        

        
        #tk window creation
        self.root_tk = tk.Tk()
        self.root_tk.geometry(f"{1200}x{700}")
        self.root_tk.title("map_view_example.py")

        #creating 2 frames to place items inside
        """self.frame_left = tk.Frame(self.root_tk, width = 0, height = 700, background='lightblue')
        self.frame_left.grid(row = 0, column=0)
        self.frame_left.pack_propagate(False)""" 
        
        self.frame_right = tk.Frame(self.root_tk, width=1200, height = 700)
        self.frame_right.grid(row=0,column=0)
        self.frame_right.pack_propagate(False) 
        self.score = tk.IntVar()
        self.score.set(0)

        

        

        #create the map widget with tkintermapview and sets map
        self.map_widget = tkintermapview.TkinterMapView(self.frame_right, width=1200, height=700, corner_radius=10)
        self.map_widget.set_tile_server("https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png")
        #map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.add_left_click_map_command(self.add_marker_event)
        self.map_widget.pack(side=tk.LEFT)

        #create the score tracker at the top
        self.score_tracker_label = tk.Label(self.frame_right, textvariable = self.score, font='Arial 30 bold')
        self.score_tracker_label.place(bordermode=tk.OUTSIDE, x = (1200/2))

        #startup functions
        self.data =  self.load_data(self.file)
        self.country_display('de')


    #handles a click on the map ==> checks if country is the right one, displays a new country if yes
    def add_marker_event(self, event):
        location = locator.reverse((event[0], event[1]))
        country_code = location.raw['address']['country_code'].upper()
        country = self.data[country_code]
        print(country[0], self.current_country)
        if country[0] == self.current_country: 
            self.score.set(self.score.get() + 1)
            new_flag = self.random_flag()
            self.current_country = self.data[new_flag][0]
            self.country_display(new_flag)
            print('True', new_flag)

        


    #load csv file with country names/codes in a dictionnary
    def load_data(self, file):
            with open(file, newline = "") as csvfile:
                reader = csv.reader(csvfile, delimiter = ",")
                data = {}
                for country, country_code in reader:
                    if country_code not in data:
                        data[country_code] = [country]
                    else:
                        data[country_code].append(country)
            return data
        



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
        return countries[number]


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

    def score_tracker(self):
        """self.score_tracker = 
        """

    # create map widget
    






if __name__ == '__main__':
    Geogssr_window = Geogssr()
    #Geogssr_window.root_tk.wm_attributes('-transparentcolor', 'red')
    Geogssr_window.root_tk.mainloop()



"""print(location.raw['address']['country'], location.raw['address']['country_code'])
    engine.say(country)
    engine.runAndWait()"""