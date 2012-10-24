EMC-E3-Waveform-Double-Exponential-Tool
=======================================

Find a double exponential that meet the required rise and fall times

In E3 and EMC, it is often the case that you need a double exponential to 
represent a transient that meets a specified time to peak and a specified
time to fall to half the peak.

The functional form of the double exponential is given as:
    A*(exp(-alpha*t)-exp(-beta*t))

