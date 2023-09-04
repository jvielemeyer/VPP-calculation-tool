import csv
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------
def button_get_entries(pkinetic,preadin,pkinematic1,pkinematic2):
    #general
    preadin.Frequ_grf=pkinetic.frequ_grf.get()
    preadin.Frequ_video=pkinematic1.frequ_video.get()
    preadin.Frequ_cut=pkinematic1.frequ_cut.get()
    preadin.Mass=pkinetic.mass.get()
    preadin.Nb_kmp = 3
    preadin.Keyword_dyn=preadin.keyword_dyn.get()
    preadin.Dist_keyword_dyn=preadin.dist_keyword_dyn.get()
    preadin.Dist_keyword_dyn_end=preadin.dist_keyword_dyn_end.get()
    preadin.Keyword_kin=preadin.keyword_kin.get()
    preadin.Dist_keyword_kin=preadin.dist_keyword_kin.get()
    #kinetics
    preadin.Col_fx1=pkinetic.col_fx1.get()
    preadin.Col_fz1=pkinetic.col_fz1.get()
    preadin.Col_copx1=pkinetic.col_copx1.get()
    preadin.Pm_fx1=pkinetic.pm_fx1.get()
    preadin.Pm_fz1=pkinetic.pm_fz1.get()
    preadin.Pm_copx1=pkinetic.pm_copx1.get()
    preadin.Col_fx2=pkinetic.col_fx2.get()
    preadin.Col_fz2=pkinetic.col_fz2.get()
    preadin.Col_copx2=pkinetic.col_copx2.get()
    preadin.Pm_fx2=pkinetic.pm_fx2.get()
    preadin.Pm_fz2=pkinetic.pm_fz2.get()
    preadin.Pm_copx2=pkinetic.pm_copx2.get()
    preadin.Col_fx3=pkinetic.col_fx3.get()
    preadin.Col_fz3=pkinetic.col_fz3.get()
    preadin.Col_copx3=pkinetic.col_copx3.get()
    preadin.Pm_fx3=pkinetic.pm_fx3.get()
    preadin.Pm_fz3=pkinetic.pm_fz3.get()
    preadin.Pm_copx3=pkinetic.pm_copx3.get()

    preadin.Fac_fx=pkinetic.fac_fx.get()
    preadin.Fac_fz=pkinetic.fac_fz.get()

    #kinematics
    pkinematic2.Mal_lat_lx= pkinematic2.mal_lat_lx.get()
    pkinematic2.Mal_lat_lz= pkinematic2.mal_lat_lz.get()
    pkinematic2.Mal_lat_rx= pkinematic2.mal_lat_rx.get()
    pkinematic2.Mal_lat_rz= pkinematic2.mal_lat_rz.get()
    pkinematic2.Mal_med_lx= pkinematic2.mal_med_lx.get()
    pkinematic2.Mal_med_lz= pkinematic2.mal_med_lz.get()
    pkinematic2.Mal_med_rx= pkinematic2.mal_med_rx.get()
    pkinematic2.Mal_med_rz= pkinematic2.mal_med_rz.get()
    pkinematic2.Toe_lx= pkinematic2.toe_lx.get()
    pkinematic2.Toe_lz= pkinematic2.toe_lz.get()
    pkinematic2.Toe_rx= pkinematic2.toe_rx.get()
    pkinematic2.Toe_rz= pkinematic2.toe_rz.get()
    pkinematic2.Knee_lx= pkinematic2.knee_lx.get()
    pkinematic2.Knee_lz= pkinematic2.knee_lz.get()
    pkinematic2.Knee_rx= pkinematic2.knee_rx.get()
    pkinematic2.Knee_rz= pkinematic2.knee_rz.get()
    pkinematic2.Hip_lx= pkinematic2.hip_lx.get()
    pkinematic2.Hip_lz= pkinematic2.hip_lz.get()
    pkinematic2.Hip_rx= pkinematic2.hip_rx.get()
    pkinematic2.Hip_rz= pkinematic2.hip_rz.get()
    pkinematic2.Shoulder_lx= pkinematic2.shoulder_lx.get()
    pkinematic2.Shoulder_lz= pkinematic2.shoulder_lz.get()
    pkinematic2.Shoulder_rx= pkinematic2.shoulder_rx.get()
    pkinematic2.Shoulder_rz= pkinematic2.shoulder_rz.get()


    pkinematic2.Mal_lat = [pkinematic2.Mal_lat_lx, pkinematic2.Mal_lat_lz, pkinematic2.Mal_lat_rx, pkinematic2.Mal_lat_rz]
    pkinematic2.Mal_med = [pkinematic2.Mal_med_lx, pkinematic2.Mal_med_lz, pkinematic2.Mal_med_rx, pkinematic2.Mal_med_rz]
    pkinematic2.Toe = [pkinematic2.Toe_lx, pkinematic2.Toe_lz, pkinematic2.Toe_rx, pkinematic2.Toe_rz]
    pkinematic2.Knee = [pkinematic2.Knee_lx, pkinematic2.Knee_lz, pkinematic2.Knee_rx, pkinematic2.Knee_rz]
    pkinematic2.Hip = [pkinematic2.Hip_lx, pkinematic2.Hip_lz, pkinematic2.Hip_rx, pkinematic2.Hip_rz]
    pkinematic2.Shoulder = [pkinematic2.Shoulder_lx, pkinematic2.Shoulder_lz, pkinematic2.Shoulder_rx, pkinematic2.Shoulder_rz]


#save data in csv
def button_save_data(ListeVPP,filename):
    # fullpath = str(filename) + ".csv"
    fullpath = "Data.csv"
    with open(fullpath,'w') as csvfile:
        writer=csv.writer(csvfile, delimiter=',')
        for index in range(0,len(ListeVPP)):
            writer.writerow(ListeVPP[index])