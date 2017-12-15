######################################################
# Jackson L. Cole
# University of Wyoming
# Summer 2017 Astronomy REU
######################################################
# General fits reduction script
######################################################

import os
from pyraf import iraf
from pyraf.iraf import noao, imred
from pyraf.iraf import bias
from pyraf.iraf import colbias
import pyfits
from astropy.io import fits

import numpy as np
import csv

os.system('rm -rf ./master*fits')
os.system('rm -rf ./master*list')
os.system('rm -rf ./*.fits')
os.system('rm -rf ./move*')
os.system('rm -rf ./_zbfiles')
os.system('rm -rf ./infiles.txt')
os.system('rm -rf ./object*')


#########################################################
# Varibles/lists with global usage
pathtoscripts = ("/d/www/jcole/public_html/scripts/")
yesresponses = frozenset(["yes","Yes","YES","yEs","y","Y"])
noresponses = frozenset(["no","No","NO","nO","n","N"])
hashblock = "#######################"

#########################################################
#########################################################
def main():
	print '################################################################'
	print '#'
	print '# WIRO Double Prime PyRAF Reduction Script'
	print '#'
	print '# Author: Jackson L. Cole'
	print '# Affiliation: Middle Tennessee State University'
	print '# 2017 University of Wyoming Astronomy REU'
	print '#'
	print '################################################################'
	print '################################################################'
	print '#'
	print '# Please make sure every file from the night of data'
	print '# being reduced is in the current working directory.'
	print '# This reduction script will handle all calibration,'
	print '# reduction, and reorganization of files for any'
	print '# number of objects observed during the night.'
	print '#'
	print '################################################################'
	print '#'
	print '# MAKE SURE YOU READ ALL OF THE PROMPTS AS THEY ARE'
	print '# PRESENTED. CHECK ALL LISTS AS PROMPTED AND TAKE'
	print '# CARE TO *****REMOVE PROBLEM IMAGES FROM THE LISTS'
	print '# ONLY*****'
	print '#'
	print '################################################################'

	print '################################################################'
	print '#'
	print '# ACKNOWLEDGEMENTS'
	print '#'
	print '# Dr. Chip Kobulnicky:'
	print '# \tThe overscan subtraction and trimming of overscan'
	print '# \tregions was adapted from a cl script written by'
	print '# \tDr. Kobulnicky specifically for the WIRO Double'
	print '# \tPrime Imager.'
	print '#'
	print '# David Kasper:'
	print '# \tThe utc_update script used in this script was'
	print '# \twritten by David in order to correct an'
	print '# \tissue found in the DATEOBS keyword in the FITS'
	print '# \theaders of WIRO images.'
	print '#'
	print '################################################################'

	raw_input('Please press [ENTER].')

	os.system('rm -rf ./*.list')

	os.system('ls -1 *.fit > allfit.list')
	os.system('cp allfit.list infiles.txt')
	os.system('rm -rf images_info.list')
	iraf.hselect(images='@allfit.list',fields='$I,FILTER,EXPTIME',expr='yes',Stdout='images_info.list')

	#########################################################
	# Preliminary log-header comparison
	if os.path.exists('./filter_change_lists') == True:
		os.system('mv ./filter_change_lists/filter*change.list .')

	if os.path.isfile('filter_g_change.list') == False:
		os.system('touch ./filter_g_change.list')

	if os.path.isfile('filter_r_change.list') == False:
		os.system('touch ./filter_r_change.list')

	if os.path.isfile('filter_u_change.list') == False:
		os.system('touch ./filter_u_change.list')

	if os.path.isfile('filter_z_change.list') == False:
		os.system('touch ./filter_z_change.list')

	if os.path.isfile('filter_i_change.list') == False:
		os.system('touch ./filter_i_change.list')

	print "The following files have been created in the working directory:\n\nfilter_g_change.list\nfilter_r_change.list\nfilter_u_change.list\nfilter_z_change.list\nfilter_i_change.list\n\nimages_info.list\n\nPlease compare the images_info.list file with the log.txt file to check for correctness of the filter information in the headers. For each image that needs the filter information changed, add the image name to the appropriate file.\n\nExample: Changing a057.fit's filter information from r' to g' would require adding 'a057.fit' to the file filter_g_change.list."
	while True:
		answer = raw_input('Have the images been added to the appropriate change files? (yes/no):\n')
		if answer in yesresponses:
			break
	raw_input('Please press [ENTER] to continue: ')


	iraf.hedit(images='@filter_g_change.list', fields='FILTER', value="Filter 1: g'' 8009", add='yes', verify="no")
	iraf.hedit(images='@filter_r_change.list', fields='FILTER', value="Filter 2: r'' 21126", add='yes', verify="no")
	iraf.hedit(images='@filter_u_change.list', fields='FILTER', value="Filter 3: u'' 34242", add='yes', verify="no")
	iraf.hedit(images='@filter_z_change.list', fields='FILTER', value="Filter 4: z'' 47347", add='yes', verify="no")
	iraf.hedit(images='@filter_i_change.list', fields='FILTER', value="Filter 5: i'' 60445", add='yes', verify="no")

	if os.path.exists('.filter_change_lists') == False:
		os.system('mkdir filter_change_lists')

	os.system('mv ./filter*change.list ./filter_change_lists/')

	while True:

		raw_input('It would be wise to double check the header information before continuing. Please press [ENTER] when completed.\n')
		raw_input('You should double check that information again. Press [ENTER] when finished.\n')
		raw_input('You sure you want to continue? Type Ctrl-c to stop script. Otherwise, please press [ENTER].\n')

		#########################################################
		# Determining the number of objects and the image numbers
		# corresponding to each object
		while True:
			def objectfunc(first,last):
				file = open("allfit.list", 'r')
				lines = file.readlines()
				lines = lines[int(first)-1:int(last)]
				file.close()

				os.system('touch object.list')
				file = open("object.list", 'w')
				for line in lines:
					file.write(str(line)+'\n')
				file.close()
			print hashblock
			raw_input('The following requested entries will ask for the first overall object image and the last overall object image.\nIf there are any issues relating to non-object images taken during the middle of the night, simply enter the first object image and last object image, and you will be allowed to edit before continuing.\nPress [ENTER].')
			print hashblock

			while True:
				firstobject = raw_input('Please enter the number corresponding to the FIRST object image:\n')
				if firstobject.isdigit() == True:
					break

			while True:
				lastobject = raw_input('Please enter the number corresponding to the LAST object image:\n')
				if lastobject.isdigit() == True:
					break

			objectfunc(int(firstobject), int(lastobject))

			os.system('awk "NF" object.list > object.list.tmp')
			os.system('rm -rf object.list')
			os.system('cat object.list.tmp > object.list')
			os.system('rm -rf object.list.tmp')

			answer = raw_input('Please check the file objects.list. Is everything correct? (yes/no):\n')
			if answer in yesresponses:
				break

		print hashblock
		while True:
			print hashblock
			raw_input('Now, you will be required to enter the NUMBER OF OBJECTS observed during the night, as well as the number of the images corresponding to the first and last image of each object. More than likely, only one object will have been observed.\nPlease press [ENTER].')

			while True:
				noofobjects = raw_input('How many objects were observed during the night?:\n')
				if noofobjects.isdigit() == True:
					break

			noofobjects = int(noofobjects)
			objects = []
			objectsrange = np.zeros((2, int(noofobjects)))
			names = []

			for i in range(0,int(noofobjects)):
				print hashblock
				while True:
					name = raw_input('WITH NO SPACES, please enter the name of object {}:\n'.format(i+1))
					objects.insert(i, name)
					answer = raw_input("You have entered that object {} is named {}. Is this correct? (yes/no):\n".format(i+1, name))
					if answer in yesresponses:
						break

				if noofobjects == 1:
					os.system('cp ./object.list ./{}.object.list'.format(name))
				else:
					while True:
						start = raw_input('Enter the two or three digit number corresponding to the FIRST image of object {}:\n'.format(name))
						if start.isdigit() == True:
							break
					while True:
						end = raw_input('Enter the two or three digit number corresponding to the LAST image of object {}:\n'.format(name))
						if end.isdigit() == True:
							break

					objectsrange[0][i] = int(start)
					objectsrange[1][i] = int(end)

					file = open("allfit.list", 'r')
					lines = file.readlines()
					lines = lines[start-1:end]
					file.close()

					os.system('touch {}.object.list'.format(name))
					file = open("{}.object.list".format(name), 'w')
					for line in lines:
						file.write(str(line)+'\n')
					file.close()

				os.system('rm -rf object.{}.{}'.format(i+1,name))
				os.system('mkdir object.{}.{}'.format(i+1,name))
				os.system('sed -e "s/a/mv\ a/" -e "s/.fit/_zbft.fits\ \.\/object.{}.{}\//" {}.object.list > move.{}.object.cl'.format(i+1,name,name,name))
				names.insert(i,name)

				os.system('awk "NF" {}.object.list > {}.object.list.tmp'.format(name,name))
				os.system('rm -rf {}.object.list'.format(name))
				os.system('cat {}.object.list.tmp > {}.object.list'.format(name,name))
				os.system('rm -rf {}.object.list.tmp'.format(name))

				os.system('awk "NF" move.{}.object.cl > move.{}.object.cl.tmp'.format(name,name))
				os.system('rm -rf move.{}.object.cl'.format(name))
				os.system('awk "NF" move.{}.object.cl.tmp > move.{}.object.cl'.format(name,name))
				os.system('rm -rf move.{}.object.cl.tmp'.format(name))

			answer = raw_input('Please check each object.{#}.{objectname} file before continuing. Is everything correct? (yes/no):\n')
			if answer in yesresponses:
				break

		os.system('ls -1 move* > movescripts.list')

		#########################################################
		# Determining the number of bias images
		while True:
			while True:
				print hashblock
				start = raw_input('Enter the two or three digit number corresponding to the FIRST bias image:\n')
				if start.isdigit() == True:
					break
			while True:
				end = raw_input('Enter the two or three digit number corresponding to the LAST bias image:\n')
				if end.isdigit() == True:
					break

				answer = raw_input('You have entered that the bias range is {}-{}. Is this correct? You will have a chance to change things if there are breaks in the bias range. (yes/no):\n'.format(start,end))
				if answer in yesresponses:
					break

			file = open("allfit.list", 'r')
			lines = file.readlines()
			lines = lines[int(start)-1:int(end)]
			file.close()

			os.system('touch bias.list')
			file = open("bias.list", 'w')
			for line in lines:
				file.write(str(line)+'\n')
			file.close()

			os.system('awk "NF" bias.list > bias.list.tmp')
			os.system('rm -rf bias.list')
			os.system('cat bias.list.tmp > bias.list')
			os.system('rm -rf bias.list.tmp')

			answer = raw_input('Please check bias.list against the log file to ensure it is correct. Is everything correct? (yes/no):\n')
			if answer in yesresponses:
				break

		#########################################################
		# Determining the number of flats
		print hashblock
		while True:
			answer = raw_input('Will you be using flats taken on this night or during another night? (tonight/other):\n')
			if answer == 'tonight' or 'other':
				break

		if answer == 'tonight':
			while True:
				while True:
					while True:
						start = raw_input('Enter the two or three digit number corresponding to the FIRST flat image:\n')
						if start.isdigit() == True:
							break
					while True:
						end = raw_input('Enter the two or three digit number corresponding to the LAST flat image:\n')
						if end.isdigit() == True:
							break

					answer = raw_input('You have entered that the flat range is {}-{}. Is this correct? You will have a chance to change things if there are breaks in the flat range. (yes/no):\n'.format(start,end))
					if answer in yesresponses:
						break

				file = open("allfit.list", 'r')
				lines = file.readlines()
				lines = lines[int(start)-1:(end)]
				file.close()

				os.system('touch flat.list')
				file = open("flat.list", 'w')
				for line in lines:
					file.write(str(line)+'\n')
				file.close()

				os.system('awk "NF" flat.list > flat.list.tmp')
				os.system('rm -rf flat.list')
				os.system('cat flat.list.tmp > flat.list')
				os.system('rm -rf flat.list.tmp')

				answer = raw_input('Please check flat.list against the log file for correctness. Is it correct? (yes/no):\n')
				if answer in yesresponses:
					break

		elif answer == 'other':
			while True:
				if os.path.exists('./otherflats') == False:
					os.system('mkdir ./otherflats')
				elif os.path.exists('./otherflats') == True:
					while True:
						try:
							os.rmdir('./otherflats')
							empty = True
							os.system('mkdir ./otherflats')

						except OSError:
							empty = False

						if empty == True:
							raw_input('The directory ./otherflats exists, but is empty. Please move the flats you intend to use to this directory. Press [ENTER] when done.')
							answer = raw_input('Does the directory now contain the flats you intend to use? (yes/no):\n')

						elif empty == False:
							answer = raw_input('The directory ./otherflats exists and contains images. Are these the flats you intend to use? (yes/no)')

						if answer in yesresponses:
							break

				otherflatlist = []
				files = os.listdir('./otherflats')
				for file in files:
					if file.endswith('.fit'):
						otherflatlist.append(file)
				otherflatlist.sort()

				datalist = []
				files = os.listdir('.')
				for file in files:
					if file.endswith('.fit'):
						datalist.append(file)

				datalist.sort()

				highest = len(datalist)
				noofflats = len(otherflatlist)
				newnames = range(highest + 1,highest + 1 + noofflats)

				for i, element in enumerate(newnames):
					newnames[i] = str((str(newnames[i]).zfill(3)))
				newnames = ["a" + name + ".fit" for name in newnames]

				for newname, flat in zip(newnames, otherflatlist):
					os.system('mv ./otherflats/{} ./{}'.format(flat, newname))

				os.system('touch flat.list')

				with open('flat.list', 'w') as file:
					for name in newnames:
						file.write(str(name)+'\n')

				answer = raw_input('Please check the flats and make sure that no data images have been overwritten. Is everything good? (yes/no):\n')
				if answer in yesresponses:
					break

		#########################################################
		# Determining the number of darks
		while True:
			print hashblock
			darkanswer = raw_input('Were any dark exposures taken? (yes/no): ')

			if darkanswer in noresponses:
				print "Awesome! Proceeding as though no dark exposures were taken."
			elif darkanswer in yesresponses:
				while True:
					while True:
						start = raw_input('Enter the two or three digit number corresponding to the FIRST dark image: ')
						if start.isdigit() == True:
							break
					while True:
						end = raw_input('Enter the two or three digit number corresponding to the LAST dark image: ')
						if end.isdigit() == True:
							break

					answer = raw_input('You have entered that the dark range is {}-{}. Is this correct? You will have a chance to change things if there are breaks in the dark range. (yes/no):\n'.format(start,end))
					if answer in yesresponses:
						break

				file = open("allfit.list", 'r')
				lines = file.readlines()
				file.close()

				os.system('touch dark.list')
				file = open("dark.list", 'w')
				for line in lines[int(start)-1:(end)]:
					file.write(str(line)+'\n')
				file.close()

			os.system('awk "NF" dark.list > dark.list.tmp')
			os.system('rm -rf dark.list')
			os.system('cat dark.list.tmp > dark.list')
			os.system('rm -rf dark.list.tmp')

			answer = raw_input('Please check dark.list to ensure it is correct. If no dark exposures were taken, this file should not exist. Is everything correct? (yes/no):\n')
			if answer in yesresponses:
				break

		#########################################################
		# The following is meant to make sure that everything has
		# been thoroughly checked over before proceeding.
		while True:
			print hashblock
			allgood = raw_input('Is everything good?\nReady to rock and roll?\nCan the data reduction process now move on seamlessly without human intervention based on how well you\'ve checked over the header information and list files? Are you confident that all will be well?\nThis is a reminder to be 100% sure of the status of things before proceeding.\nPlease enter YESYESYES to proceed:\n')
			if allgood == 'YESYESYES':
				break
		goodtogo = raw_input('Are we good to go? (yes/no): ')
		if goodtogo in yesresponses:
			break

	#########################################################
	#########################################################
	# Reduction begins here
	iraf.hedit(images='@bias.list',fields='ccdtype',value='bias',add='yes',verify='no')
	iraf.hedit(images='@bias.list',fields='imagetype',value='zero',add='yes',verify='no')
	iraf.hedit(images='@object.list',fields='ccdtype',value='object',add='yes',verify='no')
	iraf.hedit(images='@object.list',fields='ccdtype',value='object',add='yes',verify='no')
	iraf.hedit(images='@flat.list',fields='ccdtype',value='flat',add='yes',verify='no')
	iraf.hedit(images='@flat.list',fields='ccdtype',value='flat',add='yes',verify='no')
	iraf.hedit(images='@dark.list',fields='ccdtype',value='dark',add='yes',verify='no')
	iraf.hedit(images='@dark.list',fields='ccdtype',value='dark',add='yes',verify='no')

	os.system('rm -rf flat_u_temp.list')
	os.system('rm -rf flat_g_temp.list')
	os.system('rm -rf flat_r_temp.list')
	os.system('rm -rf flat_i_temp.list')
	os.system('rm -rf flat_z_temp.list')
	os.system('rm -rf flat_filter.list')

	iraf.hselect(images='@flat.list',fields='$I,FILTER',expr='yes',Stdout="flat_filter.list")
	os.system('grep "Filter 1: g" flat_filter.list | cut -c1-8 > flat_g_temp.list')
	os.system('grep "Filter 2: r" flat_filter.list | cut -c1-8 > flat_r_temp.list')
	os.system('grep "Filter 3: u" flat_filter.list | cut -c1-8 > flat_u_temp.list')
	os.system('grep "Filter 4: z" flat_filter.list | cut -c1-8 > flat_z_temp.list')
	os.system('grep "Filter 5: i" flat_filter.list | cut -c1-8 > flat_i_temp.list')

	####################################################
	os.system('rm -rf infiles.txt')
	os.system('ls -1 *.fit > infiles.txt')
	os.system('rm -rf *z.fits')
	os.system('rm -rf os_subtract.list')
	os.system('touch os_subtract.list')
	os.system('sed "s/.fit/_z.fits/" infiles.txt > os_subtract.list')

	print 'Now beginning overscan subtraction...'

	with open("infiles.txt") as file:
		with open ("os_subtract.list") as file2:
			lines = file.read().splitlines()
			outnames = file2.read().splitlines()
			for line, outname in zip(lines, outnames):
				iraf.imcopy(input="%s[8:2100,1:2048]" % (line),output="foo1.fits",verbose="no")
				iraf.colbias(input="foo1.fits",output="foo1b.fits",bias="[2054:2089,1:2048]",trim="[1:2048,*]",interactive="no", order=3)

				iraf.imcopy(input="%s[2101:4193,1:2048]" % (line),output="foo2.fits",verbose="no")
				iraf.colbias(input="foo2.fits",output="foo2b.fits",bias="[4:40,1:2048]",trim="[46:2093,*]",interactive="no", order=3)

				iraf.imcopy(input="%s[8:2100,2049:4096]" % (line),output="foo3.fits",verbose="no")
				iraf.colbias(input="foo3.fits",output="foo3b.fits",bias="[2054:2088,1:2048]",trim="[1:2048,*]",interactive="no", order=3)

				iraf.imcopy(input="%s[2101:4193,2049:4096]" % (line),output="foo4.fits",verbose="no")
				iraf.colbias(input="foo4.fits",output="foo4b.fits",bias="[4:40,1:2048]",trim="[46:2093,*]",interactive="no", order=3)

				iraf.imcopy(input="%s[1:4096,1:4096]" % (line),output="foo5.fits",verbose="no")
				iraf.imarith(operand1="foo5.fits",op="*",operand2=1.0,result="foo6.fits")
				iraf.imcopy(input="foo1b.fits", output="foo6.fits[1:2048,1:2048]", verbose="no")
				iraf.imcopy(input="foo2b.fits", output="foo6.fits[2049:4096,1:2048]", verbose="no")
				iraf.imcopy(input="foo3b.fits", output="foo6.fits[1:2048,2049:4096]", verbose="no")
				iraf.imcopy(input="foo4b.fits", output="foo6.fits[2049:4096,2049:4096]", verbose="no")
				iraf.imcopy(input="foo6.fits", output=outname,verbose="no" )

				os.system('rm -rf foo*.fits')
				print "{} ----> {}".format(line,outname)

	print 'Moving original fits images to ./originals...'

	os.system('mkdir originals')
	os.system('mv *.fit ./originals/')

	os.system('rm -rf bias_z.list')
	os.system('rm -rf flat_z.list')
	os.system('rm -rf object_z.list')
	os.system('rm -rf dark_z.list')

	os.system('sed "s/.fit/_z.fits/" bias.list > bias_z.list')
	os.system('sed "s/.fit/_z.fits/" object.list > object_z.list')
	os.system('sed "s/.fit/_z.fits/" flat.list > flat_z.list')
	if darkanswer == 'yes' or 'Yes' or 'y' or 'Y':
		os.system('sed "s/.fit/_z.fits/" dark.list > dark_z.list')

	os.system('rm -rf zero_out.list')
	os.system('rm -rf bias_out_temp.list')
	os.system('ls -1 *_z.fits > zero_out.list')
	os.system('cp zero_out.list bias_out_temp.list')
	os.system('sed "s/_z.fits/_zb.fits/" bias_out_temp.list > bias_out.list')

	print 'Now subtracting bias...'
	iraf.imcombine(input='@bias_z.list', output='masterbias_average.fits', combine='average', reject='minmax')
	iraf.unlearn('imarith')
	iraf.imarith(operand1='@zero_out.list',op='-',operand2='masterbias_average.fits',result='@bias_out.list')

	os.system('rm -rf ./*z.fits')

	os.system('sed "s/.fit/_zb.fits/" flat_u_temp.list > flat_u.list')
	os.system('sed "s/.fit/_zb.fits/" flat_g_temp.list > flat_g.list')
	os.system('sed "s/.fit/_zb.fits/" flat_r_temp.list > flat_r.list')
	os.system('sed "s/.fit/_zb.fits/" flat_i_temp.list > flat_i.list')
	os.system('sed "s/.fit/_zb.fits/" flat_z_temp.list > flat_z.list')

	os.system('rm -rf masterflat_u.fits')
	os.system('rm -rf masterflat_g.fits')
	os.system('rm -rf masterflat_r.fits')
	os.system('rm -rf masterflat_i.fits')
	os.system('rm -rf masterflat_z.fits')

	print 'Combining flats...'
	try:
		iraf.imcombine(input='@flat_u.list',output='masterflat_u.fits',combine='median',reject='avsigclip',scale='median',weight='median')
	except:
		pass

	try:
		iraf.imcombine(input='@flat_g.list',output='masterflat_g.fits',combine='median',reject='avsigclip',scale='median',weight='median')
	except:
		pass

	try:
		iraf.imcombine(input='@flat_r.list',output='masterflat_r.fits',combine='median',reject='avsigclip',scale='median',weight='median')
	except:
		pass

	try:
		iraf.imcombine(input='@flat_i.list',output='masterflat_i.fits',combine='median',reject='avsigclip',scale='median',weight='median')
	except:
		pass

	try:
		iraf.imcombine(input='@flat_z.list',output='masterflat_z.fits',combine='median',reject='avsigclip',scale='median',weight='median')
	except:
		pass

	os.system('rm -rf masterflat_u_norm.fits')
	os.system('rm -rf masterflat_g_norm.fits')
	os.system('rm -rf masterflat_r_norm.fits')
	os.system('rm -rf masterflat_i_norm.fits')
	os.system('rm -rf masterflat_z_norm.fits')

	print 'Normalizing flats...'
	try:
		iraf.imarith(operand1="masterflat_u.fits", op="/", operand2=np.mean((pyfits.open('masterflat_u.fits'))[0].data), result="masterflat_u_norm.fits")
	except:
		pass
	try:
		iraf.imarith(operand1="masterflat_g.fits", op="/", operand2=np.mean((pyfits.open('masterflat_g.fits'))[0].data), result="masterflat_g_norm.fits")
	except:
		pass

	try:
		iraf.imarith(operand1="masterflat_r.fits", op="/", operand2=np.mean((pyfits.open('masterflat_r.fits'))[0].data), result="masterflat_r_norm.fits")
	except:
		pass

	try:
		iraf.imarith(operand1="masterflat_i.fits", op="/", operand2=np.mean((pyfits.open('masterflat_i.fits'))[0].data), result="masterflat_i_norm.fits")
	except:
		pass

	try:
		z_mean = iraf.imarith(operand1="masterflat_z.fits", op="/", operand2=np.mean((pyfits.open('masterflat_z.fits'))[0].data), result="masterflat_z_norm.fits")
	except:
		pass

	os.system('rm -rf masterscience.list')
	os.system('rm -rf masterscience_g.list')
	os.system('rm -rf masterscience_r.list')
	os.system('rm -rf masterscience_u.list')
	os.system('rm -rf masterscience_z.list')
	os.system('rm -rf masterscience_i.list')
	os.system('rm -rf masterscience_g_f.list')
	os.system('rm -rf masterscience_r_f.list')
	os.system('rm -rf masterscience_u_f.list')
	os.system('rm -rf masterscience_z_f.list')
	os.system('rm -rf masterscience_i_f.list')

	#os.system('touch masterscience.list')
	iraf.hselect(images='*_zb.fits',fields='$I,FILTER',expr='yes',Stdout="masterscience.list")

	os.system('grep "Filter 1: g" masterscience.list | cut -c1-12 > masterscience_g.list')
	os.system('grep "Filter 2: r" masterscience.list | cut -c1-12 > masterscience_r.list')
	os.system('grep "Filter 3: u" masterscience.list | cut -c1-12 > masterscience_u.list')
	os.system('grep "Filter 4: z" masterscience.list | cut -c1-12 > masterscience_z.list')
	os.system('grep "Filter 5: i" masterscience.list | cut -c1-12 > masterscience_i.list')

	os.system('sed "s/_zb.fits/_zbf.fits/" masterscience_g.list > masterscience_g_f.list')
	os.system('sed "s/_zb.fits/_zbf.fits/" masterscience_r.list > masterscience_r_f.list')
	os.system('sed "s/_zb.fits/_zbf.fits/" masterscience_u.list > masterscience_u_f.list')
	os.system('sed "s/_zb.fits/_zbf.fits/" masterscience_z.list > masterscience_z_f.list')
	os.system('sed "s/_zb.fits/_zbf.fits/" masterscience_i.list > masterscience_i_f.list')

	print 'Now flat fielding...'
	try:
		iraf.imarith('@masterscience_g.list','/','masterflat_g_norm.fits','@masterscience_g_f.list')
	except:
		pass

	try:
		iraf.imarith('@masterscience_r.list','/','masterflat_r_norm.fits','@masterscience_r_f.list')
	except:
		pass

	try:
		iraf.imarith('@masterscience_u.list','/','masterflat_u_norm.fits','@masterscience_u_f.list')
	except:
		pass

	try:
		iraf.imarith('@masterscience_z.list','/','masterflat_z_norm.fits','@masterscience_z_f.list')
	except:
		pass

	try:
		iraf.imarith('@masterscience_i.list','/','masterflat_i_norm.fits','@masterscience_i_f.list')
	except:
		pass

	os.system('rm -rf ./*zb.fits')

	os.system('rm -rf object_filter.list')
	#os.system('object_zbf_g.list')
	#os.system('object_zbf_r.list')
	#os.system('object_zbf_u.list')
	#os.system('object_zbf_z.list')
	#os.system('object_zbf_i.list')
	#os.system('object_zbf_g.tmp')
	#os.system('object_zbf_r.tmp')
	#os.system('object_zbf_u.tmp')
	#os.system('object_zbf_z.tmp')
	#os.system('object_zbf_i.tmp')
	#os.system('object_zbf_g.cl')
	#os.system('object_zbf_r.cl')
	#os.system('object_zbf_u.cl')
	#os.system('object_zbf_z.cl')
	#os.system('object_zbf_i.cl')

	os.system('cp /d/www/jcole/public_html/scripts/utc_update.py .')
	print 'Now correcting the UTC information in the image headers...'

	os.system('python utc_update.py')
	os.system('rm -rf ./*zbf.fits')

	# The following moves the time corrected images into the appropriate object directories.
	'''
	with open("movescripts.list", 'r') as file:
		lines = file.readlines()
		for line in lines:
			print line

			iraf.cl(str(line))
	'''

	with open("movescripts.list", 'r') as file:
		lines = file.read().splitlines()
		for line in lines:
			with open(line, 'r') as file2:
				lines2 = file2.read().splitlines()
				for line2 in lines2:
					os.system(str(line2))

	#######################################################################
	#######################################################################
	#######################################################################
	#######################################################################
	#######################################################################
	#######################################################################
	#######################################################################
	print 'Organizing based on object and filter...'
	for i, name in enumerate(names):
		where = os.getcwd()
		directory = "object.{}.{}".format(i+1,name)
		os.system('rm -rf {}.list'.format(directory))
		path = "./{}".format(directory)
		os.chdir(path)
		os.system('rm -rf *list')
		os.system('rm -rf *cl')
		# In an object directory
		image_file = "{}_zbft.list".format(directory)
		filter_file = "{}_filter.list".format(directory)

		os.system('rm -rf {}'.format(image_file))
		#os.system('ls -1 *zbft.fits > {}'.format(image_file))
		iraf.files('*zbft.fits', Stdout='{}'.format(image_file))
		os.system('rm -rf {}'.format(filter_file))
		os.system('touch {}'.format(filter_file))

		images = []
		with open(image_file, 'r') as file:
			images = file.read().splitlines()

		os.system('rm -rf filter_g')
		os.system('rm -rf filter_r')
		os.system('rm -rf filter_u')
		os.system('rm -rf filter_z')
		os.system('rm -rf filter_i')

		os.system('mkdir filter_g')
		os.system('mkdir filter_r')
		os.system('mkdir filter_u')
		os.system('mkdir filter_z')
		os.system('mkdir filter_i')

		for image in images:
			data, header = fits.getdata(image, header=True)
			if header['FILTER'] == "Filter 1: g' 8009":
				os.system('mv ./{} ./filter_g/'.format(image))

			elif header['FILTER'] == "Filter 2: r' 21126":
				os.system('mv ./{} ./filter_r/'.format(image))

			elif header['FILTER'] == "Filter 3: u' 34242":
				os.system('mv ./{} ./filter_u/'.format(image))

			elif header['FILTER'] == "Filter 4: z' 47347":
				os.system('mv ./{} ./filter_z/'.format(image))

			elif header['FILTER'] == "Filter 5: i' 60445":
				os.system('mv ./{} ./filter_i/'.format(image))

		os.chdir(where)


	#######################################################################
	#######################################################################
	#######################################################################
	#######################################################################
	#######################################################################
	#######################################################################
	#######################################################################
	#iraf.cl('object_zbf_g.cl')
	#iraf.cl('object_zbf_r.cl')
	#iraf.cl('object_zbf_u.cl')
	#iraf.cl('object_zbf_z.cl')
	#iraf.cl('object_zbf_i.cl')


	print 'Cleaning up...'
	os.system('rm -rf ./*z.fits')
	os.system('rm -rf ./*zb.fits')
	os.system('rm -rf ./*zbf.fits')
	os.system('rm -rf ./*zbft.fits')
	os.system('rm -rf ./masterflat*.fits')
	os.system('rm -rf ./masterflat*norm.fits')
	os.system('rm -rf ./masterbias*.fits')
	os.system('rm -rf ./masterdark*.fits')
	os.system('rm -rf ./*flat*.fits')

	print 'All done!'

if __name__ == '__main__':
	main()
