######################################################
# Multi-filter Target Transit Plotting Routine # Author: Jackson L. Cole
# Middle Tennessee State University
# 2017 University of Wyoming Astronomy REU
######################################################

######################################################
# Packages
import os
import matplotlib.pyplot as plt
import numpy as np

###################################################### # The following lines set the fonts for the plotting
from matplotlib import rc
#rc('font',**{'family':'serif','serif':['Times']})
#rc('text', usetex=True)

def main():
    yesresponses = frozenset(['yes','y'])
    testinganswer = raw_input('Are you testing on a mac? (yes/no):\n> ')
    PWD = os.getcwd()
    output = raw_input('Please pick an output format for your graph:\npdf\nps\npng\n> ')
    answer = raw_input('Do you want to plot the filter information as well? This will be output on a separate plot. (yes/no)\n> ')

    print 'The current target directory is: {}'.format(os.getcwd())
    target = raw_input('Please enter the target name:\n> ')
    filters = ['g','r','u','z','i']

    '''
    if os.path.exists('./quote_files/g_quote.txt') == True:
        os.system('cp ./quote_files/g_quote.txt .')
        filters.append('g')

    if os.path.exists('./quote_files/r_quote.txt') == True:
        os.system('cp ./quote_files/r_quote.txt .')
        filters.append('r')

    if os.path.exists('./quote_files/u_quote.txt') == True:
        os.system('cp ./quote_files/u_quote.txt .')
        filters.append('u')

    if os.path.exists('./quote_files/z_quote.txt') == True:
        os.system('cp ./quote_files/z_quote.txt .')
        filters.append('z')

    if os.path.exists('./quote_files/i_quote.txt') == True:
        os.system('cp ./quote_files/i_quote.txt .')
        filters.append('i')
    '''

    ####################################################
    # Finding the full width half max of the data
    pathtofiles = './wiro_doubleprime_filters/'
    filternames = ['g_filter','r_filter','u_filter','z_filter','i_filter']
    asciifiles = ['g-info.csv','r-info.csv','u-info.csv','z-info.csv','i-info.csv']

    for file, filter in zip(asciifiles,filternames):
        if filter == 'g_filter':
            g_filter = np.loadtxt('{}{}'.format(pathtofiles,file), dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))

        elif filter == 'r_filter':
            r_filter = np.loadtxt('{}{}'.format(pathtofiles,file), dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))

        elif filter == 'u_filter':
            u_filter = np.loadtxt('{}{}'.format(pathtofiles,file), dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))

        elif filter == 'z_filter':
            z_filter = np.loadtxt('{}{}'.format(pathtofiles,file), dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))

        elif filter == 'i_filter':
            i_filter = np.loadtxt('{}{}'.format(pathtofiles,file), dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))

    def hwhm(filter_data):
        index = len(filter_data)-150
        maximum = np.max(filter_data[0:index,1])
        for i in range(len(filter_data[0:index,1])):
            if filter_data[i,1] == maximum: maxIndex = i

        minimum = np.min(filter_data[0:index,1])
        for i in range(len(filter_data[0:index,1])):
            if filter_data[i,1] == maximum:
                minIndex = i

        difference = (filter_data[maxIndex,1] - filter_data[minIndex,1])*0.5
        HM = difference*0.5
        nearest = (np.abs(filter_data[:,1] - HM)).argmin()

        for i in range(len(filter_data[0:index,1])):
            if filter_data[i,1] == nearest:
                nearestIndex = i

        hw = np.abs(maxIndex - nearest)

        return hw

    ghw = hwhm(g_filter)*.1
    rhw = hwhm(r_filter)*.1
    uhw = hwhm(u_filter)*.1
    zhw = hwhm(z_filter)*.1
    ihw = hwhm(i_filter)*.1

    ####################################################
    dataarray = np.empty(shape=[5,6])
    dataarray[0,0:3] = [468.6, ghw, ghw] # g
    dataarray[1,0:3] = [616.5, rhw, rhw] # r
    dataarray[2,0:3] = [355.1, uhw, uhw] # u
    dataarray[3,0:3] = [893.1, zhw, zhw] # z
    dataarray[4,0:3] = [748.1, ihw, ihw] # i

    for filter in filters:
        if os.path.exists('./quote_files/{}_quote.txt'.format(filter)) == True:
            os.system('cp ./quote_files/{}_quote.txt .'.format(filter))
            if testinganswer.lower() in yesresponses:
                os.system('gsed -i "s/^.//" {}_quote.txt'.format(filter))
            if testinganswer.lower() not in yesresponses:
                os.system('sed -i "s/^.//" {}_quote.txt'.format(filter))

            datalist = np.loadtxt('{}_quote.txt'.format(filter), float, comments=')', delimiter=',', skiprows=1)
            r_data = datalist[2,:] # Radius data

        elif os.path.exists('/quote_files/{}_quote.txt'.format(filter)) == False:
            r_data = float('nan')

        if filter == 'g':
            dataarray[0,3:7] = r_data
            if os.path.exists('./quote_files/g_quote.txt') == False:
                dataarray[0,0:7] = float('nan')
		elif filter == 'r':
            dataarray[1,3:7] = r_data
            if os.path.exists('./quote_files/r_quote.txt') == False:
                dataarray[1,0:7] = float('nan')
        elif filter == 'u':
            dataarray[2,3:7] = r_data
            if os.path.exists('./quote_files/u_quote.txt') == False:
                dataarray[2,0:7] = float('nan')
        elif filter == 'z':
            dataarray[3,3:7] = r_data
            if os.path.exists('./quote_files/z_quote.txt') == False:
                dataarray[3,0:7] = float('nan')
        elif filter == 'i':
            dataarray[4,3:7] = r_data
            if os.path.exists('./quote_files/i_quote.txt') == False:
                dataarray[4,0:7] = float('nan')

    print dataarray
    ####################################################
    # Loading in auxiliary data from other papers/sources


    lower_x_error = np.transpose(dataarray[:,1])
    upper_x_error = np.transpose(dataarray[:,2])
    x_error = [lower_x_error, upper_x_error]

    lower_y_error = np.transpose(dataarray[:,4])
    upper_y_error = np.transpose(dataarray[:,5])
    y_error = [lower_y_error, upper_y_error]

    f = plt.figure()
    #font = {'family':'Times'}
    #rc('font',**font)
    plt.scatter(dataarray[:,0], dataarray[:,3], color='#000000')
    index = len(g_filter)-150
    plt.errorbar(dataarray[:,0], dataarray[:,3], xerr=x_error, yerr=y_error, fmt='none', ecolor='#000000')
    plt.title(r'{}'.format(target))
    plt.xlabel(r'Wavelength [nm]')
    plt.ylabel(r'$\frac{R_{p}}{R_{*}}$',rotation=0)
    plt.xlim([250, 1000])

    ax = plt.gca()
    #ax.invert_xaxis()
    fig = plt.gcf()
    fig.savefig('{}_plot.{}'.format(target, output))
    f.show()

    if answer in yesresponses:
        g = plt.figure()
        plt.plot(g_filter[0:index,0], g_filter[0:index,1], r_filter[0:index,0], r_filter[0:index,1], u_filter[0:index,0], u_filter[0:index,1], z_filter[0:index,0], z_filter[0:index,1], i_filter[0:index,0], i_filter[0:index,1])
        plt.xlabel(r'Wavelength [nm]')
        plt.ylabel(r'Transmission [%]')
        g.show()

    raw_input()
    os.chdir(PWD)
main()
