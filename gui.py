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
        
        tkinter.Tk.__init__(self)
        self.configure(background='black')
        self.title("Physiophone 0.1")
        self.minsize(544,804)
        self.configure(bg = 'black')
        self.gui_init = Image.open("./image/GUI.png")
        self.gui_init = self.gui_init.resize((544,804))
        self.gui = Image.open("./image/GUI.png")
        self.gui = self.gui.resize((544,804))
        self.gui_mock = Image.open("/Users/hyeonah/Desktop/Project/Physiophone/internetradioplayer/internetradioplayer/image/GUI-mock.png")
        self.gui_mock = self.gui_mock.resize((544,804))
        
        self.canvas = Canvas(self, width=544, height=804)
        self.canvas.bind('<Key>', self.key)
        self.canvas.bind('<Button-1>', self.callback)
        self.canvas.pack()

        self.params = {
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
            
            "headbox" : [(479,19,533,71),(481,87,531,137)]
        }
        
        
        #sttk.Scrollbar(self).grid(row =1, column = 1)
        
        
        
        #body = Image.open("GUI.png")
        self.head = Image.open("./image/GUI-mock.png")
        #body = self.img.resize((544,804))
        self.head = self.head.resize((544,804))
        
        self.gui_init = ImageTk.PhotoImage(self.gui_init)
        self.canvas.create_image(544,804, anchor= tkinter.SE, image=self.gui_init)
        self.canvas.pack()
        
        
        #self = ThemedTk(theme="black")
        #self.set_theme("black")
