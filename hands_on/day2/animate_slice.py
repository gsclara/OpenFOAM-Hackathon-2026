import numpy as np
import matplotlib.pyplot as plt
import time
#
# Set default plotting size
#
def fixPlot(thickness=1.5, fontsize=20, markersize=8, labelsize=15, texuse=False, tickSize = 15):
    '''
        This plot sets the default plot parameters
    INPUT
        thickness:      [float] Default thickness of the axes lines
        fontsize:       [integer] Default fontsize of the axes labels
        markersize:     [integer] Default markersize
        labelsize:      [integer] Default label size
    OUTPUT
        None
    '''
    # Set the thickness of plot axes
    plt.rcParams['axes.linewidth'] = thickness    
    # Set the default fontsize
    plt.rcParams['font.size'] = fontsize    
    # Set the default markersize
    plt.rcParams['lines.markersize'] = markersize    
    # Set the axes label size
    plt.rcParams['axes.labelsize'] = labelsize
    # Enable LaTeX rendering
    plt.rcParams['text.usetex'] = texuse
    # Tick size
    plt.rcParams['xtick.major.size'] = tickSize
    plt.rcParams['ytick.major.size'] = tickSize
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
#
# Define read binary snapshot function
#
def read_binary(filename,myd_type=np.float64):
    with open(filename,'rb') as f:
        f.seek(0)
        x = np.fromfile(f,dtype=myd_type)
        f.close()
    return x
#
# USER INPUT PARAMETERS
#
Uinf = 5.0
zindex = 10
param = ['Umag']
# Semi-fixed parameters
start_index = 5
interval = 5
end_index = 360
# Load the data
indices = np.arange(start=start_index,step=interval,stop=end_index+interval)
# Load the coordinates
x = read_binary('data/x_'+str(zindex)+'.bin')
y = read_binary('data/y_'+str(zindex)+'.bin')
# Loop and load
fixPlot(thickness=1.2, fontsize=15, markersize=8, labelsize=15, texuse=True, tickSize=15)
# Flag to load building data
load_buildings = True
for myindex in indices:
    time1 = time.time()
    my_filename1 = 'data/'+str(param[0])+'_'+str(zindex)+'_'+str(myindex)+'.bin'
    # Load the file
    Umag = read_binary(my_filename1)  
    plt.tricontourf(x, y, Umag,cmap='BrBG')
    # FORMATTING
    plt.xlabel(r'$x_1$',fontsize=25)
    plt.ylabel(r'$x_2$',fontsize=25)    
    plt.pause(0.5)
    # Print time message
    print(f"Finished {my_filename1} in {time.time()-time1} seconds...")

