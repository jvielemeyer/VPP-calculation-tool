# VPP-calculation-tool

This software is created to calculate the Virtual Pivot Point (VPP) easily. Until now, it is only tested on Linux. If there are problems in Windows, please feel free to contact me (johanna.vielemeyer@uni-jena.de) or to optimize the code yourself.

Here is a short description of the software.

## Installation

You have to install the following:

- python3

packages:

- tkinter
- pandas
- numpy
- matplotlib.pyplot
- scipy
- configparser (to read ini-file)

## Starting programm

Start programm in terminal with the following:

```
cd myfolder
python3 main.py
```

## General comments

You need the following data for VPP calculation:
- kinetic data: ground reaction forces (GRF) of x (anterior-posterior, in walking) and z (vertical to walking) direction and center of pressure (CoP) in x direction and optional the mass of the subject (to measure at standing)
- kinematic data: from 3D video system: Marker position of the following joints/ anatomical landmarks: toe, malleolus lateralis, malleolus medialis, epicondylus lateralis femoris (knee), trochanter major (hip), acromion (shoulder), epicondylus lateralis humeri (elbow), ulnar styloid proc. (wrist) to calculate the center of mass (CoM)

File format:
- the input files could be in txt or tsv
- kinetic and kinematic data could be in separate files or in one single file
- it is helpful to name the files according to a system similar to the sample data (e.g. code for subject + number)

You need at least 3 contacts, because the first and the last contact are only used for the calculation of touch down and take-off (to calculate the exact single support phase).




## Description:

Start Page: VPP calculation tool
- choose where kinetic and kinematic data are saved (in one file or in two separate files)
- choose initialisation file (e.g. “VPPdata.ini”), with this you can load in prepared values for all the following general information about the measurement (e.g. marker positions); you can create such file for your data set or skip this feature and write all the values manually in the entries of the gui
- one file: “Load data files”: choose input files, you can also choose the content of the whole folder
- two separate input files: “Load kinetic data files”: choose input files with kinetic data, e.g. “anre 011.txt”; “Load kinematic data files”: choose input files with kinematic data, e.g. “anre0012.tsv” (you can also choose more than one file, but make sure that the data are synchronized in pairs)

1. general information (kinetic data)
- sample frequency: with which frequency measure the ground reaction force plates (you can find this information normally in the txt-files of the kinetic data)
- give the mass of the participant in Newton (note that exact value is not relevant for VPP calculation)
- which column contains the GRF in anterior-posterior (x) direction etc. of the first force plate (e.g. column 11, start counting at 1), sign: direction of the forces (+: direction fits, - direction has to be mirrored)
- factor GRF: Here you can readjust the amplification of the ground reaction forces in the two different dimensions (standard values are “1.0”) 

2. general information (kinematic data)
- sample frequency: with which frequency measures the camera system
- cut-off frequency: with which frequency should the kinematic data (center of mass data) be filtered, used is a bidirectional fourth-order butterworth filter

3. marker setup (kinematic data)
- give the column of the particular markers (start counting at 1)

4. read in data
- give information about where in the input file the data fields could be found (exclude headers)
- press “calculate VPP”

→ Get the following:
 - VPP values in gui and a VPP plot of one data set (you can switch with “next” and “prev” between all files you have loaded in and see the different values and plots, plots are named after the kinetic files)
- a file named “Data.csv” (you can change the code that this is named after the folder, where the data are stored) will be automatically created within the VPP values for each file
- if you click on “save all figures”, all VPP plots will be saved as svg in the current folder

### Description Plot:
- the coordinate system is centered to the center of mass (green cross)
- x-axis: horizontal VPP-position in meter (and horizontal part of the ground reaction forces)
- y-axis: vertical VPP-position in meter (and vertical part of the ground reaction forces)
- lines (black to blue): ground reaction force vectors for different single measurement time points for the single support phase of the contact (that means from toe off of the other leg to the touch down of the other leg), starting at center of pressure
- red cross: calculated VPP position
- Figure title: Name of the kinetic file

## Sample Data
In the folder 'Data' you can found a sample data set. This data set contains kinetic and kinematic data of barefoot walking of one subject (ten trials). You can find more sample data on figshare: https://figshare.com/s/6e934414ca9bb4a2cdde.


