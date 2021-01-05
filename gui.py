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

import brainflow
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams
import time
from scipy import signal
import pyo as p
import threading
from ipywidgets import interact

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class App(tkinter.Tk):
    def __init__(self):
        
        self.RT_Params = {
            "Synth" : {"sin" : 0, "pinknoise" : 1},
            "Presets" : {"Delta" : 0, "Alpha" : 1, "Beta" : 2, "Gamma" : 3, "EGG" : 4, "EMG" : 5, "SoftECG" : 6, "HardECG" : 7, "Manual" : 8},
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
            "mouse_x" : 0,
            "mouse_y" : 0,
            "fs" : 250,
            "zi_bp" : None,
            "zi_bs" : None,
            "raw" : [],
            "recording" : [],
            "a" : 400,
            "b" : 400,
            "c" : 0,
            "q" : 10
        }
        
        self.buffer = np.array([0.0 for _ in range(1)])
        self.init_GUI()
        self.init_Graph()
        self.start()
  
    def start(self):
        try :
            #self.update_GUI()
            self.board = self.start_board()
            self.s, self.osc = self.start_audio()
            #self.init_Graph()
            modulate()
        except :
            return 0
            #self.stop()
            
   # def stop(self) :
   #     self.stop_board()
   #     self.stop_audio()
   #     self.stop_modulation()
        
    def update_params(self, key, value) :
        self.update_osc()
        self.update_filter()
        self.update_GUI()
        
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
        
        self.init_Synth()
        self.init_Presets()
        self.init_Filtering()
        self.init_Modulation()
        self.init_Scale()
        #self.init_Graph()
        
        #graph
        
        
        self.gui_init = ImageTk.PhotoImage(self.gui_init)
        self.canvas.create_image(544,804, anchor= tkinter.SE, image=self.gui_init)
        self.canvas.pack()
    
    def init_Synth(self) :
        self.v = tk.IntVar()
        self.sin = tk.Radiobutton(self, variable = self.v, value= self.RT_Params["Synth"].get("sin"), bg = "black", command = self.update_Synth)
        self.pink = tk.Radiobutton(self, variable = self.v, value=self.RT_Params["Synth"].get("pinknoise"), bg = "black", command = self.update_Synth)
        self.canvas.create_window(390,60, window = self.sin)
        self.canvas.create_window(390,102, window = self.pink)
        
    def init_Presets(self):
        self.vp = tk.IntVar()
        self.delta = tk.Radiobutton(self, variable = self.vp, value= self.RT_Params["Presets"].get("Delta"), bg = "black", command = self.update_Presets)
        self.alpha = tk.Radiobutton(self, variable = self.vp, value=self.RT_Params["Presets"].get("Alpha"), bg = "black", command = self.update_Presets)
        self.beta = tk.Radiobutton(self, variable = self.vp, value= self.RT_Params["Presets"].get("Beta"), bg = "black", command = self.update_Presets)
        self.gamma = tk.Radiobutton(self, variable = self.vp, value=self.RT_Params["Presets"].get("Gamma"), bg = "black", command = self.update_Presets)
        self.egg = tk.Radiobutton(self, variable = self.vp, value= self.RT_Params["Presets"].get("EGG"), bg = "black", command = self.update_Presets)
        self.emg = tk.Radiobutton(self, variable = self.vp, value=self.RT_Params["Presets"].get("EMG"), bg = "black", command = self.update_Presets)
        self.softecg = tk.Radiobutton(self, variable = self.vp, value=self.RT_Params["Presets"].get("SoftECG"), bg = "black", command = self.update_Presets)
        self.hardecg = tk.Radiobutton(self, variable = self.vp, value= self.RT_Params["Presets"].get("HardECG"), bg = "black", command = self.update_Presets)
        self.manual = tk.Radiobutton(self, variable = self.vp, value=self.RT_Params["Presets"].get("Manual"), bg = "black", command = self.update_Presets)
        
        self.canvas.create_window(46,240, window = self.delta)
        self.canvas.create_window(105,240, window = self.alpha)
        self.canvas.create_window(161,240, window = self.beta)
        self.canvas.create_window(220,240, window = self.gamma)
        self.canvas.create_window(279,240, window = self.egg)
        self.canvas.create_window(335,240, window = self.emg)
        self.canvas.create_window(387,240, window = self.softecg)
        self.canvas.create_window(444,240, window = self.hardecg)
        self.canvas.create_window(502,240, window = self.manual)
 
    def init_Filtering(self):
        var = tk.DoubleVar()
        
        self.LCF = tk.Scale(self, orient= tk.HORIZONTAL, length="420", bg="black", command = self.update_lcf)
        self.HCF = tk.Scale(self, orient= tk.HORIZONTAL, length="420", bg="black", command = self.update_hcf)
        self.NTC = tk.Scale(self, orient= tk.HORIZONTAL, length="420", bg="black", command = self.update_ntc)
        
        self.LCF_Label = tk.Label(self, text= "0", bg = "black", fg="white")
        self.HCF_Label = tk.Label(self, text= "0", bg = "black", fg="white")
        self.NTC_Label = tk.Label(self, text= "0", bg = "black", fg="white")
        
        self.canvas.create_window(320,395, window = self.NTC)
        self.canvas.create_window(320,357, window = self.HCF)
        self.canvas.create_window(320,320, window = self.LCF)
    
    def init_Modulation(self):
        #Modulation
        self.Exp = tk.Scale(self, from_=0, to=100, tickinterval=1, orient= tk.HORIZONTAL, length="420", bg="black", command = self.update_exp)
        self.Lin = tk.Scale(self, orient= tk.HORIZONTAL, length="420", bg="black", command = self.update_lin)
        self.Add = tk.Scale(self, orient= tk.HORIZONTAL, length="420", bg="black", command = self.update_add)
        
        self.Exp_Label = tk.Label(self, text= "0", bg = "black", fg="white")
        self.Lin_Label = tk.Label(self, text= "0", bg = "black", fg="white")
        self.Add_Label = tk.Label(self, text= "0", bg = "black", fg="white")
        
        self.canvas.create_window(320,565, window = self.Add)
        self.canvas.create_window(320,527, window = self.Lin)
        self.canvas.create_window(320,500, window = self.Exp)
    
    def init_Scale(self):
        #V-Scale
        self.V_Scale = tk.Scale(self, orient= tk.VERTICAL, length="120", bg="black")
        self.canvas.create_window(420,720, window = self.V_Scale)
        
        #T-Scale
        self.T_Scale = tk.Scale(self, orient= tk.VERTICAL, length="120", bg="black")
        self.canvas.create_window(490,720, window = self.T_Scale)
        
        #Volume
        self.Volume = tk.Scale(self, orient= tk.VERTICAL, length="90", bg="black")
        self.canvas.create_window(420,80, window = self.Volume)
    
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
        
        self.update_Boot()
        self.update_Record()
        self.update_Flip()
        self.update_Energy()
        
        self.gui = ImageTk.PhotoImage(self.gui)
        self.canvas.create_image(544,804, anchor= tkinter.SE, image=self.gui)
        
    def update_Boot(self) :
        headbox = (479,19,533,71)
        if (self.RT_Params["boot"]) :
            self.gui_crop = Image.open("./image/boot_off.png")
            self.gui.paste(self.gui_crop, (479,19))
        else :
            self.gui_mock_crop = Image.open("./image/boot_on.png")
            self.gui.paste(self.gui_mock_crop, (479,19))
        self.gui.save("./image/updateGUI.png")
        
    def update_Record(self) :
        headbox = (481,87,531,137)
        if (self.RT_Params["record"]) :
            self.gui_crop = Image.open("./image/record_off.png")
            self.gui.paste(self.gui_crop, (481,87))
        else :
            self.gui_mock_crop = Image.open("./image/record_on.png")
            self.gui.paste(self.gui_mock_crop, (481,87))
        self.gui.save("./image/updateGUI.png")

    def update_Flip(self):
        headbox = (200,41,217,57)
        if (self.RT_Params["flip"]) :
            self.gui_crop = Image.open("./image/flip_off.png")
            self.gui.paste(self.gui_crop, (200,41))
        else :
            self.gui_mock_crop = Image.open("./image/radio_on.png")
            self.gui.paste(self.gui_mock_crop, (200,41))
        self.gui.save("./image/updateGUI.png")
        
    def update_Energy(self):
        headbox = (201,108,218,125)
        if (self.RT_Params["energy"]) :
            self.gui_crop = Image.open("./image/energy_off.png")
            self.gui.paste(self.gui_crop, (201,108))
        else :
            self.gui_mock_crop = Image.open("./image/radio_on.png")
            self.gui.paste(self.gui_mock_crop, (201,108))
        self.gui.save("./image/updateGUI.png")

    def update_Synth(self):
        print(self.v.get())
    
    def update_Presets(self):
        print(self.vp.get())

    def update_lcf(self, val):
        self.RT_Params["LCF"] = val
        self.LCF_Label['text'] = val
        self.LCF_Label.place(x=66, y=320)
        self.filter_update(LCF = self.RT_Params["LCF"], HCF = self.RT_Params["HCF"], FS = 250)
        print (val)
        
    def update_hcf(self, val):
        self.RT_Params["HCF"] = val
        self.HCF_Label['text'] = val
        self.filter_update(LCF = self.RT_Params["LCF"], HCF = self.RT_Params["HCF"], FS = 250)
        self.HCF_Label.place(x=66, y=355)
       
    def update_ntc(self, val):
        self.RT_Params["NTC"] = val
        self.NTC_Label['text'] = val
        self.NTC_Label.place(x=66, y=385)
        
    def update_exp(self, val):
        self.RT_Params["Exp"] = val
        self.Exp_Label['text'] = val
        self.Exp_Label.place(x=66, y=490)
        
    def update_lin(self, val):
        self.RT_Params["Lin"] = val
        self.Lin_Label['text'] = val
        self.Lin_Label.place(x=66, y=525)
        
    def update_add(self, val):
        self.RT_Params["Add"] = val
        self.Add_Label['text'] = val
        self.Add_Label.place(x=66, y=555)

    def key(self, event):
        print ("pressed", repr(event.char))

    def callback(self, event):
        self.RT_Params["mouse_x"] = event.x
        self.RT_Params["mouse_y"] = event.y
        self.update_GUI()

    def start_board(self):
        params = BrainFlowInputParams ()
        params.serial_port = 'COM3'
        self.board = BoardShim(0,params)
        self.board.prepare_session ()
        self.board.start_stream (2)
        return self.board
        

    def start_audio(self):
        s = p.Server(nchnls=1, sr=150000, buffersize=1024).boot()
        
        # sinusoidal oscillator (uncomment the line below and comment out the lines below it)
    #     osc = p.SineLoop(freq=1).out()

        # filtered noise
        n = p.PinkNoise()
        self.osc = p.ButBP(n,q=10).out()
        
        
        
        #uncomment the lines below to record the audio in a wav file
    #     s.recordOptions(dur=20, filename="./recording,wav", fileformat=0, sampletype=1)
    #     s.recstart()

        s.start()
        return s,self.osc
        
    def run(self,x):
        self.buffer = np.roll(self.buffer,-1)
        self.buffer[-1] = x
        y,z_bs = self.bandstop(60-3,60+3,self.buffer, self.fs, self.zi_bs)
        self.zi_bs = z_bs
        y,z_bp = self.bandpass(self.lcf,self.hcf,y, self.fs, self.zi_bp)
        self.zi_bp = z_bp
        return y[-1]
    
    def update(self, lcf=None, hcf=None, fs=None ):
        if lcf:
            self.lcf = lcf
        if hcf:
            self.hcf = hcf
        if fs:
            self.fs = fs
    
    def bandpass(self, start, stop, data, fs = 250, z=None):
            bp_Hz = np.array([start, stop])
            b, a = signal.butter(2, bp_Hz / (fs / 2.0), btype='bandpass')
            if isinstance(z,np.ndarray):
                zi = z
            else:
                zi = signal.lfilter_zi(b, a)
            return signal.lfilter(b, a, data, zi =zi, axis=0)
            
    def bandstop(self, start, stop, data, fs = 250, z=None):
            bp_Hz = np.array([start, stop])
            b, a = signal.butter(2, bp_Hz / (fs / 2.0), btype='bandstop')
            if isinstance(z,np.ndarray):
                zi = z
            else:
                zi = signal.lfilter_zi(b, a)
            return signal.lfilter(b, a, data, zi =zi, axis=0)

    def param_update(slef, A, B, C):
        self.a = A
        self.b = B
        self.c = C
    
    #filter parameters
    lcf=2
    hcf=120
    fs=250

    def filter_update(self, LCF = lcf, HCF = hcf, FS = fs):
        #global ff
        self.update(lcf=LCF, hcf=HCF, fs=FS)
        
    def freq_update(self, r):
        f = float(self.run(r))
        # uncomment the lines below to record the raw signal or the filtered signal (recording)
    #     raw.append(r)
        self.RT_params["recording"].append(f)
        self.osc.freq = float(b * np.exp(min( f/a , 4 ))) + c

    def stream(self):
        channel = 5 # the channel from which you are recording (N5P). Don't forget you need a bias channel too.
        
        cd=self.board.get_current_board_data(1)[channel][0]
        try:
            while True:
                # whenever the value of the current board data is changed, update the frequency of the oscillator
                ncd=self.board.get_current_board_data(1)[channel][0]
                if ncd!=cd:
                    cd = ncd
                    self.freq_update(cd)

        except KeyboardInterrupt:
            print("Press Ctrl-C to terminate while statement")
            self.s.stop()
            
    def modulate(self) :
        # run to modulate the sound with the data from the board
        st = threading.Thread(target=stream, daemon=True)
        st.start()
        
            
    def init_Graph(self) :
        self.fig = plt.figure(figsize=(3.6,1.4), dpi=100, facecolor='black')
        self.ax = plt.subplot(111, xlim=(0,50), ylim=(0,1024), facecolor ='black')
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        
        max_points = 50
        self.line, = self.ax.plot(np.arange(max_points), np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='yellow', ms=1)
        
        self.draw_Graph()
    
    def init_line(self) :
        return self.line

    def draw_Graph(self) :
        #self.graph_Label = tk.Label(self, bg = "black", fg="white")
        self.canvas3 = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().place(relx=0.05, rely=0.8)
        anim = animation.FuncAnimation(self.fig, self.animate, init_func = self.init_line, frames=200, interval = 50, blit=False)
        plt.show(block=False)
            
    def animate(self, i) :
        self.y = random.randint(0,1024)
        self.old_y = self.line.get_ydata()
        self.new_y = np.r_[self.old_y[1:], self.y]
        self.line.set_ydata(self.new_y)
        print(self.new_y)
        return self.line
    
if __name__ == '__main__':
    App().mainloop()






