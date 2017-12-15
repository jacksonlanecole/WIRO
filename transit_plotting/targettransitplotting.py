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
	testinganswer = raw_input('Are you testing on a mac? (yes/no):\n')


	print 'The current target directory is: {}'.format(os.getcwd())
	target = raw_input('Please input the name of the target exactly as written in the target directory path above:\n')

	filters = []
	if os.path.exists('./g') == True:
		filters.append('g')

	if os.path.exists('./r') == True:
		filters.append('r')

	if os.path.exists('./u') == True:
		filters.append('u')

	if os.path.exists('./z') == True:
		filters.append('z')

	if os.path.exists('./i') == True:
		filters.append('i')

	print "The following filter directories exist for {}:".format(target)
	for filter in filters:
		print '{}'.format(filter)

	namestemp = []
	for filter in filters:
		for root, dirs, files in os.walk('./{}'.format(filter)):
			name1 = os.listdir('./{}'.format(filter))
			for i in name1:
				namestemp.append(i)
	names = []
	for name in namestemp:
		if name not in names:
			names.append(name)

	namestemp = []
	completenames = []
	incompletenames = []
	for name in names:
		for filter in filters:
			if os.path.exists('./{}/{}'.format(filter, name)) == True:
				namestemp.append(filter)
		if set(namestemp) & set(filters) == set(filters):
			completenames.append(name)
		elif set(namestemp) & set(filters) != set(filters):
			incompletenames.append(name)

		nameestemp = []

	print 'The following people have completed reductions of all available filters for {}:'.format(target)

	for name in completenames:
		print name

	print 'The following people have only partially completed reductions of all available filters for {}:'.format(target)

	for name in incompletenames:
		print name

	namechoice = raw_input('Please select the person whose data you would like to plot:\n')

	if os.path.exists('./plotted_results') == False:
		os.system('mkdir ./plotted_results')
		os.system('chmod 777 ./plotted_results')

		if os.path.exists('./plotted_results/{}'.format(namechoice)) == False:
			os.system('mkdir ./plotted_results/{}'.format(namechoice))
			os.system('chmod 777 ./plotted_results/{}'.format(namechoice))

	elif os.path.exists('./plotted_results') == True:
		if os.path.exists('./plotted_results/{}'.format(namechoice)) == False:
			os.system('mkdir ./plotted_results/{}'.format(namechoice))
			os.system('chmod 777 ./plotted_results/{}'.format(namechoice))

	######################################################
	# The following set of conditional statements check
	# for the existence of an auxiliary data set directory.
	'''
	if os.path.exists('./plotted_results/{}/extradatasets'.format(namechoice)) == False:
		os.system('mkdir ./plotted_results/{}/extradatasets'.format(namechoice))
		os.system('chmod 777 ./plotted_results/{}/extradatasets')
		exex = False

	if os.path.exists('./plotted_results/{}/extradatasets'.format(namechoice)) == True:
		exex = True
		try:
			os.rmdir('./plotted_results/{}/extradatasets'.format(namechoice))
			empty = True
			os.system('mkdir ./plotted_results/{}/extradatasets'.format(namechoice))
			os.system('chmod 777 ./plotted_results/{}/extradatasets'.format(namechoice))
		except OSError:
			empty = False

		os.system('mkdir ./plotted_results/{}/extradatasets'.format(namechoice))
		os.system('chmod 777 ./plotted_results/{}/extradatasets')
		exex = True

	######################################################

	while True:
		if exex == False:
			raw_input('The directory ./plotted_results/{}/extradatasets has been created. Please create files corresponding to any extra data sets you wish to use, using the naming convention\n\t1_useful'.format(namechoice))

		print 'Before going any further, if there are any auxiliary data sets you wish to use (from other sources, papers, etc.), please put them in ./plotted_results/{}/extradatasets.'.format(namechoice)
	'''

	filter_quote_loc = []
	filter_quote_dest = []
	for i, filter in enumerate(filters):
		filter_quote_loc.append('./{}/{}/{}_quote.txt'.format(filter, namechoice, filter))
		filter_quote_dest.append('./plotted_results/{}/'.format(namechoice))

	for location, destination in zip(filter_quote_loc, filter_quote_dest):
		os.system('cp {} {}'.format(location, destination))

	plot_dir = './plotted_results/{}'.format(namechoice)
	os.chdir(plot_dir)

	####################################################
	# Finding the full width half max of the data
	pathtofiles = '/d/www/jcole/public_html/scripts/transit_plotting/wiro_doubleprime_filters/'
	files = ['G-PRIME.CSV','R-PRIME.CSV','U-PRIME.CSV','Z-PRIME.CSV','I-PRIME.CSV']
	asciifiles = ['g-info.csv','r-info.csv','u-info.csv','z-info.csv','i-info.csv']

	for file, asciifile in zip(files,asciifiles):
		os.system('iconv -f UTF-16 -t ASCII {}{} > {}{}'.format(pathtofiles,file,pathtofiles,asciifile))

	g_filter = np.loadtxt('/d/www/jcole/public_html/scripts/transit_plotting/wiro_doubleprime_filters/g-info.csv', dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))
	r_filter = np.loadtxt('/d/www/jcole/public_html/scripts/transit_plotting/wiro_doubleprime_filters/r-info.csv', dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))
	u_filter = np.loadtxt('/d/www/jcole/public_html/scripts/transit_plotting/wiro_doubleprime_filters/u-info.csv', dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))
	z_filter = np.loadtxt('/d/www/jcole/public_html/scripts/transit_plotting/wiro_doubleprime_filters/z-info.csv', dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))
	i_filter = np.loadtxt('/d/www/jcole/public_html/scripts/transit_plotting/wiro_doubleprime_filters/i-info.csv', dtype=np.float, delimiter=',', skiprows=1, usecols=(0,1))

	def hwhm(filter_data):
		index = len(filter_data)-150
		maximum = np.max(filter_data[0:index,1])
		for i in range(len(filter_data[0:index,1])):
			if filter_data[i,1] == maximum:
				maxIndex = i

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
		if testinganswer == 'yes':
			os.system('gsed -i "s/^.//" {}_quote.txt'.format(filter))
		if testinganswer == 'no':
			os.system('sed -i "s/^.//" {}_quote.txt'.format(filter))
		datalist = np.loadtxt('{}_quote.txt'.format(filter), float, comments=')', delimiter=',', skiprows=1)
		r_data = datalist[2,:]
		if filter == 'g':
			dataarray[0,3:7] = r_data
		elif filter == 'r':
			dataarray[1,3:7] = r_data
		elif filter == 'u':
			dataarray[2,3:7] = r_data
		elif filter == 'z':
			dataarray[3,3:7] = r_data
		elif filter == 'i':
			dataarray[4,3:7] = r_data

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
	fig.savefig('{}_plot.pdf'.format(target))
	f.show()

	g = plt.figure()
	plt.plot(g_filter[0:index,0], g_filter[0:index,1], r_filter[0:index,0], r_filter[0:index,1], u_filter[0:index,0], u_filter[0:index,1], z_filter[0:index,0], z_filter[0:index,1], i_filter[0:index,0], i_filter[0:index,1])
	plt.xlabel(r'Wavelength [nm]')
	plt.ylabel(r'Transmission [%]')
	g.show()

	raw_input()

main()
