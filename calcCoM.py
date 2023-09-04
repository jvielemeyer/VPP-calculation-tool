
from math import *
import numpy as np

#----------------------------------------------------
#calculates position of the center of mass in 3D
#input: kinematic data(frames, x,z)
# theoretical data from Winter, 2009, Biomechanics and Motor Control of Human Movement:

def Com_calc(DataKin, Mal_lat, Mal_med, Toe, Knee, Hip, Shoulder,preadin):
    weighting_masses = np.multiply([1.45, 4.65, 10, 67.8*0.5],1/100) #foot, leg (shank), thigh, 1/2 HAT: head, arms, trunk
    offset = 1
    distances = np.multiply([50, 43.3, 43.3, 62.6],1/100)
    Foot_l = DataKin[:,[Mal_lat[0]-offset,Mal_lat[1]-offset]] - np.multiply((DataKin[:,[Mal_lat[0]-offset,Mal_lat[1]-offset]]-DataKin[:,[Toe[0]-offset,Toe[1]-offset]]),distances[0])
    Foot_r = DataKin[:,[Mal_lat[2]-offset,Mal_lat[3]-offset]] - np.multiply((DataKin[:,[Mal_lat[2]-offset,Mal_lat[3]-offset]]-DataKin[:,[Toe[2]-offset,Toe[3]-offset]]),distances[0])
    Shank_l = DataKin[:,[Knee[0]-offset,Knee[1]-offset]] - np.multiply((DataKin[:,[Knee[0]-offset,Knee[1]-offset]]-DataKin[:,[Mal_med[0]-offset,Mal_med[1]-offset]]),distances[1])
    Shank_r = DataKin[:,[Knee[2]-offset,Knee[3]-offset]] - np.multiply((DataKin[:,[Knee[2]-offset,Knee[3]-offset]]-DataKin[:,[Mal_med[2]-offset,Mal_med[3]-offset]]),distances[1])
    Thigh_l = DataKin[:,[Hip[0]-offset,Hip[1]-offset]] - np.multiply((DataKin[:,[Hip[0]-offset,Hip[1]-offset]]-DataKin[:,[Knee[0]-offset,Knee[1]-offset]]),distances[2])
    Thigh_r = DataKin[:,[Hip[2]-offset,Hip[3]-offset]] - np.multiply((DataKin[:,[Hip[2]-offset,Hip[3]-offset]]-DataKin[:,[Knee[2]-offset,Knee[3]-offset]]),distances[2])
    HAT_l = DataKin[:,[Hip[0]-offset,Hip[1]-offset]] - np.multiply((DataKin[:,[Hip[0]-offset,Hip[1]-offset]]-DataKin[:,[Shoulder[0]-offset,Shoulder[1]-offset]]),distances[3])
    HAT_r = DataKin[:,[Hip[2]-offset,Hip[3]-offset]] - np.multiply((DataKin[:,[Hip[2]-offset,Hip[3]-offset]]-DataKin[:,[Shoulder[2]-offset,Shoulder[3]-offset]]),distances[3])
    CoM = np.multiply((Foot_l + Foot_r),weighting_masses[0]) + np.multiply((Shank_l + Shank_r),weighting_masses[1]) + np.multiply((Thigh_l + Thigh_r),weighting_masses[2]) + np.multiply((HAT_l + HAT_r),weighting_masses[3])

    return CoM

