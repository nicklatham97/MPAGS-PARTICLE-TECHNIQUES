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

# Arrays and files #
inf = ROOT.TFile.Open("out_1.root")
tree = inf.Get("B5")
ecal_energy = []
hcal_energy = []

def plotEnergy(xvalues): # Plots reconstructed energy as a histogram
    n, bins, patches = plt.hist(xvalues, bins=70, edgecolor = "k", color = "firebrick", alpha = 0.8, histtype = 'stepfilled')
    xmin, xmax = plt.xlim()
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlabel("Reconstructed energy [GeV]", fontsize = 20)
    plt.ylabel("Number of events", fontsize = 20)
    plt.tick_params(right=True, top=True)
    plt.minorticks_on() 
    plt.tick_params(axis="both",which = "both", direction="in")
    plt.annotate("$\mu^{+}$ ECal", xy=(0.75, 0.91), xycoords='axes fraction', fontsize = 24, alpha = 0.8)
    plt.show()
    plt.savefig("Reconstructed_energy.png")
    return n, bins

for event in tree: # Main function to run
    ecal_energy.append(event.ECEnergy)
    hcal_energy.append(event.HCEnergy)

n, bins = plotEnergy(ecal_energy)



