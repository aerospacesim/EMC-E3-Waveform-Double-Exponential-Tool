# -*- coding: utf-8 -*-
"""
Find a double exponential that meet the required rise and fall times

In E3 and EMC, it is often the case that you need a double exponential to 
represent a transient that meets a specified time to peak and a specified
time to fall to half the peak.

The functional form of the double exponential is given as:
    A*(exp(-alpha*t)-exp(-beta*t))

@author: Tim McDonald tim@ema3d.com
"""
###### User input REQUIRED below #####################################
#Enter the desired time to peak
peak = 6.4e-6

#Enter the desired time to decay to half of the peak
halftime=75e-6

#Enter the desired time to decay nearly to zero
fulldecay=0.001

#Enter the desired peak intensity
intensity = 200000
###### End User Input Area ############################################


#Load the modules
import numpy as np
import pylab as plt
from scipy import optimize

#Define the Double Exponential Equation
def f2(t,A,alpha,beta):
    return A*(np.exp(-alpha*t)-np.exp(-beta*t))
    
#Now make an educated guess about the initial parameters
guess = [1.0* intensity, 1/halftime, 1/peak]

#Enter the desired "fit" data in X and Y
#The points before and after the peak keep the fitted peak from overshooting
#Too much
xdata = np.array([0.0, peak/5, 0.8*peak, peak, halftime/4, halftime/2, \
    halftime, fulldecay])
ydata = np.array([0.0, 0.5*intensity, 0.98*intensity, 1.0*intensity, \
    0.9*intensity, 0.736*intensity, 0.5*intensity, 1e-9*intensity])

#Enter the time array for plotting later
t=np.arange(0,fulldecay/2,peak/100)

#Enter the allowed error for the fit routine
sigma = np.array([0.5, 0.005, 0.5, 0.0001, 0.0005, 0.0001, 0.00002, 10000])

#Do the first optimization (curve fit) for the exponential function
params, params_covariance = optimize.curve_fit(f2, xdata, ydata, guess, \
    sigma,maxfev=16000000)

#You probably slightly missed the peak, we care about this the most
#Let's do another optimization to ensure that the peak is at the exact
#right time

#The function below is the derivative of the double exponential curve
def f4(t,beta):
    return -params[1]*np.exp(-params[1]*t)+beta*np.exp(-beta*t)
    
#We want to make sure that at the peak time, the derivative is zero
xdata3 = np.array([peak])
ydata3 = np.array([0])

#execute the next optimization
newbeta, root_covariance = optimize.curve_fit(f4, xdata3, ydata3,params[2])

#Take beta as the second optimization result
beta = newbeta

#keep the old alpha
alpha = params[1]

#The peak intensity may be slightly off now, correct this
A = params[0] * intensity / f2(peak,params[0],alpha,beta)


#The function below is the derivative of the double exponential curve
def f3(t,alpha):
    return A*(np.exp(-alpha*t)-np.exp(-beta*t))
    
#We want to make sure that at the peak time, the derivative is zero
xdata2 = np.array([halftime])
ydata2 = np.array([0.5*intensity])

#execute the next optimization
newalpha, root_covariance = optimize.curve_fit(f3, xdata2, ydata2,params[1])

#Take alpha as the second optimization result
alpha = newalpha

#The peak intensity may be slightly off now, correct this
A = params[0] * intensity / f2(peak,params[0],alpha,beta)



#Plot is and show the results
xdata2 = np.array([0.0 , peak, halftime])
ydata2 = np.array([0.0 , 1.0*intensity, 0.5*intensity])
plt.plot(t,f2(t,A,alpha,beta),'-',xdata2,ydata2,'o')
plt.xlabel('Time (s)')
plt.ylabel('Intensity (AU)')
plt.figtext(0.6,0.6,r'$\alpha$ = ' + np.str(alpha[0]) + '\n' + r'$\beta$ = ' + \
str(beta[0]) + '\n' + 'A = ' + np.str(A[0]))
print r'$\alpha$ = ' + np.str(alpha[0]) + '\n' + r'$\beta$ = ' + \
str(beta[0]) + '\n' + 'A = ' + np.str(A[0])