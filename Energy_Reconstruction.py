import ROOT
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
import scipy.optimize as opt
import matplotlib.mlab as mlab
import numpy as np
from scipy.stats import norm
from scipy.optimize import curve_fit
from numpy.polynomial import Polynomial

rcParams['mathtext.fontset'] = 'stix'
rcParams['font.family'] = 'STIXGeneral'

def plotEnergy(xvalues1, xvalues2): # Plots reconstructed energy as a histogram
    n, bins, patches = plt.hist(xvalues1, bins=nbins1, edgecolor = "k", color = "firebrick", alpha = 0.8, histtype = 'stepfilled')
    n2, bins2, patches2 = plt.hist(xvalues2, bins=nbins2, edgecolor = "k", color = "royalblue", alpha = 0.8, histtype = 'stepfilled')
    xmin, xmax = plt.xlim(limits)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlabel("Reconstructed energy [GeV]", fontsize = 20)
    plt.ylabel("Number of events", fontsize = 20)
    plt.tick_params(right=True, top=True)
    plt.minorticks_on() 
    plt.tick_params(axis="both",which = "both", direction="in")
    plt.annotate(label, xy=(0.9, 0.91), xycoords='axes fraction', fontsize = 24, alpha = 0.8)
    plt.show()
    plt.savefig("Reconstructed_energy.png")
    return n, bins, n2, bins2


# Main program #
particleChoice = input("Choose particle, (a) antimuon, (b) positron, (c) proton \n") # Choose particle and assign limits, labels and input files
if particleChoice == "a":
    infile = "task5a.root"
    label = "$\mu^{+}$"
    limits = [0,2]
    nbins1 = 80
    nbins2 = 150
elif particleChoice == "b":
    infile = "task5b.root"
    label = "$e^{+}$"
    limits = [-2,100]
    nbins1 = 2
    nbins2 = 70
elif particleChoice == "c":
    infile = "task5c.root"
    label = "$p^{+}$"
    limits = [0,80]
    nbins1 = 10
    nbins2 = 70

inf = ROOT.TFile.Open(infile)
tree = inf.Get("B5")
ecal_energy = []
hcal_energy = []

for event in tree: # Main function to plot histograms of each calorimeter and print the total energy
    if event.ECEnergy != 0:
        ecal_energy.append(event.ECEnergy/1000)
    if event.HCEnergy != 0:
        hcal_energy.append(event.HCEnergy/1000)

print(sum(ecal_energy))
print(sum(hcal_energy))

n, bins, n2, bins2 = plotEnergy(hcal_energy, ecal_energy)





