import sys
import os
from pyraf import iraf
import time
import string
import datetime

##create a list of all images
os.system("ls *zbf.fits > science.txt")
##create an output list
os.system("sed -e s/f.fits/ft.fits/ science.txt > timecorrected.txt")

##make the image list a python list
orgfiles = [line.rstrip('\n') for line in open('science.txt')]
newfiles = [line.rstrip('\n') for line in open('timecorrected.txt')]

##read accurate local time header and inaccurate UTC time header
loctim = iraf.hselect('@science.txt','date-obs','yes',Stdout=1)
uthour = iraf.hselect('@science.txt','utc','yes',Stdout=1)

##for each iamge
for i in range (0, len(loctim)):
     iraf.imcopy(orgfiles[i],newfiles[i])
     update=datetime.datetime(year=int(str(loctim[i])[0:4]),month=int(str(loctim[i])[5:7]),day=int(str(loctim[i])[8:10]),hour=int(str(loctim[i])[11:13]),minute=int(str(loctim[i])[14:16]),second=int(str(loctim[i])[17:19]),microsecond=int(str(loctim[i])[20:23])*1000)  ##read in the time to python's datetime function
    
     diff = int(str(uthour[i])[0:2])-int(str(loctim[i])[11:13]) #find the (hour) difference between UTC and loc header entries
     
     if diff < 0:
          diff+=24 ##get true difference if rollover to next night has occured
     if 10 >= int(str(loctim[i-1])[14:16]) >= 0 and 60 >= int(str(uthour[i-1])[3:5]) >= 50: ##get true hour difference if hour rollover has only occured for local time
          diff+=1
     if not (6 == diff):  ##if the diff is not 6 or 7 something went wrong for WIRO data
           print 'Something went wrong with the MT to UTC conversion on image '+orgfiles[i]
     diff = datetime.timedelta(hours=diff) ##make hour difference into the right class to interact with datetime objects
     update=update+diff
     datetim=update.isoformat()

     iraf.hedit(newfiles[i],'date-obs',datetim,verify='no',show='no')#write new image with AIJ time inputs


