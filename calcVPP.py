import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


def VPP_calculation(COP,COM,Force_x, Force_z,VPP_init,file_name):
    def f(VPP_init):
        def VPPsum_dist_squared(VPP, xVPP_beg, xVPP_end, zVPP_beg, zVPP_end, modus):

            xVPP_beg = xVPP_beg[~np.isnan(xVPP_beg)]
            xVPP_end = xVPP_end[~np.isnan(xVPP_end)]
            zVPP_beg = zVPP_beg[~np.isnan(zVPP_beg)]
            zVPP_end = zVPP_end[~np.isnan(zVPP_end)]

            r = -((xVPP_beg - xVPP_end) * (xVPP_end - VPP[0]) + (zVPP_beg - zVPP_end) * (zVPP_end - VPP[1])) / \
                ((xVPP_beg - xVPP_end)**2 + (zVPP_beg - zVPP_end)**2)

            Xx = xVPP_end + r * (xVPP_beg - xVPP_end)
            Xz = zVPP_end + r * (zVPP_beg - zVPP_end)

            r_squared = (VPP[0] - Xx)**2 + (VPP[1] - Xz)**2
            y_temp = np.sqrt(r_squared)

            if modus == 1: #calculation
                y = np.sum(y_temp)
            else: #optimization (to get the minimal distance, is needed for R^2)
                y = np.mean(y_temp)

            return y

        y_VPP = VPPsum_dist_squared(VPP_init, x_beg, x_end, z_beg, z_end, 1)
        return y_VPP

    x_beg = COP - COM[:, 0]
    x_end = COP - COM[:, 0] + Force_x
    z_beg = 0- COM[:, 1] #Copz = 0
    z_end = 0- COM[:, 1] + Force_z

    result = minimize(f, VPP_init)
    return result.x


def R_mod(COP,COM,Force_x, Force_z,VPP_calc,plot,file_name):
    def R_squared(R):
        # calculate explained variation of theoretical and measured forces
        # formula: see Herr and Popovic (2008): Angular momentum in human walking

        temp_mean = np.nanmean(R["theta_exp"])
        t_exp_mean = np.nanmean(temp_mean)

        numerator = np.nansum(np.power(R["theta_exp"] - R["theta_mod"], 2))
        denominator = np.nansum(np.power(R["theta_exp"] - t_exp_mean, 2))

        R_2 = 1 - np.sum(numerator) / np.sum(denominator)
        return R_2


    def VPP_plot(Force_x, Force_z, Com, COP, VPP_opt, factor, j,file_name):
        COPx = COP
        COPz = np.zeros(len(COP))
        #plt.figure(j, figsize=(4, 7)) #figsize: size of the plot window
        plt.clf()
       # plt.gca().set_aspect('equal', adjustable='box')

        if Com[0,0] < Com[-1,0]:
            for ii in range(0, len(COPx), 5):  # draw each single force vector in Com-centered coordinate system
                beg = [(COPx[ii] - Com[ii][0]), COPz[ii] - Com[ii][1]]  # begin force vector (in COP)
                ende = [(Force_x[ii] * factor + COPx[ii] - Com[ii][0]), (Force_z[ii] * factor + COPz[ii] - Com[ii][1])]  # end force vector
                plt.plot([beg[0], ende[0]], [beg[1], ende[1]], color=[0, 0, ii/ (len(COPx) - 1)])
        else: #first value of Comx greater than last -> flip VPP plot and VPPx
            for ii in range(1, len(COPx), 5):  # draw each single force vector in Com-centered coordinate system
                beg = [(COPx[len(COPx)-ii] - Com[len(COPx)-ii][0]), COPz[len(COPx)-ii] - Com[len(COPx)-ii][1]]  # begin force vector (in COP)
                ende = [(Force_x[len(COPx)-ii] * factor + COPx[len(COPx)-ii] - Com[len(COPx)-ii][0]), (Force_z[len(COPx)-ii] * factor + COPz[len(COPx)-ii] - Com[len(COPx)-ii][1])]  # end force vector
                plt.plot([beg[0], ende[0]], [beg[1], ende[1]], color=[0, 0, ii/ (len(COPx) - 1)])


        plt.xlabel('horizontal position [m]')
        plt.ylabel('vertical position [m]')
        plt.title(file_name)
      #  plt.axis([-0.35, 0.25, -1.5, 1.5])
        # plt.gcf().set_position([10, 10, 150, 400])
        p1 = plt.plot(0, 0, 'Xg', markersize=10)  # green cross: COM
        p2 = plt.plot(VPP_opt[0], VPP_opt[1], 'Xr', markersize=10)  # red cross: VPP
        #plt.legend([p1, p2], ['CoM', 'VPP'])
        plt.grid(True)
        if plot == 2:
            plt.savefig(file_name+".svg")

    Cop_Com_Centered_1 = np.transpose([COP,np.zeros(len(COP))])- COM
    VPP_COP_Centered_1 = VPP_calc - Cop_Com_Centered_1
    VPP_Angle_1 = np.squeeze(np.arctan2(VPP_COP_Centered_1[:, 1], VPP_COP_Centered_1[:, 0]))
    VPP_Angle_1[VPP_Angle_1 < 0] = VPP_Angle_1[VPP_Angle_1 < 0] + np.pi
    Force_Angle_1 = np.squeeze(np.arctan2(Force_z, Force_x))
    Force_Angle_1[Force_Angle_1 < 0] = Force_Angle_1[Force_Angle_1 < 0] + np.pi

    R_calc_ss1 = {
        'theta_mod': VPP_Angle_1,
        'theta_exp': Force_Angle_1
    }

    r_mod = R_squared(R_calc_ss1)

    if plot > 0:
        factor = (VPP_calc[1]+1)*1.7 #length of force vectors
        j = 1
        VPP_plot(Force_x, Force_z, COM, COP, VPP_calc, factor, j,file_name)
    return r_mod

