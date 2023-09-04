#VPP calculation Software by Johanna Vielemeyer
#johanna.vielemeyer@uni-jena.de
#github-link
#-----------------------
from tkinter import font
from tkinter import ttk
import tkinter as tk
from math import *
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import configparser #to read ini-file
import os #to get file name instead of whole file path
from numpy import genfromtxt #to get NaN for empty columns
from scipy import signal
from scipy.signal import butter #for butterworth filter


import calcVPP
import calcCoM
import calcInput

#  -----------------------------------------------------------------------
#-------------------------------------------------------------------------
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

#--------------------------------------------------------------------------
class PageStart(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.background=tk.Label(self,bg="white")
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.big_font=font.Font(self, family='Arial', size=50)
        self.normal_font=font.Font(self, family='Arial', size=12)

        self.number_files = tk.IntVar()

#header
        self.label_header=tk.Label(self, text= 'VPP calculation tool',font=self.big_font,bg='white', anchor='nw')
        self.label_header.place(relx=0.05, rely=0.05, relwidth=1, relheight=0.15)
#how many files
        self.label_number_files=tk.Label(self, text= 'Kinematic and kinetic data are saved in ',font=self.normal_font,bg='white', anchor='nw')
        self.label_number_files.place(relx=0.1, rely=0.3, relwidth=0.7, relheight=0.05)
        self.radio_number_files_1=tk.Radiobutton(self, text="one file", variable=self.number_files, value =1, font=self.normal_font, anchor='w',bg='white', activeforeground="dim gray")
        self.radio_number_files_2=tk.Radiobutton(self, text="two separate files", variable=self.number_files, value =2, font=self.normal_font, anchor='w',bg='white', activeforeground="dim gray")
        self.radio_number_files_1.place(relx=0.5, rely=0.3, relwidth=0.2, relheight=0.05)
        self.radio_number_files_2.place(relx=0.65, rely=0.3, relwidth=0.25, relheight=0.05)
        self.radio_number_files_2.select()
#Button
        self.browseButton_ini=tk.Button(self, text='Load initialisation file...', bg='lightblue', fg='black', font=('helvetica', 12, 'bold'))
        self.browseButton_ini.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)
        #all in one data file
        self.browseButton_data=tk.Button(self, text='Load data files...', bg='blue', fg='white', font=('helvetica', 12, 'bold'))

        #two separate data files (the order of the files has to fit)
        self.browseButton_data_dyn=tk.Button(self, text='Load kinetic data files...', bg='blue', fg='white', font=('helvetica', 12, 'bold'))

        self.browseButton_data_kin=tk.Button(self, text='Load kinematic data files...', bg='blue', fg='white', font=('helvetica', 12, 'bold'))


        #option one file is shown on start page:
        # self.browseButton_data.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)

        #option two files is shown on start page:
        self.browseButton_data_dyn.place(relx=0.15, rely=0.5, relwidth=0.34, relheight=0.1)
        self.browseButton_data_kin.place(relx=0.5, rely=0.5, relwidth=0.35, relheight=0.1)

        self.button_forward =  tk.Button(self, text = ">>", font = self.normal_font,bd=1,bg = 'green', highlightbackground='black',activebackground="#e6e3e4")
        self.button_forward.place(relx = 0.9, rely = 0.9, relwidth=0.07, relheight=0.07)
