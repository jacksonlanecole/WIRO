import batman
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
import time
import corner
import emcee
import sys
import os


imfilt=str(sys.argv[1]+'.txt') ##give the txt file for the single nights data

dat=np.zeros((2,3)) ##will hold all data

##input locations for priors and relative photometry solved data 
night = np.genfromtxt(imfilt, delimiter='\t',skip_header=1) #read data

midpoint= np.genfromtxt(imfilt,dtype='str',usecols=(0),comments='earth') #read midpoint (comments=/='#')

cut=str.find(midpoint[0],'=') ##normalize time to midpoint
midpoint=midpoint[0][int(cut)+1:]
night[:,0]=night[:,0]-float(midpoint)
for y in range (0, len(night)): ##re-write data into numpy array
    dat = np.append(dat,[night[y]],axis=0)

dat = np.delete(dat,[0,1],axis=0) ##clear the inital filler

inpriors = np.genfromtxt('priors.txt', delimiter='\t',skip_header=1) #read priors data



###BATMAN###################
#physical parameters
params = batman.TransitParams()
tif_true = params.t0 = inpriors[0,1]                       #time of inferior conjunction
per_true = params.per = inpriors[1,1]                      #orbital period (arbitrary with time units)
r_true = params.rp = inpriors[2,1]                      #planet radius (in units of stellar radii)
a_true = params.a = inpriors[3,1]                       #semi-major axis (in units of stellar radii)
inc_true = params.inc = inpriors[4,1]                     #orbital inclination (in degrees)
ecc_true = params.ecc = inpriors[5,1]                      #eccentricity
w_true = params.w = inpriors[6,1]                       #longitude of periastron (in degrees)
params.limb_dark = "quadratic"        #limb darkening model
params.u = [0.1,0.3]      #limb darkening coefficients
f_true=0.001
t = np.array(dat[:,0]) ##create time array in BATMAN readable format

m = batman.TransitModel(params, t)    #initializes model
   #calculation timespace (start,stop,divisions)
flux = m.light_curve(params)          #calculates light curve

##################################

t0=time.time()


#split up data into time and flux

x=t
y=dat[:,1]
yerr=dat[:,2]
#end create data

plt.plot(t,flux,"b")
plt.errorbar(x, y, yerr=yerr, fmt=".r")
plt.xlabel("Time from central transit")
plt.ylabel("Relative flux")
plt.savefig(sys.argv[1]+"_realimage.png")
plt.clf()


##mcmc##############
#log likelihood
def lnlike(theta,x,y,yerr):
    tif,per,r,a,inc, ecc,w,lnf = theta
    if 0. <= ecc <= 1.  and 0. <= w <= 90. and 0. <= per and 0. <= r and 0. <= inc <= 1.:
        params.t0 = tif
        params.per = per
        params.rp = r
        params.a = a
        params.inc = np.arccos(inc)*180./np.pi
        params.ecc = ecc
        params.w = w
        flux=m.light_curve(params)
        model = flux
        inv_sigma2 = 1.0/(yerr**2 + model**2*np.exp(2*lnf))
        return -0.5*np.sum((y-model)**2*inv_sigma2-np.log(inv_sigma2))
    else:
        return -np.inf
#log prior
def lnprior(theta):
    tif,per,r,a,inc,ecc,w,lnf = theta
    if -10. < lnf < -2. and (tif_true-inpriors[0,2]) < tif < (tif_true+inpriors[0,2]) and (per_true-inpriors[1,2]) < per < (per_true+inpriors[1,2]) and (r_true-inpriors[2,2]) < r < (r_true+inpriors[2,2]) and (a_true-inpriors[3,2]) < a < (a_true+inpriors[3,2]) and np.cos((inc_true-inpriors[4,2])*np.pi/180.) > inc > np.cos((inc_true+inpriors[4,2])*np.pi/180.) and (ecc_true-inpriors[5,2]) < ecc < (ecc_true+inpriors[5,2]) and (w_true-inpriors[6,2]) < w < (w_true+inpriors[6,2]):
        return 0.0
    return -np.inf


#full log probability lnlikelihood + lnprior
def lnprob(theta,x,y,yerr):
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp+lnlike(theta,x,y,yerr)
#####################



#numerical optimum of log likelihood (first guess)
nll = lambda *args: -lnlike(*args)
result = op.minimize(nll, [tif_true, per_true, r_true, a_true, np.cos(inc_true*np.pi/180.), ecc_true, w_true, np.log(f_true)], args=(x, y, yerr)) #take first guess "true's" and run them to best
tif_ml, per_ml, r_ml, a_ml, inc_ml, ecc_ml, w_ml, lnf_ml = result["x"]
print result["x"], "first guesses"
t1 = time.time() 
print t1- t0, "seconds to find initial guesses"

#independent walkers set up
ndim, nwalkers= 8, 100 #100 walkers in 8dimensional space
pos = [result["x"]+1e-3*np.random.randn(ndim) for i in range(nwalkers)]

#mcmc runner
sampler=emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(x,y,yerr))

sampler.run_mcmc(pos,1000) #run each setup for 500 steps
samples = sampler.chain[:, 500:, :].reshape((-1, ndim)) #cut away the first 50 and also reshape to 45000x8 as all samples in chain are equally good

t2 = time.time() - t1
print t2, "seconds to run mcmc"

#diagnostic tools
#-----------------

samples[:, 4] = np.arccos(samples[:, 4])*180/np.pi ##remake all cosi's into i


