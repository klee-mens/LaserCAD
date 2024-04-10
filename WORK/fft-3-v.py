#!/usr/bin/python3
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# import sys
# sys.path.append("E:\Program Files\Spyder\pkgs")

# from sys import argv
import numpy as np
from scipy.special import factorial 
#from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
#%matplotlib inline
# plt.rc('text', usetex=True)
plt.rc('font', size=20)
# plt.rc('font', family='serif', serif='dc', size=20)
pltadj = {'top':0.88, 'bottom':0.15, 'right':0.9}
lwhigh = 0.7
subfolder = 'yGraph'
# import importlib
# try:
#   labs = importlib.import_module(subfolder+'.labels')
# except:    
class labs:
    iinau = '$I$ / a.u.'
    eiinau = '$E,\,I$ / a.u.'
    tginfs = '$t_\mathrm {g}$ / fs'
    phirad = '$\phi $ / rad'
    vphirad = '$\varphi $ / rad'
    finthz = '$f$ / THz'
    tauinfs = '$\\tau$ / fs'
    tinfs = '$t$ / fs'

a= ["",'20','gfa',0,0,5000,0]
argv=a

# <codecell>

tau = np.float64(argv[1])
phi = np.array(list(map(np.float64,argv[:2:-1]))) 
phip = np.poly1d(phi/factorial(range(len(phi)-1,-1,-1)))
myvars=[['fstau', tau, 'fs', 0]]
if len(phi)>0: myvars.append(['fsphia', phi[-1], '', 0]) 
if len(phi)>1: myvars.append(['fsphib', phi[-2], 'fs', 0])
myvars.extend([ ['fsphi'+chr(ord('a')+i), phi[-1-i], 'fs^'+str(i), 0] \
       for i in range(len(phi)) if i>1] )
figures = []

# <codecell>

c = 299792458.0 
T = 800.0 / c * 10**6
f = 1 / T
omega = 2 * np.pi / T

# <headingcell level=1>

# Frequency Space

# <headingcell level=2>

# <codecell>

if 'g' in argv[2]:
    # gauss
    wscale     = 2*np.log(2)
    ftscale    = 2*np.sqrt(np.pi/wscale)
    sigmakoeff = 2*np.sqrt(wscale)
    fscale     = wscale/np.pi 
    def ampfi(x): 
        return np.exp(-wscale*(x)**2)
elif 's' in argv[2]:        
    # sech
    wscale     = 2*np.log(1+np.sqrt(2))
    ftscale    = 2*np.pi/wscale
    fscale     = (wscale/np.pi)**2    
    sigmakoeff = 4*np.sqrt(3)/ftscale
    def ampfi(x): 
        return 1/np.cosh(wscale*x)
else:
    quit()

# <codecell>

# <headingcell level=2>

df = fscale / tau
myvars.append(['fsdf', 1000*df, 'THz', 0])

# Plot Spectrum