#-------------------------------------------------------------------------
#general information (kinetic data)
class PageKinetic(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.background=tk.Label(self,bg="white")
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.big_font=font.Font(self, family='Arial', size=25)
        self.normal_font=font.Font(self, family='Arial', size=12)
        self.container_1=tk.Frame(self, bg='white')
        self.container_1.place(relx=0, rely=0.5, relwidth=1, relheight=0.1)
        self.container_2=tk.Frame(self, bg='white')
        self.container_2.place(relx=0, rely=0.6, relwidth=1, relheight=0.1)
        self.container_3=tk.Frame(self, bg='white')
        self.container_3.place(relx=0, rely=0.7, relwidth=1, relheight=0.1)
        self.container_4=tk.Frame(self, bg='white')
        self.container_4.place(relx=0, rely=0.8, relwidth=1, relheight=0.1)

        self.frequ_grf=tk.IntVar()
        self.unit=tk.IntVar()
        self.nb_kmp=tk.IntVar()
        self.mass=tk.IntVar()
        self.fac_fx=tk.DoubleVar()
        self.fac_fz=tk.DoubleVar()

        #header
        self.label_header=tk.Label(self, text= '1. general information (kinetic data)',font=self.big_font,bg='white', anchor='nw')
        self.label_header.place(relx=0.05, rely=0.05, relwidth=1, relheight=0.15)
        #measurement frequency
        self.label_grf=tk.Label(self, text= 'sample frequency kinetic data in Hz (e.g. 1000 Hz):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_grf.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.05)
        self.entry_frequ_grf=tk.Entry(self, textvariable=self.frequ_grf, justify='left',font=("Arial", 14))

        self.entry_frequ_grf.place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.05)
        #unit CoP
        self.label_unit_cop=tk.Label(self, text= 'CoP measured in:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_unit_cop.place(relx=0.1, rely=0.25, relwidth=0.7, relheight=0.05)
        self.radio_unit_cop_mm=tk.Radiobutton(self, text="mm", variable=self.unit, value =1, font=self.normal_font, anchor='w',bg='lightgray', activeforeground="dim gray")
        self.radio_unit_cop_meter=tk.Radiobutton(self, text="m", variable=self.unit, value =0, font=self.normal_font, anchor='w',bg='lightgray', activeforeground="dim gray")
        self.radio_unit_cop_mm.place(relx=0.6, rely=0.25, relwidth=0.15, relheight=0.05)
        self.radio_unit_cop_meter.place(relx=0.75, rely=0.25, relwidth=0.15, relheight=0.05)
        self.radio_unit_cop_meter.select()

        #order and signs of kinetic data
        self.label_dyn=tk.Label(self, text= 'GRFx  \t \t GRFz \t \t CoPx',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_dyn.place(relx=0.3, rely=0.45, relwidth=0.6, relheight=0.05)

        #mass subject
        self.label_mass=tk.Label(self, text= 'mass of participant in N:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_mass.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.05)
        self.entry_mass=tk.Entry(self, textvariable=self.mass, justify='left',font=("Arial", 14))
        self.entry_mass.place(relx=0.65, rely=0.35, relwidth=0.1, relheight=0.05)

        #1st
        self.col_fx1=tk.IntVar()
        self.col_fz1=tk.IntVar()
        self.col_copx1=tk.IntVar()
        self.pm_fx1=tk.StringVar()
        self.pm_fz1=tk.StringVar()
        self.pm_copx1=tk.StringVar()


        self.label_fp_1=tk.Label(self.container_1, text= 'Force Plate 1:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_fp_1.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_fx1=tk.Entry(self.container_1, textvariable=self.col_fx1, justify='center',font=("Arial", 14))
        self.entry_fx1.place(relx=0.35, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_fz1=tk.Entry(self.container_1, textvariable=self.col_fz1, justify='center',font=("Arial", 14))
        self.entry_fz1.place(relx=0.55, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_copx1=tk.Entry(self.container_1, textvariable=self.col_copx1, justify='center',font=("Arial", 14))
        self.entry_copx1.place(relx=0.75, rely=0, relwidth=0.05, relheight=0.5)

        self.combo_pm_fx1=ttk.Combobox(self.container_1, textvariable=self.pm_fx1, font=("Arial", 14))
        self.combo_pm_fx1['values']=('+', '-')
        self.combo_pm_fx1.current(0) # "+" = 0 as standard
        self.combo_pm_fx1.place(relx=0.3, rely=0, relwidth=0.05, relheight=0.5)
        self.combo_pm_fz1=ttk.Combobox(self.container_1, textvariable=self.pm_fz1, font=("Arial", 14))
        self.combo_pm_fz1['values']=('+', '-')
        self.combo_pm_fz1.current(0)
        self.combo_pm_fz1.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.combo_pm_copx1=ttk.Combobox(self.container_1, textvariable=self.pm_copx1, font=("Arial", 14))
        self.combo_pm_copx1['values']=('+', '-')
        self.combo_pm_copx1.current(0)
        self.combo_pm_copx1.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)

        #2nd
        self.col_fx2=tk.IntVar()
        self.col_fz2=tk.IntVar()
        self.col_copx2=tk.IntVar()
        self.pm_fx2=tk.StringVar()
        self.pm_fz2=tk.StringVar()
        self.pm_copx2=tk.StringVar()

        self.label_fp_2=tk.Label(self.container_2, text= 'Force Plate 2:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_fp_2.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_fx2=tk.Entry(self.container_2, textvariable=self.col_fx2, justify='center',font=("Arial", 14))
        self.entry_fx2.place(relx=0.35, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_fz2=tk.Entry(self.container_2, textvariable=self.col_fz2, justify='center',font=("Arial", 14))
        self.entry_fz2.place(relx=0.55, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_copx2=tk.Entry(self.container_2, textvariable=self.col_copx2, justify='center',font=("Arial", 14))
        self.entry_copx2.place(relx=0.75, rely=0, relwidth=0.05, relheight=0.5)

        self.combo_pm_fx2=ttk.Combobox(self.container_2, textvariable=self.pm_fx2, font=("Arial", 14))
        self.combo_pm_fx2['values']=('+', '-')
        self.combo_pm_fx2.current(0)
        self.combo_pm_fx2.place(relx=0.3, rely=0, relwidth=0.05, relheight=0.5)
        self.combo_pm_fz2=ttk.Combobox(self.container_2, textvariable=self.pm_fz2, font=("Arial", 14))
        self.combo_pm_fz2['values']=('+', '-')
        self.combo_pm_fz2.current(0)
        self.combo_pm_fz2.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.combo_pm_copx2=ttk.Combobox(self.container_2, textvariable=self.pm_copx2, font=("Arial", 14))
        self.combo_pm_copx2['values']=('+', '-')
        self.combo_pm_copx2.current(0)
        self.combo_pm_copx2.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)

        #3rd
        self.col_fx3=tk.IntVar()
        self.col_fz3=tk.IntVar()
        self.col_copx3=tk.IntVar()
        self.pm_fx3=tk.StringVar()
        self.pm_fz3=tk.StringVar()
        self.pm_copx3=tk.StringVar()

        self.label_fp_3=tk.Label(self.container_3, text= 'Force Plate 3:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_fp_3.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_fx3=tk.Entry(self.container_3, textvariable=self.col_fx3, justify='center',font=("Arial", 14))
        self.entry_fx3.place(relx=0.35, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_fz3=tk.Entry(self.container_3, textvariable=self.col_fz3, justify='center',font=("Arial", 14))
        self.entry_fz3.place(relx=0.55, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_copx3=tk.Entry(self.container_3, textvariable=self.col_copx3, justify='center',font=("Arial", 14))
        self.entry_copx3.place(relx=0.75, rely=0, relwidth=0.05, relheight=0.5)

        self.combo_pm_fx3=ttk.Combobox(self.container_3, textvariable=self.pm_fx3, font=("Arial", 14))
        self.combo_pm_fx3['values']=('+', '-')
        self.combo_pm_fx3.current(0)
        self.combo_pm_fx3.place(relx=0.3, rely=0, relwidth=0.05, relheight=0.5)
        self.combo_pm_fz3=ttk.Combobox(self.container_3, textvariable=self.pm_fz3, font=("Arial", 14))
        self.combo_pm_fz3['values']=('+', '-')
        self.combo_pm_fz3.current(0)
        self.combo_pm_fz3.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.combo_pm_copx3=ttk.Combobox(self.container_3, textvariable=self.pm_copx3, font=("Arial", 14))
        self.combo_pm_copx3['values']=('+', '-')
        self.combo_pm_copx3.current(0)
        self.combo_pm_copx3.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)


        self.button_forward =  tk.Button(self, text = ">>", font = self.normal_font,bd=1,bg = 'green', highlightbackground='black',activebackground="#e6e3e4")
        self.button_forward.place(relx = 0.9, rely = 0.9, relwidth=0.07, relheight=0.07)
        self.button_back =  tk.Button(self, text = "<<", font = self.normal_font,bd=1,bg = 'green', highlightbackground='black',activebackground="#e6e3e4")
        self.button_back.place(relx = 0.03, rely = 0.9, relwidth=0.07, relheight=0.07)

        #factor forces
        self.label_factor_Fx=tk.Label(self, text= 'Factor GRFx:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_factor_Fx.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.05)
        self.entry_factor_Fx=tk.Entry(self, textvariable=self.fac_fx, justify='left',font=("Arial", 14))
        self.entry_factor_Fx.place(relx=0.3, rely=0.85, relwidth=0.1, relheight=0.05)
        self.fac_fx.set(1.0)
        self.label_factor_Fz=tk.Label(self, text= 'Factor GRFz:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_factor_Fz.place(relx=0.5, rely=0.85, relwidth=0.3, relheight=0.05)
        self.entry_factor_Fz=tk.Entry(self, textvariable=self.fac_fz, justify='left',font=("Arial", 14))
        self.entry_factor_Fz.place(relx=0.7, rely=0.85, relwidth=0.1, relheight=0.05)
        self.fac_fz.set(1.0)
#-------------------------------------------------------------------------
#general information (kinematic data)
class PageKinematic1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.background=tk.Label(self,bg="white")
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.big_font=font.Font(self, family='Arial', size=25)
        self.normal_font=font.Font(self, family='Arial', size=12)

        self.frequ_video=tk.IntVar()
        self.frequ_cut=tk.IntVar()
        self.unit=tk.IntVar()

        #header
        self.label_header=tk.Label(self, text= '2. general information (kinematic data)',font=self.big_font,bg='white', anchor='nw')
        self.label_header.place(relx=0.05, rely=0.05, relwidth=1, relheight=0.15)
        #sample frequency
        self.label_video=tk.Label(self, text= 'sample frequency kinematics in Hz (e.g. 200 Hz):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_video.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.05)
        self.entry_frequ_video=tk.Entry(self, textvariable=self.frequ_video, justify='left',font=("Arial", 14))
        self.entry_frequ_video.place(relx=0.65, rely=0.15, relwidth=0.1, relheight=0.05)
        #cutoff frequency
        self.label_frequ_cut=tk.Label(self, text= 'cut-off frequency kinematics in Hz (e.g. 50 Hz):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_frequ_cut.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.05)
        self.entry_frequ_cut=tk.Entry(self, textvariable=self.frequ_cut, justify='left',font=("Arial", 14))
        self.entry_frequ_cut.place(relx=0.65, rely=0.25, relwidth=0.1, relheight=0.05)
        #unit data
        self.label_unit=tk.Label(self, text= 'data measured in:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_unit.place(relx=0.1, rely=0.35, relwidth=0.7, relheight=0.05)
        radio_unit_mm=tk.Radiobutton(self, text="mm", variable=self.unit, value =1, font=self.normal_font, anchor='w',bg='lightgray', activeforeground="dim gray")
        radio_unit_meter=tk.Radiobutton(self, text="m", variable=self.unit, value =0, font=self.normal_font, anchor='w',bg='lightgray', activeforeground="dim gray")
        radio_unit_mm.place(relx=0.6, rely=0.35, relwidth=0.15, relheight=0.05)
        radio_unit_meter.place(relx=0.75, rely=0.35, relwidth=0.15, relheight=0.05)
        radio_unit_mm.select()
        #button
        self.button_forward =  tk.Button(self, text = ">>", font = self.normal_font,bd=1,bg = 'green', highlightbackground='black',activebackground="#e6e3e4")
        self.button_forward.place(relx = 0.9, rely = 0.9, relwidth=0.07, relheight=0.07)
        self.button_back =  tk.Button(self, text = "<<", font = self.normal_font,bd=1,bg = 'green', highlightbackground='black',activebackground="#e6e3e4")
        self.button_back.place(relx = 0.03, rely = 0.9, relwidth=0.07, relheight=0.07)
#-------------------------------------------------------------------------
        #marker setup (kinematic data)
class PageKinematic2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.background=tk.Label(self,bg="white")
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.big_font=font.Font(self, family='Arial', size=25)
        self.normal_font=font.Font(self, family='Arial', size=12)

        self.container_1=tk.Frame(self, bg='white')
        self.container_1.place(relx=0, rely=0.225, relwidth=1, relheight=0.1)
        self.container_2=tk.Frame(self, bg='white')
        self.container_2.place(relx=0, rely=0.3, relwidth=1, relheight=0.1)
        self.container_3=tk.Frame(self, bg='white')
        self.container_3.place(relx=0, rely=0.375, relwidth=1, relheight=0.1)
        self.container_4=tk.Frame(self, bg='white')
        self.container_4.place(relx=0, rely=0.45, relwidth=1, relheight=0.1)
        self.container_5=tk.Frame(self, bg='white')
        self.container_5.place(relx=0, rely=0.525, relwidth=1, relheight=0.1)
        self.container_6=tk.Frame(self, bg='white')
        self.container_6.place(relx=0, rely=0.6, relwidth=1, relheight=0.1)
        self.container_7=tk.Frame(self, bg='white')
        self.container_7.place(relx=0, rely=0.675, relwidth=1, relheight=0.1)
        self.container_8=tk.Frame(self, bg='white')
        self.container_8.place(relx=0, rely=0.75, relwidth=1, relheight=0.1)


        #header
        self.label_header=tk.Label(self, text= '3. marker setup (kinematic data)',font=self.big_font,bg='white', anchor='nw')
        self.label_header.place(relx=0.05, rely=0.05, relwidth=1, relheight=0.15)
        self.label_marker=tk.Label(self, text= 'left:  \t x \t z \t right: \t x \t z',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_marker.place(relx=0.3, rely=0.15, relwidth=0.6, relheight=0.05)

        #mal lat
        self.mal_lat_lx=tk.IntVar()
        self.mal_lat_lz=tk.IntVar()
        self.mal_lat_rx=tk.IntVar()
        self.mal_lat_rz=tk.IntVar()
        self.label_mal_lat=tk.Label(self.container_1, text= 'malleolus lateralis:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_mal_lat.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_mal_lat_lx=tk.Entry(self.container_1, textvariable=self.mal_lat_lx, justify='center',font=("Arial", 14))
        self.entry_mal_lat_lx.place(relx=0.4, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_mal_lat_lz=tk.Entry(self.container_1, textvariable=self.mal_lat_lz, justify='center',font=("Arial", 14))
        self.entry_mal_lat_lz.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_mal_lat_rx=tk.Entry(self.container_1, textvariable=self.mal_lat_rx, justify='center',font=("Arial", 14))
        self.entry_mal_lat_rx.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_mal_lat_rz=tk.Entry(self.container_1, textvariable=self.mal_lat_rz, justify='center',font=("Arial", 14))
        self.entry_mal_lat_rz.place(relx=0.8, rely=0, relwidth=0.05, relheight=0.5)

        #mal med
        self.mal_med_lx=tk.IntVar()
        self.mal_med_lz=tk.IntVar()
        self.mal_med_rx=tk.IntVar()
        self.mal_med_rz=tk.IntVar()
        self.label_mal_med=tk.Label(self.container_2, text= 'malleolus medialis:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_mal_med.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_mal_med_lx=tk.Entry(self.container_2, textvariable=self.mal_med_lx, justify='center',font=("Arial", 14))
        self.entry_mal_med_lx.place(relx=0.4, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_mal_med_lz=tk.Entry(self.container_2, textvariable=self.mal_med_lz, justify='center',font=("Arial", 14))
        self.entry_mal_med_lz.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_mal_med_rx=tk.Entry(self.container_2, textvariable=self.mal_med_rx, justify='center',font=("Arial", 14))
        self.entry_mal_med_rx.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_mal_med_rz=tk.Entry(self.container_2, textvariable=self.mal_med_rz, justify='center',font=("Arial", 14))
        self.entry_mal_med_rz.place(relx=0.8, rely=0, relwidth=0.05, relheight=0.5)

        #toe
        self.toe_lx=tk.IntVar()
        self.toe_lz=tk.IntVar()
        self.toe_rx=tk.IntVar()
        self.toe_rz=tk.IntVar()
        self.label_toe=tk.Label(self.container_3, text= 'toe:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_toe.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_toe_lx=tk.Entry(self.container_3, textvariable=self.toe_lx, justify='center',font=("Arial", 14))
        self.entry_toe_lx.place(relx=0.4, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_toe_lz=tk.Entry(self.container_3, textvariable=self.toe_lz, justify='center',font=("Arial", 14))
        self.entry_toe_lz.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_toe_rx=tk.Entry(self.container_3, textvariable=self.toe_rx, justify='center',font=("Arial", 14))
        self.entry_toe_rx.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_toe_rz=tk.Entry(self.container_3, textvariable=self.toe_rz, justify='center',font=("Arial", 14))
        self.entry_toe_rz.place(relx=0.8, rely=0, relwidth=0.05, relheight=0.5)

        #knee
        self.knee_lx=tk.IntVar()
        self.knee_lz=tk.IntVar()
        self.knee_rx=tk.IntVar()
        self.knee_rz=tk.IntVar()
        self.label_knee=tk.Label(self.container_4, text= 'knee:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_knee.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_knee_lx=tk.Entry(self.container_4, textvariable=self.knee_lx, justify='center',font=("Arial", 14))
        self.entry_knee_lx.place(relx=0.4, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_knee_lz=tk.Entry(self.container_4, textvariable=self.knee_lz, justify='center',font=("Arial", 14))
        self.entry_knee_lz.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_knee_rx=tk.Entry(self.container_4, textvariable=self.knee_rx, justify='center',font=("Arial", 14))
        self.entry_knee_rx.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_knee_rz=tk.Entry(self.container_4, textvariable=self.knee_rz, justify='center',font=("Arial", 14))
        self.entry_knee_rz.place(relx=0.8, rely=0, relwidth=0.05, relheight=0.5)

        #hip
        self.hip_lx=tk.IntVar()
        self.hip_lz=tk.IntVar()
        self.hip_rx=tk.IntVar()
        self.hip_rz=tk.IntVar()
        self.label_hip=tk.Label(self.container_5, text= 'trochanter major (hip):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_hip.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_hip_lx=tk.Entry(self.container_5, textvariable=self.hip_lx, justify='center',font=("Arial", 14))
        self.entry_hip_lx.place(relx=0.4, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_hip_lz=tk.Entry(self.container_5, textvariable=self.hip_lz, justify='center',font=("Arial", 14))
        self.entry_hip_lz.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_hip_rx=tk.Entry(self.container_5, textvariable=self.hip_rx, justify='center',font=("Arial", 14))
        self.entry_hip_rx.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_hip_rz=tk.Entry(self.container_5, textvariable=self.hip_rz, justify='center',font=("Arial", 14))
        self.entry_hip_rz.place(relx=0.8, rely=0, relwidth=0.05, relheight=0.5)

        #shoulder
        self.shoulder_lx=tk.IntVar()
        self.shoulder_lz=tk.IntVar()
        self.shoulder_rx=tk.IntVar()
        self.shoulder_rz=tk.IntVar()
        self.label_shoulder=tk.Label(self.container_6, text= 'acromion (shoulder):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_shoulder.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.5)
        self.entry_shoulder_lx=tk.Entry(self.container_6, textvariable=self.shoulder_lx, justify='center',font=("Arial", 14))
        self.entry_shoulder_lx.place(relx=0.4, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_shoulder_lz=tk.Entry(self.container_6, textvariable=self.shoulder_lz, justify='center',font=("Arial", 14))
        self.entry_shoulder_lz.place(relx=0.5, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_shoulder_rx=tk.Entry(self.container_6, textvariable=self.shoulder_rx, justify='center',font=("Arial", 14))
        self.entry_shoulder_rx.place(relx=0.7, rely=0, relwidth=0.05, relheight=0.5)
        self.entry_shoulder_rz=tk.Entry(self.container_6, textvariable=self.shoulder_rz, justify='center',font=("Arial", 14))
        self.entry_shoulder_rz.place(relx=0.8, rely=0, relwidth=0.05, relheight=0.5)

        #button
        self.button_forward =  tk.Button(self, text = ">>", font = self.normal_font,bd=1,bg = 'green', highlightbackground='black',activebackground="#e6e3e4")
        self.button_forward.place(relx = 0.9, rely = 0.9, relwidth=0.07, relheight=0.07)
        self.button_back =  tk.Button(self, text = "<<", font = self.normal_font,bd=1,bg = 'green', highlightbackground='black',activebackground="#e6e3e4")
        self.button_back.place(relx = 0.03, rely = 0.9, relwidth=0.07, relheight=0.07)
#---------------------------------------------------------------------------------
# Read in files
class PageReadin(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.background=tk.Label(self,bg="white")
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.big_font=font.Font(self, family='Arial', size=25)
        self.normal_font=font.Font(self, family='Arial', size=12)

#Variables
        self.keyword_dyn=tk.StringVar()
        self.keyword_kin=tk.StringVar()
        self.dist_keyword_dyn=tk.IntVar()
        self.dist_keyword_dyn_end=tk.IntVar()
        self.dist_keyword_kin=tk.IntVar()
#Label
        #header
        self.label_header=tk.Label(self, text= '4. read in data',font=self.big_font,bg='white', anchor='nw')
        self.label_header.place(relx=0.05, rely=0.05, relwidth=1, relheight=0.15)

        self.label_keyword_dyn=tk.Label(self, text= 'key word in header kinetics (e.g. \'Devices\'):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_keyword_dyn.place(relx=0.05, rely=0.3, relwidth=0.7, relheight=0.05)
        self.label_dist_keyword_dyn=tk.Label(self, text= 'distance (rows) from keyword kinetics to data (e.g. 5 rows):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_dist_keyword_dyn.place(relx=0.05, rely=0.4, relwidth=0.7, relheight=0.05)
        self.label_dist_keyword_dyn=tk.Label(self, text= 'distance (rows) from keyword kinematics to end kinetic data:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_dist_keyword_dyn.place(relx=0.05, rely=0.5, relwidth=0.7, relheight=0.05)
        self.label_keyword_kin=tk.Label(self, text= 'key word in header kinematics (e.g. \'Trajectories\'):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_keyword_kin.place(relx=0.05, rely=0.6, relwidth=0.7, relheight=0.05)
        self.label_dist_keyword_kin=tk.Label(self, text= 'distance (rows) from keyword kinematics to data:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_dist_keyword_kin.place(relx=0.05, rely=0.7, relwidth=0.7, relheight=0.05)
        
#Entry
        self.entry_keyword_dyn=tk.Entry(self, textvariable=self.keyword_dyn, justify='left',font=("Arial", 14))
        self.entry_keyword_dyn.place(relx=0.7, rely=0.3, relwidth=0.2, relheight=0.05)
        self.entry_keyword_kin=tk.Entry(self, textvariable=self.keyword_kin, justify='left',font=("Arial", 14))
        self.entry_keyword_kin.place(relx=0.7, rely=0.6, relwidth=0.2, relheight=0.05)
#Combobox (to choose from given entries)        
        self.combo_dist_keyword_dyn=ttk.Combobox(self, textvariable=self.dist_keyword_dyn, font=("Arial", 14))
        self.combo_dist_keyword_dyn['values']=('1', '2', '3', '4', '5', '6', '7','8','9','10')
        self.combo_dist_keyword_dyn.current(0)
        self.combo_dist_keyword_dyn.place(relx=0.7, rely=0.4, relwidth=0.2, relheight=0.05)
        self.combo_dist_keyword_dyn_end=ttk.Combobox(self, textvariable=self.dist_keyword_dyn_end, font=("Arial", 14))
        self.combo_dist_keyword_dyn_end['values']=('1', '2', '3', '4', '5', '6', '7','8','9','10')
        self.combo_dist_keyword_dyn_end.current(0)
        self.combo_dist_keyword_dyn_end.place(relx=0.7, rely=0.5, relwidth=0.2, relheight=0.05)
        self.combo_dist_keyword_kin=ttk.Combobox(self, textvariable=self.dist_keyword_kin, font=("Arial", 14))
        self.combo_dist_keyword_kin['values']=('1', '2', '3', '4', '5', '6', '7','8','9','10')
        self.combo_dist_keyword_kin.current(0)
        self.combo_dist_keyword_kin.place(relx=0.7, rely=0.7, relwidth=0.2, relheight=0.05)

#Button
        self.button_calc= tk.Button(self, text="calculate VPP", font=self.normal_font,bd=1,bg='white', highlightbackground='black', highlightcolor='navajowhite',activebackground="#e6e3e4")
        self.button_calc.place(relx=0.77, rely=0.9, relwidth=0.2, relheight=0.07)

        self.button_back =  tk.Button(self, text = "<<", font = self.normal_font,bd=1,bg = 'green', highlightbackground='black',activebackground="#e6e3e4")
        self.button_back.place(relx = 0.03, rely = 0.9, relwidth=0.07, relheight=0.07)
#--------------------------------------------------------
#Show Results
class PageResults(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.background=tk.Label(self,bg="white")
        self.background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.big_font=font.Font(self, family='Arial', size=25)
        self.normal_font=font.Font(self, family='Arial', size=12)
        self.container_1=tk.Frame(self, bg='white')
        self.container_1.place(relx=0, rely=0.2, relwidth=0.4, relheight=1)

#Variable
        self.VPPx1=tk.DoubleVar()
        self.VPPz1=tk.DoubleVar()
        self.R2_1=tk.DoubleVar()

#Label
#header
        self.label_header=tk.Label(self, text= '5. results',font=self.big_font,bg='white', anchor='nw')
        self.label_header.place(relx=0.05, rely=0.05, relwidth=1, relheight=0.15)
#general
        self.label_file=tk.Label(self.container_1,font=self.normal_font,bg='lightblue', anchor='nw')
        self.label_file.place(relx=0.05, rely=0, relwidth=0.35, relheight=0.05)
        self.label_VPPx=tk.Label(self.container_1, text= 'VPPx (m):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_VPPx.place(relx=0.05, rely=0.1, relwidth=0.35, relheight=0.05)
        self.label_VPPz=tk.Label(self.container_1, text= 'VPPz (m):',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_VPPz.place(relx=0.05, rely=0.2, relwidth=0.35, relheight=0.05)
        self.label_R2=tk.Label(self.container_1, text= 'R²:',font=self.normal_font,bg='lightgray', anchor='nw')
        self.label_R2.place(relx=0.05, rely=0.3, relwidth=0.35, relheight=0.05)


        self.label_fp1=tk.Label(self.container_1, text= 'Force Plate 2',font=self.normal_font,bg='lightgray', anchor='center')
        self.label_fp1.place(relx=0.52, rely=0.0, relwidth=0.45, relheight=0.05)

#VPP values

        self.l_VPPx1=tk.Label(self.container_1, font=self.normal_font,bg='lightgray', anchor='center')
        self.l_VPPx1.place(relx=0.52, rely=0.1, relwidth=0.45, relheight=0.05)
        self.l_VPPz1=tk.Label(self.container_1, textvariable= self.VPPz1,font=self.normal_font,bg='lightgray', anchor='center')
        self.l_VPPz1.place(relx=0.52, rely=0.2, relwidth=0.45, relheight=0.05)
        self.l_R2_1=tk.Label(self.container_1, textvariable= self.R2_1,font=self.normal_font,bg='lightgray', anchor='center')
        self.l_R2_1.place(relx=0.52, rely=0.3, relwidth=0.45, relheight=0.05)

#Button
        self.button_prev =  tk.Button(self.container_1, text = "<< prev", font = self.normal_font,bd=1,bg = 'lightblue', highlightbackground='black',activebackground="#e6e3e4")
        self.button_prev.place(relx=0.05, rely=0.4, relwidth=0.25, relheight=0.07)
        self.button_next =  tk.Button(self.container_1, text = "next >>", font = self.normal_font,bd=1,bg = 'lightblue', highlightbackground='black',activebackground="#e6e3e4")
        self.button_next.place(relx=0.73, rely=0.4, relwidth=0.25, relheight=0.07)

        self.button_save_fig =  tk.Button(self.container_1, text = "save all figures", font = self.normal_font,bd=1,bg = 'blue',fg='white', highlightbackground='black',activebackground="#e6e3e4")
        self.button_save_fig.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.07)

#-------------------------------------------------------------------
#------------------MainView-----------------------------------------
#-------------------------------------------------------------------

class MainView(tk.Frame):
    def __init__(self,*args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.normal_font=font.Font(self, family='Arial', size=12)
        self.label_font=font.Font(self, family='Arial', size=30)
        self.entry_font=font.Font(self, family='Arial', size=40)

#-------------------------------------------------------------------------
        pstart=PageStart(self)
        pkinetic=PageKinetic(self)
        pkinematic1=PageKinematic1(self)
        pkinematic2=PageKinematic2(self)
        preadin=PageReadin(self)
        pres=PageResults(self)

        container=tk.Frame(self)
        container.place(relx=0, rely=0, relwidth=1, relheight=1)

        pstart.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pkinetic.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pkinematic1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pkinematic2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        preadin.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pres.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

#---------------------------------------------------------
        def show_one_file(*args):
            pstart.browseButton_data_dyn.place_forget()
            pstart.browseButton_data_kin.place_forget()
            pstart.browseButton_data.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)
            pstart.lift()

        def show_two_files(*args):
            pstart.browseButton_data.place_forget()
            #two separate data files (the order of the files has to fit):
            pstart.browseButton_data_dyn.place(relx=0.15, rely=0.5, relwidth=0.34, relheight=0.1)
            pstart.browseButton_data_kin.place(relx=0.5, rely=0.5, relwidth=0.35, relheight=0.1)
            pstart.lift()
            preadin.label_dist_keyword_dyn.place_forget()
            preadin.combo_dist_keyword_dyn_end.place_forget()

        pstart.radio_number_files_1['command']=show_one_file
        pstart.radio_number_files_2['command']=show_two_files
    #----------------
        # def show_fp_1(*args):
        #     pkinetic.container_2.place_forget()
        #     pkinetic.container_3.place_forget()
        #     pkinetic.container_4.place_forget()
        #     pkinetic.lift()

        # def show_fp_2(*args):
        #     pkinetic.container_2.place(relx=0, rely=0.6, relwidth=1, relheight=0.1)
        #     pkinetic.container_3.place_forget()
        #     pkinetic.container_4.place_forget()
        #     pkinetic.lift()

        def show_fp_3(*args):
            pkinetic.container_2.place(relx=0, rely=0.6, relwidth=1, relheight=0.1)
            pkinetic.container_3.place(relx=0, rely=0.7, relwidth=1, relheight=0.1)
            pkinetic.container_4.place_forget()
            pkinetic.lift()

        # def show_fp_4(*args):
        #     pkinetic.container_2.place(relx=0, rely=0.6, relwidth=1, relheight=0.1)
        #     pkinetic.container_3.place(relx=0, rely=0.7, relwidth=1, relheight=0.1)
        #     pkinetic.container_4.place(relx=0, rely=0.8, relwidth=1, relheight=0.1)
        #     pkinetic.lift()

        show_fp_3()

# function of green buttons with arrows:
        pstart.button_forward['command']=pkinetic.lift
        pkinetic.button_back['command']=pstart.lift
        pkinetic.button_forward['command']=pkinematic1.lift
        pkinematic1.button_forward['command']=pkinematic2.lift
        pkinematic2.button_forward['command']=preadin.lift
        pkinematic1.button_back['command']=pkinetic.lift
        pkinematic2.button_back['command']=pkinematic1.lift
        preadin.button_back['command']=pkinematic2.lift

        pstart.lift() #Start
#----------------------------------------

#read in data

    #read in initialization file:
        def readIni ():
            #initialisation
            ini_file=filedialog.askopenfilename()
            # ini_file = "VPPdata.ini"
            config = configparser.ConfigParser()
            config.read(ini_file)

            pkinetic.frequ_grf.set(config.get("KINETICS", 'frequ_grf'))
            pkinetic.mass.set(config.get("KINETICS", 'mass'))
            pkinetic.unit.set(config.get("KINETICS", 'unit_cop'))
            pkinetic.col_fx1.set(config.get("KINETICS", 'col_fx1'))
            pkinetic.col_fz1.set(config.get("KINETICS", 'col_fz1'))
            pkinetic.col_copx1.set(config.get("KINETICS", 'col_copx1'))
            pkinetic.col_fx2.set(config.get("KINETICS", 'col_fx2'))
            pkinetic.col_fz2.set(config.get("KINETICS", 'col_fz2'))
            pkinetic.col_copx2.set(config.get("KINETICS", 'col_copx2'))
            pkinetic.col_fx3.set(config.get("KINETICS", 'col_fx3'))
            pkinetic.col_fz3.set(config.get("KINETICS", 'col_fz3'))
            pkinetic.col_copx3.set(config.get("KINETICS", 'col_copx3'))
            pkinetic.fac_fx.set(config.get("KINETICS", 'fac_fx'))
            pkinetic.fac_fz.set(config.get("KINETICS", 'fac_fz'))

            pkinetic.combo_pm_fx1.set(config.get("KINETICS", 'pm_fx1'))
            pkinetic.combo_pm_fz1.set(config.get("KINETICS", 'pm_fz1'))
            pkinetic.combo_pm_fx2.set(config.get("KINETICS", 'pm_fx2'))
            pkinetic.combo_pm_fz2.set(config.get("KINETICS", 'pm_fz2'))
            pkinetic.combo_pm_fx3.set(config.get("KINETICS", 'pm_fx3'))
            pkinetic.combo_pm_fz3.set(config.get("KINETICS", 'pm_fz3'))
            pkinetic.combo_pm_copx2.set(config.get("KINETICS", 'pm_copx2'))

            pkinematic1.frequ_video.set(config.get("KINEMATICS", 'frequ_video'))
            pkinematic1.frequ_cut.set(config.get("KINEMATICS", 'frequ_cut'))

            pkinematic2.mal_lat_lx.set(config.get("KINEMATICS", 'mal_lat_lx'))
            pkinematic2.mal_lat_lz.set(config.get("KINEMATICS", 'mal_lat_lz'))
            pkinematic2.mal_lat_rx.set(config.get("KINEMATICS", 'mal_lat_rx'))
            pkinematic2.mal_lat_rz.set(config.get("KINEMATICS", 'mal_lat_rz'))
            pkinematic2.mal_med_lx.set(config.get("KINEMATICS", 'mal_med_lx'))
            pkinematic2.mal_med_lz.set(config.get("KINEMATICS", 'mal_med_lz'))
            pkinematic2.mal_med_rx.set(config.get("KINEMATICS", 'mal_med_rx'))
            pkinematic2.mal_med_rz.set(config.get("KINEMATICS", 'mal_med_rz'))
            pkinematic2.toe_lx.set(config.get("KINEMATICS", 'toe_lx'))
            pkinematic2.toe_lz.set(config.get("KINEMATICS", 'toe_lz'))
            pkinematic2.toe_rx.set(config.get("KINEMATICS", 'toe_rx'))
            pkinematic2.toe_rz.set(config.get("KINEMATICS", 'toe_rz'))
            pkinematic2.knee_lx.set(config.get("KINEMATICS", 'knee_lx'))
            pkinematic2.knee_lz.set(config.get("KINEMATICS", 'knee_lz'))
            pkinematic2.knee_rx.set(config.get("KINEMATICS", 'knee_rx'))
            pkinematic2.knee_rz.set(config.get("KINEMATICS", 'knee_rz'))
            pkinematic2.hip_lx.set(config.get("KINEMATICS", 'hip_lx'))
            pkinematic2.hip_lz.set(config.get("KINEMATICS", 'hip_lz'))
            pkinematic2.hip_rx.set(config.get("KINEMATICS", 'hip_rx'))
            pkinematic2.hip_rz.set(config.get("KINEMATICS", 'hip_rz'))
            pkinematic2.shoulder_lx.set(config.get("KINEMATICS", 'shoulder_lx'))
            pkinematic2.shoulder_lz.set(config.get("KINEMATICS", 'shoulder_lz'))
            pkinematic2.shoulder_rx.set(config.get("KINEMATICS", 'shoulder_rx'))
            pkinematic2.shoulder_rz.set(config.get("KINEMATICS", 'shoulder_rz'))

            preadin.keyword_dyn.set(config.get("READIN", 'keyword_dyn'))
            preadin.keyword_kin.set(config.get("READIN", 'keyword_kin'))
            preadin.combo_dist_keyword_dyn.set(config.get("READIN", 'dist_keyword_dyn'))
            preadin.combo_dist_keyword_kin.set(config.get("READIN", 'dist_keyword_kin'))

        self.ListeFiles=[]
        self.ListeFiles_kin=[]

        #if only one file: kinematic and kinetic, if two files: kinetic (dyn):
        def readData (): #dyn
            self.file=filedialog.askopenfilenames()
        #if pstart.number_files == 2:
        def readData_kin ():
            self.file_kin=filedialog.askopenfilenames()
            show_two_files()

        def getData (): #initialization
            #read in all entries:
            calcInput.button_get_entries(pkinetic,preadin,pkinematic1,pkinematic2)
            #calculate kin data
            if pstart.number_files.get() == 2: #additionally data kin
                import_file_path_kin = self.file_kin
            import_file_path = self.file
            directory = os.path.split(import_file_path[0])[0]
            foldername = directory.split('/')[-1]
            for k in range(0,len(import_file_path)): #read in for each file
                if pstart.number_files == 1:
                    load_data(import_file_path,k)
                else:
                    load_data_dyn(import_file_path,k)
                    load_data_kin(import_file_path_kin,k)
                    self.ListeFiles_kin.append(import_file_path_kin[k])
                button_res(os.path.basename(import_file_path[k])[0:-4],foldername,k,0)
                self.ListeFiles.append(import_file_path[k])
            #initialisation gui page
            if pstart.number_files == 1:
                load_data(import_file_path,0)
            else:
                load_data_dyn(import_file_path,0)
                load_data_kin(import_file_path_kin,0)
            button_res_single(os.path.basename(import_file_path[0])[0:-4])

#----------------------------------------------         
#calc VPP and show result page
        self.ListeVPP=[0]
        self.ListeVPP[0]=['name of kinetic file','Force plate number' '\t' 'VPPx (m)' '\t'  'VPPz (m)' '\t' 'R^2']
        def button_res(file_name,foldername,k,p):
            COM=calcCoM.Com_calc(pres.DataKin, pkinematic2.Mal_lat, pkinematic2.Mal_med, pkinematic2.Toe, pkinematic2.Knee, pkinematic2.Hip, pkinematic2.Shoulder,preadin)

            VPP_init=[0, 0.2]
            for index in range(0,preadin.Nb_kmp):
                #change kinetic data to the same frequency as kinematic data:
                Fz_short = np.interp(np.linspace(1,len(pres.Fz),len(COM)),np.linspace(1,len(pres.Fz),len(pres.Fz)),pres.Fz[:,index])/preadin.Mass
                t = np.transpose(np.nonzero(Fz_short>0.05))
                if index == 0:
                    tdto = t[0] #TO_zero
                    tdto = np.append(tdto,t[-1],axis = 0)#end
                elif index == 1: #middle contact
                    #here VPP calculation
                    tdto = np.append(tdto,t[0],axis = 0) #TD1
                    tdto = np.append(tdto,t[-1],axis = 0) #TO1
                elif index == 2:
                    tdto = np.append(tdto,t[0],axis = 0) #TD2
                    tdto = np.append(tdto,t[-1],axis = 0)

            #calculate VPP for middle contact
            index = 1
            tdto = np.sort(tdto) #single support phase
             # change kinetic data to the same frequency as kinematic data:
            Fx_short = np.interp(np.linspace(1,len(pres.Fx),len(COM)),np.linspace(1,len(pres.Fx),len(pres.Fx)),pres.Fx[:,index])/preadin.Mass*preadin.Fac_fx
            Fz_short = np.interp(np.linspace(1,len(pres.Fz),len(COM)),np.linspace(1,len(pres.Fz),len(pres.Fz)),pres.Fz[:,index])/preadin.Mass*preadin.Fac_fz
            CoP_short = np.interp(np.linspace(1,len(pres.CoP),len(COM)),np.linspace(1,len(pres.CoP),len(pres.CoP)),pres.CoP[:,index])

            plot=p #p=0 for no plot and 2 for save plot
            #filter CoM:
            sos = butter(4, 50,  'lowpass', output='sos',fs = preadin.Frequ_video)
            CoM_filtx = np.transpose(np.array([signal.sosfiltfilt(sos, COM[tdto[2]:tdto[3],0])]))
            CoM_filt = np.append(CoM_filtx,np.transpose([signal.sosfiltfilt(sos, COM[tdto[2]:tdto[3],1])]), axis = 1)

            VPP_calc = calcVPP.VPP_calculation(CoP_short[tdto[2]:tdto[3]], CoM_filt, Fx_short[tdto[2]:tdto[3]], Fz_short[tdto[2]:tdto[3]], VPP_init,file_name)
            r_mod=calcVPP.R_mod(CoP_short[tdto[2]:tdto[3]], CoM_filt, Fx_short[tdto[2]:tdto[3]], Fz_short[tdto[2]:tdto[3]], VPP_calc, plot,file_name)
            self.ListeVPP.append([file_name,index+1 ,VPP_calc[0],VPP_calc[1],r_mod])
            calcInput.button_save_data(self.ListeVPP,foldername) #save in csv, name after foldername

        def button_res_single(file_name):
            COM=calcCoM.Com_calc(pres.DataKin, pkinematic2.Mal_lat, pkinematic2.Mal_med, pkinematic2.Toe, pkinematic2.Knee, pkinematic2.Hip, pkinematic2.Shoulder,preadin)

            VPP_init=[0, 0.2]
            for index in range(0,preadin.Nb_kmp):
                #change kinetic data to the same frequency as kinematic data:
                Fz_short = np.interp(np.linspace(1,len(pres.Fz),len(COM)),np.linspace(1,len(pres.Fz),len(pres.Fz)),pres.Fz[:,index])/preadin.Mass
                t = np.transpose(np.nonzero(Fz_short>0.05))
                if index == 0:
                    tdto = t[0] #TO_zero
                    tdto = np.append(tdto,t[-1],axis = 0)#end
                elif index == 1: #middle contact
                    #here VPP calculation
                    tdto = np.append(tdto,t[0],axis = 0) #TD1
                    tdto = np.append(tdto,t[-1],axis = 0) #TO1
                elif index == 2:
                    tdto = np.append(tdto,t[0],axis = 0) #TD2
                    tdto = np.append(tdto,t[-1],axis = 0)

            #calculate VPP for middle contact
            index = 1
            tdto = np.sort(tdto) #single support phase
             # change kinetic data to the same frequency as kinematic data:
            Fx_short = np.interp(np.linspace(1,len(pres.Fx),len(COM)),np.linspace(1,len(pres.Fx),len(pres.Fx)),pres.Fx[:,index])/preadin.Mass*preadin.Fac_fx
            Fz_short = np.interp(np.linspace(1,len(pres.Fz),len(COM)),np.linspace(1,len(pres.Fz),len(pres.Fz)),pres.Fz[:,index])/preadin.Mass*preadin.Fac_fz
            CoP_short = np.interp(np.linspace(1,len(pres.CoP),len(COM)),np.linspace(1,len(pres.CoP),len(pres.CoP)),pres.CoP[:,index])

            plot=1
            #filter CoM:
            sos = butter(4, 50,  'lowpass', output='sos',fs = preadin.Frequ_video)
            CoM_filtx = np.transpose(np.array([signal.sosfiltfilt(sos, COM[tdto[2]:tdto[3],0])]))
            CoM_filt = np.append(CoM_filtx,np.transpose([signal.sosfiltfilt(sos, COM[tdto[2]:tdto[3],1])]), axis = 1)

            VPP_calc = calcVPP.VPP_calculation(CoP_short[tdto[2]:tdto[3]], CoM_filt, Fx_short[tdto[2]:tdto[3]], Fz_short[tdto[2]:tdto[3]], VPP_init,file_name)
            r_mod=calcVPP.R_mod(CoP_short[tdto[2]:tdto[3]], CoM_filt, Fx_short[tdto[2]:tdto[3]], Fz_short[tdto[2]:tdto[3]], VPP_calc, plot,file_name)

            pres.VPPx1.set(np.round(VPP_calc[0],3))
            pres.VPPz1.set(np.round(VPP_calc[1],3))
            pres.R2_1.set(round(r_mod,3))
            pres.label_file['text'] = file_name
            pres.l_VPPx1['text'] = pres.VPPx1.get()
            pres.l_VPPz1['text'] = pres.VPPz1.get()
            pres.l_R2_1['text'] = pres.R2_1.get()

        def show_calc(*args):
            preadin.lower()
            pres.lift()
            calcVPP.plt.show()

        def show_calc1(*args):
            getData()
            show_calc()

        def load_data(import_file_path,k):
            with open(import_file_path[k]) as datatxt: #to find start and end of data
                lines=datatxt.readlines()
                for i in range(0,len(lines)):
                    l=(lines[i]).rstrip("\n").split("\t")
                    if str(l).find(preadin.Keyword_dyn) != -1: #kinetics: search entered keyword in data file
                        start_kinetics=i + preadin.Dist_keyword_dyn; #kinetics: search line of keyword + entered distance=start line of kinetic data
                    if str(l).find(preadin.Keyword_kin) != -1: #kinematics: search entered keyword in data file
                        end_kinetics=i - preadin.Dist_keyword_dyn_end;
                        start_kinematics=i + preadin.Dist_keyword_kin; #kinematics: search line of keyword + entered distance=start line of kinematic data
            DataDyn=np.loadtxt(import_file_path[k], skiprows=start_kinetics,  max_rows=end_kinetics - start_kinetics)
            pres.DataKin=np.genfromtxt(import_file_path[k],delimiter="\t",skip_header=start_kinematics)
            #if kinematic data were measured in mm, convert to meter:
            if (pkinematic1.unit.get() == 1):
                pres.DataKin=np.multiply(pres.DataKin,1/1000)

            #consider entered sign
            if (preadin.Pm_fx1 == "+"):
                sign = 1
            else: sign = -1
            #readin correct column for GRF and COP (first force plate):
            pres.Fx = np.transpose(sign*np.array([DataDyn[:,preadin.Col_fx1-2]]))
            if (preadin.Pm_fz1 == "+"):
                sign = 1
            else: sign = -1
            pres.Fz = np.transpose(sign*np.array([DataDyn[:,preadin.Col_fz1-2]]))
            if (preadin.Pm_copx1 == "+"):
                sign = 1
            else: sign = -1
            pres.CoP = np.transpose(sign*np.array([DataDyn[:,preadin.Col_copx1-2]]))

            if (preadin.Pm_fx2 == "+"):
                sign = 1
            else: sign = -1
            pres.Fx = np.append(pres.Fx, sign*np.transpose([DataDyn[:,preadin.Col_fx2-2]]), axis = 1)
            if (preadin.Pm_fz2 == "+"):
                sign = 1
            else: sign = -1
            pres.Fz = np.append(pres.Fz, sign*np.transpose([DataDyn[:,preadin.Col_fz2-2]]), axis = 1)
            if (preadin.Pm_copx2 == "+"):
                sign = 1
            else: sign = -1
            pres.CoP = np.append(pres.CoP, sign*np.transpose([DataDyn[:,preadin.Col_copx2-2]]), axis = 1)

            if (preadin.Pm_fx3 == "+"):
                sign = 1
            else: sign = -1
            pres.Fx = np.append(pres.Fx, sign*np.transpose([DataDyn[:,preadin.Col_fx3-2]]), axis = 1)
            if (preadin.Pm_fz3 == "+"):
                sign = 1
            else: sign = -1
            pres.Fz = np.append(pres.Fz, sign*np.transpose([DataDyn[:,preadin.Col_fz3-2]]), axis = 1)
            if (preadin.Pm_copx3 == "+"):
                sign = 1
            else: sign = -1
            pres.CoP = np.append(pres.CoP, sign*np.transpose([DataDyn[:,preadin.Col_copx3-2]]), axis = 1)

            #if CoP1 was measured in mm, convert to meter:
            if (pkinetic.unit.get() == 1):
                pres.CoP=np.multiply(pres.CoP,1/1000)

        #for kinematic data:
        def load_data_kin(import_file_path,k):
            with open(import_file_path[k]) as datatxt: #to find start and end of data
                lines=datatxt.readlines()
                for i in range(0,len(lines)):
                    l=(lines[i]).rstrip("\n").split("\t")
                    if str(l).find(preadin.Keyword_kin) != -1: #kinematics: search entered keyword in data file
                        start_kinematics=i + preadin.Dist_keyword_kin; #kinematics: search line of keyword + entered distance=start line of kinematic data
            pres.DataKin=np.genfromtxt(import_file_path[k],delimiter="\t",skip_header=start_kinematics)

            #if kinematic data were measured in mm, convert to meter:
            if (pkinematic1.unit.get() == 1):
                pres.DataKin=np.multiply(pres.DataKin,1/1000)

        #for kinetic (force, dynamic) data:
        def load_data_dyn(import_file_path,k):
            with open(import_file_path[k]) as datatxt: #to find start and end of data
                lines=datatxt.readlines()
                for i in range(0,len(lines)):
                    l=(lines[i]).rstrip("\n").split("\t")
                    if str(l).find(preadin.Keyword_dyn) != -1: #kinetics: search entered keyword in data file
                        start_kinetics=i + preadin.Dist_keyword_dyn; #kinetics: search line of keyword + entered distance=start line of kinetic data
            DataDyn=np.genfromtxt(import_file_path[k],delimiter="\t",skip_header=start_kinetics)

            #consider entered sign
            if (preadin.Pm_fx1 == "+"):
                sign = 1
            else: sign = -1
            #readin correct column for GRF and COP (first force plate):
            pres.Fx = np.transpose(sign*np.array([DataDyn[:,preadin.Col_fx1-2]]))
            if (preadin.Pm_fz1 == "+"):
                sign = 1
            else: sign = -1
            pres.Fz = np.transpose(sign*np.array([DataDyn[:,preadin.Col_fz1-2]]))
            if (preadin.Pm_copx1 == "+"):
                sign = 1
            else: sign = -1
            pres.CoP = np.transpose(sign*np.array([DataDyn[:,preadin.Col_copx1-2]]))

            if (preadin.Pm_fx2 == "+"):
                sign = 1
            else: sign = -1
            pres.Fx = np.append(pres.Fx, sign*np.transpose([DataDyn[:,preadin.Col_fx2-2]]), axis = 1)
            if (preadin.Pm_fz2 == "+"):
                sign = 1
            else: sign = -1
            pres.Fz = np.append(pres.Fz, sign*np.transpose([DataDyn[:,preadin.Col_fz2-2]]), axis = 1)
            if (preadin.Pm_copx2 == "+"):
                sign = 1
            else: sign = -1
            pres.CoP = np.append(pres.CoP, sign*np.transpose([DataDyn[:,preadin.Col_copx2-2]]), axis = 1)

            if (preadin.Pm_fx3 == "+"):
                sign = 1
            else: sign = -1
            pres.Fx = np.append(pres.Fx, sign*np.transpose([DataDyn[:,preadin.Col_fx3-2]]), axis = 1)
            if (preadin.Pm_fz3 == "+"):
                sign = 1
            else: sign = -1
            pres.Fz = np.append(pres.Fz, sign*np.transpose([DataDyn[:,preadin.Col_fz3-2]]), axis = 1)
            if (preadin.Pm_copx3 == "+"):
                sign = 1
            else: sign = -1
            pres.CoP = np.append(pres.CoP, sign*np.transpose([DataDyn[:,preadin.Col_copx3-2]]), axis = 1)

            #if CoP1 was measured in mm, convert to meter:
            if (pkinetic.unit.get() == 1):
                pres.CoP=np.multiply(pres.CoP,1/1000)

            pres.CoP =  pres.CoP + 0.3 #shift to kinematic system

        self.count = 0 #initialize
        def nextVPP(*args):
            pres.lift()
            if self.count < (len(self.ListeFiles)-1):
                self.count = self.count + 1
            else:
                self.count=0
            if pstart.number_files.get() == 1:
                load_data(self.ListeFiles,self.count)
            else:
                load_data_dyn(self.ListeFiles,self.count)
                load_data_kin(self.ListeFiles_kin,self.count)
            file_path = self.ListeFiles[self.count]
            button_res_single(os.path.basename(file_path)[0:-4])
            show_calc()


        def prevVPP(*args):
            pres.lift()
            if self.count > 0:
                self.count = self.count - 1
            else:
                self.count=len(self.ListeFiles)-1
            if pstart.number_files.get() == 1:
                load_data(self.ListeFiles,self.count)
            else:
                load_data_dyn(self.ListeFiles,self.count)
                load_data_kin(self.ListeFiles_kin,self.count)
            file_path = self.ListeFiles[self.count]
            button_res_single(os.path.basename(file_path)[0:-4])
            show_calc()

        def save_figures(*args):
            if pstart.number_files.get() == 2: #additionally data kin
                import_file_path_kin = self.file_kin
            import_file_path = self.file
            directory = os.path.split(import_file_path[0])[0]
            foldername = directory.split('/')[-1]
            for k in range(0,len(import_file_path)): #read in for each file
                if pstart.number_files == 1:
                    load_data(import_file_path,k)
                else:
                    load_data_dyn(import_file_path,k)
                    load_data_kin(import_file_path_kin,k)
                button_res(os.path.basename(import_file_path[k])[0:-4],foldername,k,2)

        pstart.browseButton_data['command']=readData
        pstart.browseButton_data_kin['command']=readData_kin
        pstart.browseButton_data_dyn['command']=readData
        pstart.browseButton_ini['command']=readIni
        preadin.button_calc['command']=show_calc1
        pres.button_next['command']=nextVPP
        pres.button_prev['command']=prevVPP
        pres.button_save_fig['command']=save_figures


#--------------------------------------------------------------------------------
#---------------------
#--------------------------------------------------------------------------------

if __name__ == "__main__":
    def full(event):
        root.wm_attributes('-fullscreen', True)
    def small(event):
        root.wm_attributes('-fullscreen', False)
        root.wm_geometry("700x500")

    root=tk.Tk()
    main=MainView(root)
    root.title("VPP calculation tool")
    main.place(relwidth=1, relheight=1, relx=0, rely=0)
    root.wm_geometry("700x500+20+30")
    root.mainloop()

