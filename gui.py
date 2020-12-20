#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import signal
import requests
from PIL import Image        # sudo pip3 install pillow
from PIL import ImageTk      # sudo apt-get install python3-pil python3-pil.imagetk
import tkinter               # sudo apt-get install python3-tk
from tkinter import Tk, RIGHT, LEFT, SOLID, ttk
from tkinter import Frame, Label, Button, messagebox, Canvas
from ttkthemes import ThemedTk
import tkinter as tk
import vlc                   # sudo pip3 install python-vlc
from scipy.misc import imread

class App(tkinter.Tk):
    def __init__(self):
        # Depending on distro (i.e. Deepin), full path of static files may be required. That' s what next two lines are for.
        # You can put the directory with this app wherever you want in your disk
        # In elementary os and so in ubuntu comment the follwing
        ##pathname = os.path.dirname(sys.argv[0])
        ##os.chdir(pathname)
        error_flag = 0
        
        self.init_GUI()
        
        self.RT_Params = {
            "Synth" : ["sim","pinknoise"],
            "LCF" : 1,
            "HCF" : 120,
            "NTC" : 60,
            "LIN" : 400,
            "EXP" : 1,
            "ADD" : 0,
            "Volume" : 1,
            "boot" : True,
            "record" : True,
            "flip" : True,
            "energy" : True,
            "sinusoidal" : True,
            "pinknoise" : True,
            "delta" : True,
            "alpha" : True,
            "beta" : True,
            "gamma" : True,
            "egg" : True,
            "emg" : True,
            "softecg" : True,
            "hardecg" : True,
            "manual" : True,
            "mouse_x" : 0,
            "mouse_y" : 0,
        }
        
        
        #sttk.Scrollbar(self).grid(row =1, column = 1)
        
        self.gui_init = ImageTk.PhotoImage(self.gui_init)
        self.canvas.create_image(544,804, anchor= tkinter.SE, image=self.gui_init)
        self.canvas.pack()
        
        
        #self = ThemedTk(theme="black")
        #self.set_theme("black")
#        self = ThemedTk(theme="black")
        #self.root.get_themes()
        #root.set_theme("arc")
#
#        rightframe = Frame(self.root)
#        bottomframe = Frame(rightframe)
#        bottomframe.pack()
#
#        self.scale4 = ttk.Scale(self, orient= tk.HORIZONTAL)
#        self.scale4.grid(row=2, column=2, pady=15, padx=30)
#
#        self.canvas.create_window(160,400, window = self.scale4)
        
    

    # Error messages handling
    def display_error_message(self,msg,flag):
        messagebox.showerror("Error", msg)
        if flag == 1:
            self.destroy()
            
    def motion(self, event):
        print("image clicked : (%s %s)" % (event.x, event.y))
        return
    
    def leftclick(self, event):
        x, y = event.widget.winfo_pointerxy()
        print('{}, {}'.format(x,y))

    def key(self, event):
        print ("pressed", repr(event.char))
        
    def init_GUI(self) :
    
        tkinter.Tk.__init__(self)
        self.configure(background='black')
        self.title("Physiophone 0.1")
        self.minsize(544,804)
        self.configure(bg = 'black')
        self.gui_init = Image.open("./image/GUI.png")
        self.gui_init = self.gui_init.resize((544,804))
        self.gui_mock = Image.open("./image/GUI-mock.png")
        self.gui_mock = self.gui_mock.resize((544,804))
        
        self.canvas = Canvas(self, width=544, height=804)
        self.canvas.bind('<Key>', self.key)
        self.canvas.bind('<Button-1>', self.callback)
        self.canvas.pack()
        
        root = ThemedTk()
        root.get_themes()
        root.set_theme("black")
        
        #self.scale.grid(row=2, column=10, pady=15, padx=30)
        
        #self.scale_frame = Frame(self)
#        var = tk.DoubleVar()
        self.scale = ttk.Scale(self, orient= tk.HORIZONTAL, length="420", variable = var)