# <codecell>
if 'f' in argv[2]:
    fig1, ax1 = plt.subplots()
    
    axes1 = [ax1, ax1.twinx(), ax1.twinx()]
    fig1.subplots_adjust(**pltadj)

    #y-Axes
    poslist = ['top', 'left', 'right']
    axalign = ['left', 'right', 'left']
    axpos   = [0, 0.75, 1]
    colors  = ['black', 'red', 'blue']
    labels  = [labs.iinau, labs.tginfs, labs.phirad, labs.finthz]
    for k in range(3):
        axes1[k].patch.set_visible(False)
        axes1[k].set_frame_on(True)
        for pos in poslist:
            axes1[k].spines[pos].set_color('none')
        axes1[k].spines[axalign[k]].set_position(('axes', axpos[k]))
        axes1[k].spines[axalign[k]].set_color(colors[k])
        axes1[k].tick_params(axis='y', colors=colors[k])
    #    axes1[k].set_ylabel(labels[k], color=colors[k])
        axes1[k].text(axpos[k],1.1,labels[k], horizontalalignment='center',\
        verticalalignment='center',\
        transform=axes1[k].transAxes, color=colors[k])
    
    #x-Axes
    axes1[0].set_xlabel(labels[-1] , color='black')
    axes1[0].xaxis.set_ticks_position('bottom')
    
    #plot ranges
    x = np.arange(-2*df,2*df,df/100)
    x_ = 1000*(x+f)
    axes1[0].set_xlim(1000*(f-2*df), 1000*(f+2*df))

    # indicators
    axes1[0].set_xticks([1000*f-500*df,1000*f+500*df], minor=True)
    axes1[0].xaxis.grid(True, which='minor')
    axes1[0].set_yticks([0.5], minor=True)
    axes1[0].yaxis.grid(True, which='minor')
    # plots
    axes1[0].fill_between(x_, 0, ampfi(x/df)**2, color="green", alpha=0.15);
    axes1[0].plot(x_, ampfi(x/df)**2, color=colors[0], linewidth=lwhigh);
    axes1[1].plot(x_, phip.deriv()(2*np.pi*x), color=colors[1], linewidth=lwhigh);
    axes1[2].plot(x_, phip(2*np.pi*x), color=colors[2], linewidth=lwhigh);
    fig1.fnams = '_gf.pdf'
    # plt.figure()
    # fig1.show()
    figures.append(fig1)

# <headingcell level=1>

# Time Space

# <codecell>

ffakt = 2**8
fbereich = 2**11
tstep = tau/(ffakt*fscale)
tmax = fbereich*tstep
fvrange = np.arange(-1/(2*tstep), 1/(2*tstep), 1/(2*tmax))
frange = 1000*(fvrange+f)
NET = np.fft.fftshift(np.fft.ifft(np.fft.fftshift(ampfi(fvrange/df) \
         * np.exp(-1j * phip(2*np.pi*(fvrange)))))) *ffakt/ftscale