#        self.root = ThemedTk(theme="black")
#        self.root.get_themes()
#        #root.set_theme("arc")
#
#        rightframe = Frame(self.root)
#        bottomframe = Frame(rightframe)
#        bottomframe.pack()
#
#        self.scale4 = ttk.Scale(bottomframe, orient= tk.HORIZONTAL)
#        self.scale4.grid(row=2, column=2, pady=15, padx=30)
        
        #self.canvas.create_window(160,400, window = self.scale4)
        
    

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
        
    def guiInit(self) :
        self.gui = Image.open("./image/GUI.png")
        self.gui = self.gui.resize((544,804))
        
    def updateBoot(self) :
        headbox = (479,19,533,71)
        if (self.params["boot"]) :
            #self.params["boot"] = False
            self.gui.crop(headbox).save("boot_off.png")
            self.gui_crop = Image.open("./boot_off.png")
            self.gui.paste(self.gui_crop, (479,19))
        else :
            #self.params["boot"] = True
            self.gui_mock.crop(headbox).save("boot_on.png")
            self.gui_mock_crop = Image.open("./boot_on.png")
            self.gui.paste(self.gui_mock_crop, (479,19))
        self.gui.save("./image/updateGUI.png")
        
    def updateRecord(self) :
        headbox = (481,87,531,137)
        if (self.params["record"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/record_off.png")
            self.gui_crop = Image.open("./image/record_off.png")
            self.gui.paste(self.gui_crop, (481,87))
        else :
            #self.params["record"] = True
            self.gui_mock.crop(headbox).save("./image/record_on.png")
            self.gui_mock_crop = Image.open("./image/record_on.png")
            self.gui.paste(self.gui_mock_crop, (481,87))
        self.gui.save("./image/updateGUI.png")

    def updateFlip(self):
        headbox = (200,41,217,57)
        if (self.params["flip"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/flip_off.png")
            self.gui_crop = Image.open("./image/flip_off.png")
            self.gui.paste(self.gui_crop, (200,41))
        else :
            #self.params["record"] = True
            self.gui_mock.crop(headbox).save("./image/radio_on.png")
            self.gui_mock_crop = Image.open("./image/radio_on.png")
            self.gui.paste(self.gui_mock_crop, (200,41))
        self.gui.save("./image/updateGUI.png")
        
    def updateEnergy(self):
        headbox = (201,108,218,125)
        if (self.params["energy"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/energy_off.png")
            self.gui_crop = Image.open("./image/energy_off.png")
            self.gui.paste(self.gui_crop, (201,108))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("energy_on.png")
            self.gui_mock_crop = Image.open("./image/radio_on.png")
            self.gui.paste(self.gui_mock_crop, (201,108))
        self.gui.save("./image/updateGUI.png")
        
    def updateSinusoidal(self):
        headbox = (376,55,385,68)
        if (self.params["sinusoidal"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/sinusoidal_off.png")
            self.gui_crop = Image.open("./image/sinusoidal_off.png")
            self.gui.paste(self.gui_crop, (376,55))
        else :
            #self.params["record"] = True
            self.gui_mock.crop(headbox).save("./image/sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/sinusoidal_on.png")
            self.gui.paste(self.gui_mock_crop, (376,55))
        self.gui.save("./image/updateGUI.png")
        
    def updatePinknoise(self):
        headbox = (380,104,386,125)
        if (self.params["pinknoise"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/pinknoise_off.png")
            self.gui_crop = Image.open("./image/pinknoise_off.png")
            self.gui.paste(self.gui_crop, (380,104))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/sinusoidal_on.png")
            self.gui.paste(self.gui_mock_crop, (376,100))
        self.gui.save("./image/updateGUI.png")

    def updateHardECG(self):
        headbox = (439,241,443,244)
        if (self.params["hardecg"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/hardecg_off.png")
            self.gui_crop = Image.open("./image/hardecg_off.png")
            self.gui.paste(self.gui_crop, (440,242))
        else :
            #self.params["record"] = True
            self.gui_mock.crop(headbox).save("./image/hardecg_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (439,241))
        self.gui.save("./image/updateGUI.png")
        
    def updateDelta(self):
        headbox = (44,242,47,244)
        if (self.params["delta"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/delta_off.png")
            self.gui_crop = Image.open("./image/delta_off.png")
            self.gui.paste(self.gui_crop, (46,244))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (44,241))
        self.gui.save("./image/updateGUI.png")
        
    def updateAlpha(self):
        headbox = (102,243,104,245)
        if (self.params["alpha"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/alpha_off.png")
            self.gui_crop = Image.open("./image/alpha_off.png")
            self.gui.paste(self.gui_crop, (102,243))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (100,241))
        self.gui.save("./image/updateGUI.png")

    def updateBeta(self):
        headbox = (158,242,159,244)
        if (self.params["beta"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/beta_off.png")
            self.gui_crop = Image.open("./image/beta_off.png")
            self.gui.paste(self.gui_crop, (158,242))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (157,241))
        self.gui.save("./image/updateGUI.png")

    def updateGamma(self):
        headbox = (214,242,216,243)
        if (self.params["gamma"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/gamma_off.png")
            self.gui_crop = Image.open("./image/gamma_off.png")
            self.gui.paste(self.gui_crop, (214,242))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (213,241))
        self.gui.save("./image/updateGUI.png")

    def updateEGG(self):
        headbox = (271,241,273,244)
        if (self.params["egg"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/egg_off.png")
            self.gui_crop = Image.open("./image/egg_off.png")
            self.gui.paste(self.gui_crop, (271,241))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (269,240))
        self.gui.save("./image/updateGUI.png")
    
    def updateEMG(self):
        headbox = (328,242,330,244)
        if (self.params["emg"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/emg_off.png")
            self.gui_crop = Image.open("./image/emg_off.png")
            self.gui.paste(self.gui_crop, (328,242))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (327,241))
        self.gui.save("./image/updateGUI.png")
        
    def updateSoftECG(self):
        headbox = (384,242,386,244)
        if (self.params["softecg"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/softecg_off.png")
            self.gui_crop = Image.open("./image/softecg_off.png")
            self.gui.paste(self.gui_crop, (384,242))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (383,241))
        self.gui.save("./image/updateGUI.png")
        
    def updateManual(self):
        headbox = (497,242,499,243)
        if (self.params["manual"]) :
            #self.params["record"] = False
            self.gui.crop(headbox).save("./image/manual_off.png")
            self.gui_crop = Image.open("./image/manual_off.png")
            self.gui.paste(self.gui_crop, (497,242))
        else :
            #self.params["record"] = True
            #self.gui_mock.crop(headbox).save("sinusoidal_on.png")
            self.gui_mock_crop = Image.open("./image/hardecg_on.png")
            self.gui.paste(self.gui_mock_crop, (496,241))
        self.gui.save("./image/updateGUI.png")

    def callback(self, event):
    
        #GUI init function
        self.guiInit()
         
        #boot
        if (479 <= event.x <= 516 and 22 <= event.y <= 70):
            if (self.params["boot"]) :
                self.params["boot"] = False
            else :
                self.params["boot"] = True
                       
        #record
        if (481 <= event.x <= 531 and 87 <= event.y <= 137):
            if (self.params["record"]) :
                self.params["record"] = False
            else :
                self.params["record"] = True
                
        #Flip
        if( 183 <= event.x <= 233 and 22 <= event.y <=72):
            if (self.params["flip"]) :
                self.params["flip"] = False
            else :
                self.params["flip"] = True

        #energy
        if( 183 <= event.x <= 233 and 88 <= event.y <= 137):
            if (self.params["energy"]) :
                self.params["energy"] = False
            else :
                self.params["energy"] = True
        
        #Sinusoidal
        if( 256 <= event.x <= 388 and 44 <= event.y <= 75):
            if (self.params["sinusoidal"]) :
                self.params["sinusoidal"] = False
            else :
                self.params["sinusoidal"] = True

        #Pink Noise
        if( 257 <= event.x <= 386 and 92 <= event.y <= 125):
            if (self.params["pinknoise"]) :
                self.params["pinknoise"] = False
            else :
                self.params["pinknoise"] = True
        
        #Delta
        if( 26 <= event.x <= 66 and 173 <= event.y <= 249):
            if (self.params["delta"]) :
                self.params["delta"] = False
            else :
                self.params["delta"] = True
 
        #Alpha
        if( 80 <= event.x <= 128 and 173 <= event.y <= 245):
            if (self.params["alpha"]) :
                self.params["alpha"] = False
            else :
                self.params["alpha"] = True
 
        #Beta
        if( 137 <= event.x <= 180 and 173 <= event.y <= 245):
            if (self.params["beta"]) :
                self.params["beta"] = False
            else :
                self.params["beta"] = True
 
        #Gamma
        if( 190 <= event.x <= 238 and 173 <= event.y <= 245):
            if (self.params["gamma"]) :
                self.params["gamma"] = False
            else :
                self.params["gamma"] = True

        #EGG
        if( 252 <= event.x <= 293 and 173 <= event.y <= 245):
            if (self.params["egg"]) :
                self.params["egg"] = False
            else :
                self.params["egg"] = True
                
        #EMG
        if( 308 <= event.x <= 347 and 173 <= event.y <= 245):
            if (self.params["emg"]) :
                self.params["emg"] = False
            else :
                self.params["emg"] = True
                
        #Soft ECG
        if( 362 <= event.x <= 408 and 172 <= event.y <= 245):
            if (self.params["softecg"]) :
                self.params["softecg"] = False
            else :
                self.params["softecg"] = True

        #Hard ECG
        if( 418 <= event.x <= 466 and 173 <= event.y <= 245):
            if (self.params["hardecg"]) :
                self.params["hardecg"] = False
            else :
                self.params["hardecg"] = True

        #Manual
        if( 481 <= event.x <= 521 and 173 <= event.y <= 245):
            if (self.params["manual"]) :
                self.params["manual"] = False
            else :
                self.params["manual"] = True
                
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
                
        
        print ("clicked at", event.x, event.y)
        
    def move_window(self,event):
        global img
        cx, cy = event2canvas(event, self.canvas)
        x,y,wh = (int(cx),int(cy),100)
        window_data = self.foreground_image_data[y:y+wh,x:x+wh]
        bg_img = self.background_image_data.copy()
        bg_img[y:y+wh,x:x+wh] = window_data
        img = ImageTk.PhotoImage(PIL.Image.fromarray(bg_img))
        self.canvas.create_image(0, 0,image=img,anchor="nw")
    
        
    # When you click to exit, this function is called 
    def on_exit(self):
        self.destroy()
        
if __name__ == '__main__':
    App().mainloop()



