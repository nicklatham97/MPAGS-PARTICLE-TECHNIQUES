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

# Constants #
B = 0.5 # Magnetic field strength of 0.5 T
q = 3*(10**8)/(10**9) # Muon electric charge (GeV)
L = 2.0 # Length of magnetic field chamber
dz = 0.5 # Drift chamber wire separation distances

def fit(m,x,c): # straight line function (y=mx+c) to plot reconstructed xz-plane track
    return m*x+c

def trackReconstruction(event, chamber):
    if chamber == 1:
        xz_pos = [event.Dc1HitsVector_z,event.Dc1HitsVector_x]
    elif chamber == 2:
        xz_pos = [event.Dc2HitsVector_z,event.Dc2HitsVector_x]
    coordinates = []
    for i in range(len(xz_pos[0])):
        coordinates.append([xz_pos[0][i]*dz, xz_pos[1][i]/1000])
    def fit(next):
        nextx = 0
        for z,x in coordinates:
            xp = next[0]*z+next[1]
            nextx += (x-xp)**2 
        return nextx
    m = (coordinates[-1][1]-coordinates[0][1])/(coordinates[-1][0]-coordinates[0][0])
    c = coordinates[0][1] 
    min = opt.minimize(fit, x0=[m,c])
    m = min["x"][0]
    c = min["x"][1]

    return m, c

def determineMomentum(m1,c1,m2,c2):
    sigma = math.atan((m2-m1)/(1+m1*m2))
    dx = abs((m1*(4.5)+c1)-(m2*(-2)+c2))
    return (B*q*math.sqrt(L**2 + dx**2))/sigma

def plotMomenta(momenta):
    n, bins, patches = plt.hist(momenta, bins=40, edgecolor = "k", color = "royalblue", alpha = 0.8)
    xmin, xmax = plt.xlim()
    mu, std = norm.fit(momenta)
    x = np.linspace(xmin, xmax, 1000)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, color='none')
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlabel("Reconstructed momentum [GeV]", fontsize = 20)
    plt.ylabel("Number of events", fontsize = 20)
    plt.minorticks_on() 
    plt.tick_params(axis="both",which = "both", direction="in")
    plt.axvline(mu, color='k', linewidth=1, linestyle = "dashed")
    plt.annotate("$\mu$ = " + str(round(mu,1)) + "\n" + "$\sigma$ = " + str(round(std,2)), xy=(0.76, 0.85), xycoords='axes fraction', fontsize = 18)
    plt.show()
    plt.savefig("Reconstructed_momentum.pdf")
    return n, bins

inf = ROOT.TFile.Open("out_1.root")
tree = inf.Get("B5")
p = []
for event in tree:
    if len(event.Dc1HitsVector_x)==5 and len(event.Dc2HitsVector_x)==5:
        m1,c1 = trackReconstruction(event, 1)
        m2,c2 = trackReconstruction(event, 2)
        recMom = determineMomentum(m1,c1,m2,c2)
        if abs(recMom)<200: p.append(abs(recMom))
n, bins = plotMomenta(p)