trange = np.arange(-tmax, tmax, tstep)
NETh = np.unwrap(np.angle(NET))
NETArg = NETh-NETh[len(NETh)//2]
NETAbs  = 2 * np.abs(NET)
NET2Abs = np.square(NETAbs) 
NEFDArg = phip.deriv()(2*np.pi*(fvrange))
NETDArg = np.diff(NETArg) / tstep

# <codecell>

def FWHM(xa):
    maxpos = np.argmax(xa)
    maxhw  = xa[maxpos]/2
    fwhma  = np.argmin(np.abs(xa-maxhw))
    xb = xa.copy()
    xb[fwhma] = 0
    fwhmb  = np.argmin(np.abs(xb-maxhw))
    return np.sort(np.array([maxpos,fwhma,fwhmb]))

# <codecell>
# measure pos, width, etc.
magic = 10
MBa = np.average(trange, weights=NET2Abs)
CenterI = np.interp(MBa, trange, NET2Abs)
sig = np.sqrt((np.average(trange**2, weights=NET2Abs) - MBa**2))
VBa = sig * sigmakoeff 
TBa = magic*(np.average(trange**3, weights=NET2Abs)-3*sig**2*MBa-MBa**3)/sig**3  
fwint = FWHM(NET2Abs)
trex = np.arange(MBa+TBa-3*VBa,MBa+TBa+3*VBa,T/30)
NETRe = 2 * np.real(
          (np.interp(trex,trange,np.real(NET))\
      +1j* np.interp(trex,trange,np.imag(NET)))\
                                      *np.exp(1j*omega*trex))

myvars.append(['fst', MBa, 'fs', 1])
myvars.append(['fsdt', VBa, 'fs', 1])
myvars.append(['fsmaxt', trange[fwint[1]], 'fs', 1])
myvars.append(['fsHWB', trange[fwint[2]]-trange[fwint[0]], 'fs', 1])

# <headingcell level=2>

# Plot Intensity and Field

# <codecell>
if 't' in argv[2]:

    fig2, ax2 = plt.subplots()
    axes2 = [ax2, ax2.twinx(), ax2.twinx()]
    fig2.subplots_adjust(**pltadj)
    
    #y-Axes
    poslist = ['top', 'left', 'right']
    axalign = ['left', 'right', 'left']
    axpos   = [0, 0.75, 1]
    colors  = ['black', 'red', 'blue']
    labels  = [labs.eiinau, labs.finthz, labs.phirad, labs.tinfs]
    for k in range(3):
        axes2[k].patch.set_visible(False)
        axes2[k].set_frame_on(True)
        for pos in poslist:
            axes2[k].spines[pos].set_color('none')
        axes2[k].spines[axalign[k]].set_position(('axes', axpos[k]))
        axes2[k].spines[axalign[k]].set_color(colors[k])
        axes2[k].tick_params(axis='y', colors=colors[k])
    #    axes2[k].set_ylabel(labels[k], color=colors[k])
        axes2[k].text(axpos[k],1.1,labels[k], horizontalalignment='center',\
        verticalalignment='center',\
        transform=axes2[k].transAxes, color=colors[k])
    
    #x-Axes
    axes2[0].set_xlabel(labels[-1] , color='black')
    axes2[0].xaxis.set_ticks_position('bottom')
    
    #plot ranges
    xl = np.argmin(np.abs(trange-(MBa+TBa-3*VBa)))
    xr = np.argmin(np.abs(trange-(MBa+TBa+3*VBa)))
    ptrange = trange[xl:xr]
    axes2[0].set_xlim(MBa+TBa-3*VBa,MBa+TBa+3*VBa)
    axes2[1].set_ylim(1000*(f-3*df), 1000*(f+3*df))
    axes2[0].set_ylim(-1,1)
    argmax=np.max(NETArg[xl:xr])
    argmin=np.min(NETArg[xl:xr])
    if argmax-argmin < np.pi:
        axes2[2].set_ylim((argmax+argmin-np.pi)/2,(argmax+argmin+np.pi)/2)
    
    # indicators
    axes2[0].set_xticks([MBa-VBa/2,MBa,MBa+VBa/2], minor=True)
    axes2[0].xaxis.grid(True, which='minor')
    axes2[0].set_yticks([CenterI/2], minor=True)
    axes2[0].yaxis.grid(True, which='minor')
    
    # plots
    axes2[0].fill_between(ptrange, 0, NET2Abs[xl:xr], color="green", alpha=0.15);
    axes2[0].fill_between(ptrange, -NETAbs[xl:xr], NETAbs[xl:xr], color="red", alpha=0.07);
    axes2[0].plot(ptrange, NET2Abs[xl:xr], color=colors[0], linewidth=lwhigh);
    axes2[0].plot(trex, NETRe, color=colors[0], alpha=0.7, linewidth=lwhigh);
    axes2[1].plot(ptrange, 1000*(f+NETDArg[xl:xr]/(2*np.pi)), color=colors[1], linewidth=lwhigh);
    axes2[1].plot(NEFDArg, frange, color=colors[1], linestyle=(0, (10, 10)), linewidth=lwhigh);
    axes2[2].plot(ptrange, NETArg[xl:xr], color=colors[2], linewidth=lwhigh);
    fig2.fnams = '_gt.pdf'
    figures.append(fig2)

# <headingcell level=1>

# Autocorrelation

# <codecell>

pistep = 20
phas1 = np.array([np.exp(1j*(n-pistep)/pistep*np.pi) for n in range(2*pistep)])
norma = np.sqrt(1/np.sum(np.square(NET2Abs)))
aet = (np.sqrt(2)*norma)*NET2Abs
bet = (4         *norma)*np.square(NET)
cet = (np.sqrt(8)*norma)*NET
det = NET2Abs * cet
Ampli = 1 + np.correlate(aet, aet, mode='same')
Intera = np.correlate(det,cet,mode='same')+np.correlate(cet,det,mode='same') 
Interb = np.correlate(bet, bet, mode='same') 
InterX = np.real(np.outer(phas1,Intera) + np.outer(np.square(phas1),Interb)) 
top,   bot   = Ampli + [np.real(Interb + Intera), np.real(Interb - Intera)] 
Upper, Lower = Ampli + [np.amax(InterX,axis=0), np.amin(InterX,axis=0)]
fwup  = FWHM(Upper)
fwam  = FWHM(Ampli-1)
textr = np.arange(4.5*trange[fwam[0]],4.5*trange[fwam[2]],T/30)
Inter = np.interp(textr,trange,Ampli)+\
        np.real((np.interp(textr,trange,np.real(Intera))\
             + 1j*np.interp(textr,trange,np.imag(Intera)))\
                                              * np.exp(1j*omega*textr) \
             +  (np.interp(textr,trange,np.real(Interb))\
            + 1j*np.interp(textr,trange,np.imag(Interb)))\
                                              * np.exp(2j*omega*textr) )

myvars.append(['fsi', trange[fwup[2]]-trange[fwup[0]], 'fs', 1])
myvars.append(['fsa', trange[fwam[2]]-trange[fwam[0]], 'fs', 1])

# <codecell>

if 'a' in argv[2]:

    fig3, ax3 = plt.subplots()
    fig3.subplots_adjust(**pltadj)
    
    ax3.patch.set_visible(False)
    ax3.spines['top'].set_color('none')
    ax3.spines['right'].set_color('none')
    ax3.xaxis.set_ticks_position('bottom')
    ax3.set_xlabel(labs.tauinfs)
    #ax3.set_ylabel('I / a.u.')
    ax3.text(0,1.1,labs.iinau, horizontalalignment='center',\
       verticalalignment='center',\
       transform=ax3.transAxes)
    ax3.yaxis.set_ticks_position('left')
    
    #plot range
    ax3.set_xlim(4.5*trange[fwam[0]],4.5*trange[fwam[2]])
    ax3.set_ylim(0, 8)
    
    #indicators
    ax3.set_xticks([trange[fwup[0]],trange[fwup[2]],trange[fwam[0]],trange[fwam[2]]], minor=True)
    ax3.xaxis.grid(True, which='minor')
    ax3.set_yticks([1,2,3,4,8], minor=True)
    ax3.yaxis.grid(True, which='minor')
    
    #plot
    ax3.fill_between(trange, Upper, Lower, color='red', alpha=0.08);
    #ax3.fill_between(trange, Lower, 0, color='blue', alpha=0.15);
    ax3.plot(trange, Upper, color='red', linewidth=lwhigh);
    ax3.plot(trange, Lower, color='blue', linewidth=lwhigh);
    ax3.plot(trange, top, color='red', alpha=0.5, linewidth=lwhigh);
    ax3.plot(trange, bot, color='blue', alpha=0.5, linewidth=lwhigh);
    ax3.fill_between(trange,0, Ampli, color='green', alpha=0.15);
    ax3.plot(trange, Ampli, color='black', linewidth=lwhigh);
    ax3.plot(textr, Inter, color='black', alpha=0.7, linewidth=lwhigh);
    fig3.fnams = '_gAC.pdf'
    figures.append(fig3)

# <codecell>
fname = subfolder + '/' + str(int(tau))+'_'+argv[2][0]
for i in range(len(phi)-1,-1,-1): fname += '_'+str(int(phi[i]))
# for fig in figures: fig.savefig(fname+fig.fnams, format='PDF')
for fig in figures:
  fig.show()

# <codecell>
myvarsformat='\gdef\{0}{{${1:.{3}f}\,\mathrm{{{2}}}$}}\n'
with open(fname+'_dat.tex', mode='w') as datfile:
    for x in myvars: 
        datfile.write(myvarsformat.format(*x))

#for x in myvars: print('{0}={1:.{3}f} {2}'.format(*x))

# <codecell>

if 'j' in argv[2]:
    
    import json
    
    with open('test.txt', mode='w') as atestfile:
        json.dump([pltadj,myvars], atestfile)
    #    json.dump(myvars, atestfile)
    
    # <codecell>
    with open('test.txt', mode='r') as atestfile:
        astes1, astes2 =json.load(atestfile)