#the 1 and 2D posterior probability distributions
fig = corner.corner(samples[:,[0,2,3,4,5]], labels=["$tif$" , "radius", "$a$", "$i$","$e$"],
                      truths=[tif_true, r_true, a_true, inc_true, ecc_true]) 
fig.savefig(sys.argv[1]+"_post_0.png")
fig.clf()

fig = corner.corner(samples[:,[1,2,3,6,7]], labels=["T" , "radius", "$a$", "$w$","$lnf$"],
                      truths=[per_true, r_true, a_true, w_true, np.log(f_true)]) 
fig.savefig(sys.argv[1]+"_post_1.png")
fig.clf()

print("Mean acceptance fraction: {0:.3f}".format(np.mean(sampler.acceptance_fraction)))

#for i in range(ndim):
#    pl.figure()
#    pl.hist(sampler.flatchain


#numbers to quote
samples[:, 7] = np.exp(samples[:, 7]) #remake all lnf's into f

#give the 50th, then 84-50th then 50-16th percentiles of the chain population for each of the 3 params (value +high-low)
tif_mcmc, per_mcmc, r_mcmc, a_mcmc, inc_mcmc, ecc_mcmc, w_mcmc, f_mcmc = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),  
                             zip(*np.percentile(samples, [16, 50, 84], 
                                                axis=0))) #get the 16,50,and84 percentiles along the unweighted 45000 chain for the 2 params

f = open(sys.argv[1]+"_quote.txt", 'w')
f.write("Mean acceptance fraction: {0:.3f}".format(np.mean(sampler.acceptance_fraction))+"\n")
f.write(str(tif_mcmc)+"mcmc analysis of tif\n")
f.write(str(per_mcmc)+"mcmc analysis of period\n")
f.write(str(r_mcmc)+"mcmc analysis of r\n")
f.write(str(a_mcmc)+"mcmc analysis of a\n")
f.write(str(inc_mcmc)+"mcmc analysis of i\n")
f.write(str(ecc_mcmc)+"mcmc analysis of ecc\n")
f.write(str(w_mcmc)+"mcmc analysis of w\n")
f.write(str(f_mcmc)+ "mcmc analysis of f\n")
f.close() 

print tif_mcmc, "mcmc analysis of tif"
print per_mcmc, "mcmc analysis of period"
print r_mcmc, "mcmc analysis of r"
print a_mcmc, "mcmc analysis of a"
print inc_mcmc, "mcmc analysis of i"
print ecc_mcmc, "mcmc analysis of ecc"
print w_mcmc, "mcmc analysis of w"
print f_mcmc, "mcmc analysis of f"

##make a "best fit plot"
params.t0 = tif_mcmc[0]                       #time of inferior conjunction
params.per = per_mcmc[0]                      #orbital period (arbitrary with time units)
params.rp = r_mcmc[0]                     #planet radius (in units of stellar radii)
params.a = a_mcmc[0]                       #semi-major axis (in units of stellar radii)
params.inc = inc_mcmc[0]                     #orbital inclination (in degrees)
params.ecc = ecc_mcmc[0]                   #eccentricity
params.w = w_mcmc[0] 
params.limb_dark = "quadratic"        #limb darkening model
params.u = [0.1,0.3]      #limb darkening coefficients

flux1 = m.light_curve(params) #publish 50th percentile
plt.plot(t,flux1,"r")


##remake flux for 16th
params.t0 = tif_mcmc[0]-tif_mcmc[1]                       #time of inferior conjunction
params.per = per_mcmc[0]-per_mcmc[1]                      #orbital period (arbitrary with time units)
params.rp = r_mcmc[0]-r_mcmc[1]                     #planet radius (in units of stellar radii)
params.a = a_mcmc[0]-a_mcmc[1]                       #semi-major axis (in units of stellar radii)
params.inc = inc_mcmc[0]-inc_mcmc[1]                     #orbital inclination (in degrees)
params.ecc = ecc_mcmc[0]-ecc_mcmc[1]                   #eccentricity
params.w = w_mcmc[0]-w_mcmc[1] 
params.limb_dark = "quadratic"        #limb darkening model
params.u = [0.1,0.3]      #limb darkening coefficients

flux2=m.light_curve(params)


##remake flux for 84th
params.t0 = tif_mcmc[0]+tif_mcmc[2]                       #time of inferior conjunction
params.per = per_mcmc[0]+per_mcmc[2]                      #orbital period (arbitrary with time units)
params.rp = r_mcmc[0]+r_mcmc[2]                     #planet radius (in units of stellar radii)
params.a = a_mcmc[0]+a_mcmc[2]                       #semi-major axis (in units of stellar radii)
params.inc = inc_mcmc[0]+inc_mcmc[2]                     #orbital inclination (in degrees)
params.ecc = ecc_mcmc[0]+ecc_mcmc[2]                   #eccentricity
params.w = w_mcmc[0]+w_mcmc[2] 
params.limb_dark = "quadratic"        #limb darkening model
params.u = [0.1,0.3]      #limb darkening coefficients

flux3=m.light_curve(params)

plt.fill_between(x,flux2,flux3,facecolor='b')

plt.errorbar(x, y, yerr=yerr, fmt=".r")
plt.xlabel("Time from central transit")
plt.ylabel("Relative flux")
plt.savefig(sys.argv[1]+"_fitimage.png")
plt.clf()

t3 = time.time()

print t3-t0, "total seconds"

