######################################################
# Jackson L. Cole
# University of Wyoming
# Summer 2017 Astronomy REU
######################################################
# General fits reduction script
######################################################

import os
#workingdir = os.getcwd()
#irafpath = "/knuckles1/jcole/iraf"
#os.chdir(irafpath)
from pyraf import iraf
from iraf import tv
from pyraf.iraf import noao, imred
from pyraf.iraf import bias
from pyraf.iraf import colbias
#os.chdir(workingdir)

import numpy as np
import csv

#########################################################
# Varibles/lists with global usage
pathtoscripts = ("/d/www/jcole/public_html/scripts/")
yesresponses = frozenset(["yes","Yes","YES","yEs","y","Y"])
noresponses = frozenset(["no","No","NO","nO","n","N"])
hashblock = "#######################"

#########################################################
# Preliminary log-header comparison

os.system('ls -1 *.fit > allfit.list')
os.system('cp allfit.list infiles.txt')
os.system('rm -rf images_info.list')
iraf.hselect(images='@allfit.list',fields='$I,FILTER',expr='yes',Stdout='images_info.list')

####################################################
os.system('rm -rf *z.fits')
os.system('rm -rf os_subtract.list')
os.system('touch os_subtract.list')
os.system('sed "s/.fit/_z.fits/" infiles.txt > os_subtract.list')

with open("infiles.txt") as file:
	with open ("os_subtract.list") as file2:
		lines = file.read().splitlines()
		outnames = file2.read().splitlines()
		for line, outname in zip(lines, outnames):
			iraf.imcopy(input="%s[8:2100,1:2048]" % (line),output="foo1.fits",verbose="no")
			#ccdproc(images="foo1.fits", output="foo1b.fits", overscan="yes", trim="yes", readaxis="column", biassec="[2054:2089,1:2048]", trimsec="[1:2048,*]")
			iraf.colbias(input="foo1.fits",output="foo1b.fits",bias="[2054:2089,1:2048]",trim="[1:2048,*]",interactive="no", order=3)

			iraf.imcopy(input="%s[2101:4193,1:2048]" % (line),output="foo2.fits",verbose="no")

			#ccdproc(images="foo2.fits", output="foo2b.fits", overscan="yes", trim="yes", readaxis="column", biassec="[4:40,1:2048]", trimsec="[46:2093,*]")
			iraf.colbias(input="foo2.fits",output="foo2b.fits",bias="[4:40,1:2048]",trim="[46:2093,*]",interactive="no", order=3)

			iraf.imcopy(input="%s[8:2100,2049:4096]" % (line),output="foo3.fits",verbose="no")
			#ccdproc(images="foo3.fits", output="foo3b.fits", overscan="yes", trim="yes", readaxis="column", biassec="[2054:2088,1:2048]", trimsec="[1:2048,*]")
			iraf.colbias(input="foo3.fits",output="foo3b.fits",bias="[2054:2088,1:2048]",trim="[1:2048,*]",interactive="no", order=3)

			iraf.imcopy(input="%s[2101:4193,2049:4096]" % (line),output="foo4.fits",verbose="no")
			#ccdproc(images="foo4.fits", output="foo4b.fits", overscan="yes", trim="yes", readaxis="column", biassec="[4:40,1:2048]", trimsec="[46:2093,*]")
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