#
#        selection = str(var.get())
#        button = ttk.Button(self, text = selection, command=sel )
#        button.pack()
#        #elf.canvas.scale("all, ")

        self.canvas.create_window(320,400, window = self.scale)
        #self.canvas.pack()
        
    def update_GUI(self) :
    
        self.gui = Image.open("./image/GUI.png")
        self.gui = self.gui.resize((544,804))
    
        mouse_x = self.RT_Params["mouse_x"]
        mouse_y = self.RT_Params["mouse_y"]
    
        #boot
        if (479 <= mouse_x <= 516 and 22 <= mouse_y <= 70):
            if (self.RT_Params["boot"]) :
                self.RT_Params["boot"] = False
            else :
                self.RT_Params["boot"] = True
                       
        #record
        if (481 <= mouse_x <= 531 and 87 <= mouse_y <= 137):
            if (self.RT_Params["record"]) :
                self.RT_Params["record"] = False
            else :
                self.RT_Params["record"] = True
                
        #Flip
        if( 183 <= mouse_x <= 233 and 22 <= mouse_y <=72):
            if (self.RT_Params["flip"]) :
                self.RT_Params["flip"] = False
            else :
                self.RT_Params["flip"] = True

        #energy
        if( 183 <= mouse_x <= 233 and 88 <= mouse_y <= 137):
            if (self.RT_Params["energy"]) :
                self.RT_Params["energy"] = False
            else :
                self.RT_Params["energy"] = True
        
        #Sinusoidal
        if( 256 <= mouse_x <= 388 and 44 <= mouse_y <= 75):
            if (self.RT_Params["sinusoidal"]) :
                self.RT_Params["sinusoidal"] = False
            else :
                self.RT_Params["sinusoidal"] = True

        #Pink Noise
        if( 257 <= mouse_x <= 386 and 92 <= mouse_y <= 125):
            if (self.RT_Params["pinknoise"]) :
                self.RT_Params["pinknoise"] = False
            else :
                self.RT_Params["pinknoise"] = True
        
        #Delta
        if( 26 <= mouse_x <= 66 and 173 <= mouse_y <= 249):
            if (self.RT_Params["delta"]) :
                self.RT_Params["delta"] = False
            else :
                self.RT_Params["delta"] = True
 
        #Alpha
        if( 80 <= mouse_x <= 128 and 173 <= mouse_y <= 245):
            if (self.RT_Params["alpha"]) :
                self.RT_Params["alpha"] = False
            else :
                self.RT_Params["alpha"] = True
 
        #Beta
        if( 137 <= mouse_x <= 180 and 173 <= mouse_y <= 245):
            if (self.RT_Params["beta"]) :
                self.RT_Params["beta"] = False
            else :
                self.RT_Params["beta"] = True
 
        #Gamma
        if( 190 <= mouse_x <= 238 and 173 <= mouse_y <= 245):
            if (self.RT_Params["gamma"]) :
                self.RT_Params["gamma"] = False
            else :
                self.RT_Params["gamma"] = True

        #EGG
        if( 252 <= mouse_x <= 293 and 173 <= mouse_y <= 245):
            if (self.RT_Params["egg"]) :
                self.RT_Params["egg"] = False
            else :
                self.RT_Params["egg"] = True
                
        #EMG
        if( 308 <= mouse_x <= 347 and 173 <= mouse_y <= 245):
            if (self.RT_Params["emg"]) :
                self.RT_Params["emg"] = False
            else :
                self.RT_Params["emg"] = True
                
        #Soft ECG
        if( 362 <= mouse_x <= 408 and 172 <= mouse_y <= 245):
            if (self.RT_Params["softecg"]) :
                self.RT_Params["softecg"] = False
            else :
                self.RT_Params["softecg"] = True

        #Hard ECG
        if( 418 <= mouse_x <= 466 and 173 <= mouse_y <= 245):
            if (self.RT_Params["hardecg"]) :
                self.RT_Params["hardecg"] = False
            else :
                self.RT_Params["hardecg"] = True

        #Manual
        if( 481 <= mouse_x <= 521 and 173 <= mouse_y <= 245):
            if (self.RT_Params["manual"]) :
                self.RT_Params["manual"] = False
            else :
                self.RT_Params["manual"] = True
                
        self.updateBoot()
        self.updateRecord()
        self.updateFlip()
        self.updateEnergy()
        self.updateSinusoidal()
        self.updatePinknoise()
        self.updateHardECG()
        self.updateDelta()
        self.updateAlpha()
        self.updateBeta()
        self.updateGamma()
        self.updateEGG()
        self.updateEMG()
        self.updateSoftECG()
        self.updateManual()
        
        self.gui = ImageTk.PhotoImage(self.gui)
        self.canvas.create_image(544,804, anchor= tkinter.SE, image=self.gui)
        
    def updateBoot(self) :
        headbox = (479,19,533,71)
        if (self.RT_Params["boot"]) :
            self.gui_crop = Image.open("./image/boot_off.png")
            self.gui.paste(self.gui_crop, (479,19))
        else :
            self.gui_mock_crop = Image.open("./image/boot_on.png")
            self.gui.paste(self.gui_mock_crop, (479,19))
        self.gui.save("./image/updateGUI.png")
        
    def updateRecord(self) :
        headbox = (481,87,531,137)
        if (self.RT_Params["record"]) :
            self.gui_crop = Image.open("./image/record_off.png")
            self.gui.paste(self.gui_crop, (481,87))
        else :
            self.gui_mock_crop = Image.open("./image/record_on.png")
            self.gui.paste(self.gui_mock_crop, (481,87))
        self.gui.save("./image/updateGUI.png")

    def updateFlip(self):
        headbox = (200,41,217,57)
        if (self.RT_Params["flip"]) :
            self.gui_crop = Image.open("./image/flip_off.png")
            self.gui.paste(self.gui_crop, (200,41))
        else :
            self.gui_mock_crop = Image.open("./image/radio_on.png")
            self.gui.paste(self.gui_mock_crop, (200,41))
        self.gui.save("./image/updateGUI.png")
        
    def updateEnergy(self):
        headbox = (201,108,218,125)
        if (self.RT_Params["energy"]) :
            self.gui_crop = Image.open("./image/energy_off.png")
            self.gui.paste(self.gui_crop, (201,108))
        else :
            self.gui_mock_crop = Image.open("./image/radio_on.png")
            self.gui.paste(self.gui_mock_crop, (201,108))
        self.gui.save("./image/updateGUI.png")
        
    def updateSinusoidal(self):
        headbox = (376,55,385,68)
        if (self.RT_Params["sinusoidal"]) :
            self.gui_crop = Image.open("./image/sinusoidal_off.png")
            self.gui.paste(self.gui_crop, (376,55))
        else :
            self.gui_mock_crop = Image.open("./image/sinusoidal_on.png")
            self.gui.paste(self.gui_mock_crop, (376,55))
        self.gui.save("./image/updateGUI.png")
        
    def updatePinknoise(self):
        headbox = (380,104,386,125)
        if (self.RT_Params["pinknoise"]) :
            self.gui_crop = Image.open("./image/pinknoise_off.png")
            self.gui.paste(self.gui_crop, (380,104))
        else :
            self.gui_mock_crop = Image.open("./image/sinusoidal_on.png")
            self.gui.paste(self.gui_mock_crop, (376,100))
        self.gui.save("./image/updateGUI.png")

    def updateHardECG(self):
        headbox = (439,241,443,244)
        if (self.RT_Params["hardecg"]) :
            self.gui_crop = Image.open("./image/hardecg_off.png")
            self.gui.paste(self.gui_crop, (440,242))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (439,241))
        self.gui.save("./image/updateGUI.png")
        
    def updateDelta(self):
        headbox = (44,242,47,244)
        if (self.RT_Params["delta"]) :
            self.gui_crop = Image.open("./image/delta_off.png")
            self.gui.paste(self.gui_crop, (46,244))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (44,241))
        self.gui.save("./image/updateGUI.png")
        
    def updateAlpha(self):
        headbox = (102,243,104,245)
        if (self.RT_Params["alpha"]) :
            self.gui_crop = Image.open("./image/alpha_off.png")
            self.gui.paste(self.gui_crop, (102,243))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (100,241))
        self.gui.save("./image/updateGUI.png")

    def updateBeta(self):
        headbox = (158,242,159,244)
        if (self.RT_Params["beta"]) :
            self.gui_crop = Image.open("./image/beta_off.png")
            self.gui.paste(self.gui_crop, (158,242))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (157,241))
        self.gui.save("./image/updateGUI.png")

    def updateGamma(self):
        headbox = (214,242,216,243)
        if (self.RT_Params["gamma"]) :
            self.gui_crop = Image.open("./image/gamma_off.png")
            self.gui.paste(self.gui_crop, (214,242))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (213,241))
        self.gui.save("./image/updateGUI.png")

    def updateEGG(self):
        headbox = (271,241,273,244)
        if (self.RT_Params["egg"]) :
            self.gui_crop = Image.open("./image/egg_off.png")
            self.gui.paste(self.gui_crop, (271,241))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (269,240))
        self.gui.save("./image/updateGUI.png")
    
    def updateEMG(self):
        headbox = (328,242,330,244)
        if (self.RT_Params["emg"]) :
            self.gui_crop = Image.open("./image/emg_off.png")
            self.gui.paste(self.gui_crop, (328,242))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (327,241))
        self.gui.save("./image/updateGUI.png")
        
    def updateSoftECG(self):
        headbox = (384,242,386,244)
        if (self.RT_Params["softecg"]) :
            self.gui_crop = Image.open("./image/softecg_off.png")
            self.gui.paste(self.gui_crop, (384,242))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (383,241))
        self.gui.save("./image/updateGUI.png")
        
    def updateManual(self):
        headbox = (497,242,499,243)
        if (self.RT_Params["manual"]) :
            self.gui_crop = Image.open("./image/manual_off.png")
            self.gui.paste(self.gui_crop, (497,242))
        else :
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (496,241))
        self.gui.save("./image/updateGUI.png")
        
    def start(self):
        try :
            self.update_GUI()
            #self.start_board()
            #self.start_audio()
            #self.modulate()
        except :
            self.stop()

    def stop(self) :
        self.stop_board()
        self.stop_audio()
        self.stop_modulation()
        
        

    def callback(self, event):
        self.RT_Params["mouse_x"] = event.x
        self.RT_Params["mouse_y"] = event.y
        self.update_GUI()
        
        print ("clicked at", event.x, event.y)
       
        
#    def move_window(self,event):
#        global img
#        cx, cy = event2canvas(event, self.canvas)
#        x,y,wh = (int(cx),int(cy),100)
#        window_data = self.foreground_image_data[y:y+wh,x:x+wh]
#        bg_img = self.background_image_data.copy()
#        bg_img[y:y+wh,x:x+wh] = window_data
#        img = ImageTk.PhotoImage(PIL.Image.fromarray(bg_img))
#        self.canvas.create_image(0, 0,image=img,anchor="nw")
    
        
    # When you click to exit, this function is called
    def on_exit(self):
        self.destroy()
        
if __name__ == '__main__':
    App().mainloop()




