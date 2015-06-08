
'''
    Here we will list some tools which come in handy optimizing stochastic 
    functions
'''

import numpy as np
import random as rd
import math


def sample_batch(X, z = None, b = None, r = None, debug = False, adp = None):
	"""
	returns a subset of [N] as a list?

	Parameters:
		N: Size of the original set
		b: parameter for subsample size (e.g. b=.1)
	"""
	
	assert b != None or r!= None, "Choose either absolute or relative sample size!"
	assert (b != None) != (r!= None), "Choose only one: Absolute or relative sample size!"
	N = X.shape[0]
	if b != None:
	    nSamples = b
	else:
	    nSamples = r*N
	if nSamples > N:
	    if debug:
		print "Batch size larger than N, using whole dataset"
	    nSamples = N
	##
	## Draw from uniform distribution
	##
	random_indices = rd.sample( range(N), int(nSamples)) 
	if debug: print "random indices", random_indices
	 
	X_S = np.asarray([X[i,:] for i in random_indices])
	z_S = np.asarray([z[i] for i in random_indices]) if z != None else None
	
	##
	## Count data points
	##
	if adp != None and type(adp) == type(1):
	    adp += nSamples
	
	if debug: print X_S, z_S, adp
		
	   
	if z == None or len(z) == 0:
		return X_S, None, adp
	else: 
		return X_S, z_S, adp

def stochastic_gradient(g, w, X=None, z=None):
	"""
	Calculates Stochastic gradient of F at w as per formula (1.4)
	"""
	(nSamples, nFeatures) = np.shape(X)
	if z is None:
		return np.matrix(sum( [ g(w,X[i,:]) for i in range(nSamples) ] )).T
	else:
		assert len(X)==len(z), "Error: Dimensions must match" 
		return sum([g(w,X[i,:],z[i]) for i in range(nSamples)])