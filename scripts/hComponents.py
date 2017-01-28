#!/usr/bin/env python
import os, pickle, glob, sys
import numpy as np
from pymbar.timeseries import statisticalInefficiency

def doStatistics( filename ):
    array = np.genfromtxt( filename, skip_header = 100 , usecols = 1, dtype = float)
    return np.mean(array), np.std(array) / np.sqrt(len(array)/statisticalInefficiency(array))

def errorPropagation( array ):
    return np.sqrt(np.dot(array,array))

path1 = '/work/cluster/gduarter/freeSolvData/2016_GDRM_freeSolv/u_xvg_h/' #path to original simulations
path2 = '/work/cluster/gduarter/freeSolvData/2016_GDRM_freeSolv/xvg_h_components/' #path to Daisy's simulations
energyConvert = 0.239006 # kJ to kcal

message1 = ''' 
====================================
Calculating potential energy average
<U_u>_u
====================================
'''
message2 = ''' 
====================================
Calculating potential energy average
<U_v>_v
====================================
'''
message3 = ''' 
====================================
Calculating potential energy average
<U_v>_u
====================================
'''

freeSolv = pickle.load(open('../database.pickle'))
molecules = freeSolv.keys()

Uwat, dUwat = doStatistics( os.path.join(path1,"water.xvg") ) 
for molecule in molecules:
    print("Starting job in %s..." % molecule)
    print(message1)
    Uaq, dUaq = doStatistics( os.path.join(path1,"%s.aq.xvg" % molecule) )
    print(message2)
    Uvac, dUvac = doStatistics( os.path.join(path1,"%s.vac.xvg" % molecule) )
    print(message3)
    Uconf, dUconf = doStatistics( os.path.join(path2,"%s.xvg" % molecule) )
    Hsolv = Uaq - Uconf - Uwat
    dHsolv = errorPropagation( np.array([dUaq,dUconf,dUwat]) )
    Hconf = Uconf - Uvac
    dHconf = errorPropagation( np.array( [dUconf,dUvac]) )
    freeSolv[molecule]['h_solv'] = Hsolv*energyConvert
    freeSolv[molecule]['d_h_solv'] = dHsolv*energyConvert
    freeSolv[molecule]['h_conf'] = Hconf*energyConvert
    freeSolv[molecule]['d_h_conf'] = dHconf*energyConvert
    print("h_solv = %.2f +- %.2f" % (freeSolv[molecule]['h_solv'],freeSolv[molecule]['d_h_solv']))
    print("h_conf = %.2f +- %.2f" % (freeSolv[molecule]['h_conf'],freeSolv[molecule]['d_h_conf']))
    print("h_calc = %.2f +- %.2f" % (freeSolv[molecule]['calc_h'],freeSolv[molecule]['d_calc_h']))
    print("Next!\n")


pickle.dump(freeSolv,open('../database.pickle','wb'))


