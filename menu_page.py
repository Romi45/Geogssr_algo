# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:30:03 2023

@author: camil
"""
import tkinter as tk
import json


class Geo_Guess():
    
    def __init__(self):
        self.racine = tk.Tk()
        self.racine.geometry(f"{800}x{500}")
        self.racine.title("Match The Flag")
        
        self.background_image = PhotoImage(file = "name file.png")
        
        self.best_scores = []
        self.file_neighb_c = "list_neighb_countries.json"
        self.dict_neighb_c = {}
        #self.make_dict()
        self.timer = 60
        self.create_widget(self.racine)
       
        
    def create_widget(self, root):
        
        self.set_background = tk.Label(root, i = self.background_image)
        
        self.select = tk.Label(root, text="\nDifficulty")
        self.select.pack(anchor = tk.CENTER)
        
        self.choice_easy = tk.IntVar()
        self.check_easy = tk.Checkbutton(root, text = "Easy mode", onvalue = True,
                                        offvalue = False, height = 1, width = 15,
                                        variable = self.choice_easy)
        self.check_easy.bind('<Button-1>', self.only_one_check)
        self.check_easy.pack(anchor = tk.CENTER)
        self.choice_normal = tk.IntVar()
        self.check_normal = tk.Checkbutton(root, text = "Normal mode", onvalue = True,
                                        offvalue = False, height = 1, width = 15,
                                        variable = self.choice_normal)
        self.check_normal.bind('<Button-1>', self.only_one_check)
        self.check_normal.pack(anchor = tk.CENTER)
        
        self.choice_hard = tk.IntVar()
        self.check_hard = tk.Checkbutton(root, text = "Hard mode", onvalue = True,
                                        offvalue = False, height = 1, width = 15,
                                        variable = self.choice_hard)
        self.check_hard.bind('<Button-1>', self.only_one_check)
        self.check_hard.pack(anchor = tk.CENTER)
        
        self.start = tk.Button(root, text = "Start Game")
        #self.start.bind('<Button-1>', self.game)
        self.start.pack(side = tk.LEFT)
        
        self.quit = tk.Button(root, text = "quit")
        self.quit.bind('<Button-1>', self.close_window)
        self.quit.pack(side = tk.BOTTOM, fill = 'x' )
    
        
    #def make_dict(self):
        #with open(self.file_neighb_c, encoding='utf-8') as jsonfile:
            #self.dict_neighb_c = json.load(jsonfile)
    
    
    def close_window(self, event):
        self.racine.destroy()
        
    def amount_time(self):
        if self.choice_easy.get() :
            self.timer = 90
        
        if self.choice_normal.get() :
            self.timer = 60
            
        if self.choice_hard.get() :
            self.timer = 30
            
    def only_one_check(self,event):
        if self.choice_easy.get() == 0:
            self.check_normal.deselect()
            self.check_hard.deselect()
            
        if self.choice_normal.get() == 0:
            self.check_easy.deselect()
            self.check_hard.deselect()
            
        if self.choice_hard.get() == 0:
            self.check_easy.deselect()
            self.check_normal.deselect()
    
        
            
        
        
        
    
        


if __name__ == "__main__":
    app = Geo_Guess()
    app.racine.mainloop()
