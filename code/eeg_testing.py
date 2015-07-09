
#from multiprocessing import Pool, Process

import itertools


"""
Logistic Regression
"""
from SQN.LogisticRegression import LogisticRegression
from SQN.LogisticRegressionTest import LogisticRegressionTest

from SQN.SGD import SQN, SGD

# from SQN.PSQN import PSQN

import numpy as np
import timeit

import data.datasets as datasets

import sys, random

from SQN import stochastic_tools

"""
SQN
"""

def print_f_vals(sqn, options, filepath, testcase=None, rowlim=None):
    
    t_start = timeit.default_timer() #get current system time
    print("\nSQN, EEG-Dataset\n")
    logreg = LogisticRegression(lam_1=0.0, lam_2=1.0)
    X, y = datasets.load_eeg()
    #sqn.set_start(dim=sqn.options['dim'])
    #sqn.set_start(w1=np.array([ random.randint(-100,100) * random.random() for i in range(sqn.options['dim']) ]))
    sqn.set_start(w1 = np.array([-0.88, 0.05, -0.73, -0.48, -0.36, 0.59, 0.11, -0.93, -0.14, -0.68, -0.27, -0.89, 0.0, -0.14, -0.62, -0.65, -0.37, -0.54, -0.14, -0.91, -0.23, -0.3, 0.48, -1.29, -0.46, -1.38, -0.62, 0.19, -0.47, -0.18, -0.88, -0.07, 0.11, -0.35, -0.28, 0.0, -0.43, -0.75, -0.56, 0.39, -0.53, -0.14, 0.17, -0.11, 0.23, -0.32, -0.15, 0.84, -0.33, 0.75, 0.0, 0.0, 0.56, 0.36, -0.01, 0.01, 0.17, -0.29, -0.61, -0.05, -0.65, -0.04, -0.18, 0.55, 0.0, -0.5, -0.48, 0.09, 0.51, -0.02, -0.92, -0.45, 0.02, 0.56, 0.04, -1.06, -0.36, -0.04, -0.57, -0.07, -0.12, -0.01, 0.13, 0.15, -0.1, -0.19, -0.4, 0.23, -0.04, -0.01, -0.76, 0.42, -0.23, 0.1, 0.0, 0.24, 0.04, 0.24, -0.05, -0.03, -0.09, -0.18, -1.12, 0.2, 0.64, -0.46, -0.42, -0.21, -0.26, 0.12, 0.2, 0.63, 0.0, 0.66, -0.97, -0.15, -0.25, 0.02, 0.66, 0.38, -0.53, -0.77, -0.07, -0.01, 0.37, -0.17, 0.52, 0.58, -1.12, -0.04, -0.87, 0.02, -1.06, 0.63, 0.28, -0.03, 0.01, -0.01, -0.03, -0.32, 0.67, -0.37, 0.0, -0.39, 0.25, 0.95, 0.29, 0.71, 0.01, 0.25, 0.02, 0.0, -0.52, -0.04, -0.49, -0.3, -0.05, -0.29, 0.06, 0.0, -0.02, -0.58, -0.07, 0.19, 0.68, 0.22, 0.11, -0.11, 0.09, 0.15, 0.48, 0.77, 0.04, 0.72, -0.3, 0.25, -0.4, -0.18, 0.51, 1.26, 0.13, 0.26, 0.49, 0.15, 0.54, -0.54, -0.03, -0.05, 0.31, 0.4, 0.1, -0.06, 0.9, -0.37, 0.71, 0.1, 0.36, 0.24, 0.79, 0.0, -0.25, 0.13, 0.08, 0.18, 0.44, -0.07, 0.44, 0.32, 0.94, 0.91, 0.18, 0.39, 0.04, 0.22, 0.59, 0.26, 0.1, 1.13, -0.42, 0.37, 0.38, 0.06, 1.19, 0.31, 0.43, -0.23, 0.71, 0.42, 0.59, 0.39, 0.64, 0.62, 0.18, 0.75, 0.35, 0.01, 1.35, 0.35, -0.32, 1.13, -0.18, -0.02, 0.55, -0.44, -0.07, 0.97, 0.63, 0.46, 0.21, 0.41, 0.28, 0.73, 0.64, 0.25, 0.09, 0.47, 0.5, 0.65, -0.1, 0.85, 0.38, 1.3, 0.0, 0.39, 0.51, -0.84, 0.05, 0.25, -0.19, -0.07, -0.06, -0.85, -0.09, -0.13, 0.81, 0.02, 0.67, 0.71, -0.03, 0.41, 0.3, 0.35, 0.27, -0.25, 0.04, -0.67, 0.12, 0.0, 0.9, -0.52, -0.28, 0.32, -0.21, 0.04, 0.11, 0.08, -0.6, -0.33, 0.32, 0.25, -0.04, -0.83, -0.23, 0.59, -1.28, -0.42, 0.09, 0.43, 0.19, -0.6, -0.98, -1.07, 0.83, 0.08, -0.14, -0.38, -0.26, -0.21, -0.16, -0.9, -0.25, -0.27, -0.34, -0.58, -0.15, -0.18, 0.03, -0.17, 0.27, 0.09, -0.09, -0.76, -0.43, -0.96, -0.59, -0.61, 0.2, 0.62, -0.28, 0.21, 0.21, -0.39, 0.12, -0.27, -0.22, -0.54, 0.53, 0.08, -0.52, -0.01, -0.19, -0.07, -0.71, 0.07, 0.37, -0.34, 0.03, -0.37, -0.26, 0.28, -0.16, 0.25, -0.05, -0.11, -0.1, -0.01, 0.0, -0.05, -0.49, 0.63, 0.28, -0.16, -0.83, 0.02, 0.13, -0.03, 0.06, 0.12, -0.02, -0.12, 0.36, 0.17, -0.28, 0.91, 0.47, -0.14, 0.15, 0.37, -0.4, -0.12, -0.15, 0.05, 0.43, 0.01, 0.52, -0.42, -0.49, 0.57, 0.06, 0.34, 0.12, 0.41, -0.34, 0.15, 0.18, 0.14, -0.51, -0.2, -0.06, -0.65, -0.87, -0.69, 0.64, -0.01, 0.53, 0.08, 0.41, -0.13, 0.73, 0.38, 0.0, 0.18, 0.05, 0.82, 0.53, 0.58, 0.45, 0.17, -0.01, 0.14, 0.03, -0.05, -0.29, 0.26, -0.3, 0.21, -0.61, 0.06, -0.41, 0.31, -0.05, 1.23, 0.04, 0.17, 0.0, -0.14, 0.36, -0.04, 0.03, 0.37, 0.82, 0.62, 0.03, 0.37, 0.03, 0.48, 0.02, 0.73, -0.03, -0.2, 0.0, 0.16, -0.57, -0.15, 0.1, 0.54, 0.04, -0.08, 0.15, 0.12, -0.1, 0.39, 0.23, 0.17, -0.22, -0.08, 0.2, 0.27, -0.85, -0.14, -0.15, -0.38, -0.41, 0.74, -0.09, 0.58, -0.27, 0.24, 0.5, 0.08, 0.95, 0.35, -0.25, 0.22, 0.94, 0.17, 0.8, 0.21, 0.79, 0.9, 0.87, -0.35, 0.41, 0.2, 0.54, 0.89, 0.13, -0.61, 0.05, 0.79, 0.8, 0.11, -0.06, -0.28, 0.68, 0.42, -0.65, 0.54, -0.15, 0.13, -0.03, 0.73, -0.07, 0.59, 0.1, 0.22, 0.05, 0.36, 0.42, -0.02, -0.4, -0.22, 0.37, 0.95, 0.7, 0.02, -0.01, -0.72, 0.68, 0.12, -0.4, -0.05, -0.44, -0.65, -0.75, 0.16, -0.67, 0.57, -0.69, 0.89, -0.08, -0.19, -0.43, 0.48, 0.12, 0.12, -0.67, -0.11, -0.07, 0.0, -0.55, 0.47, -0.19, -1.1, 0.11, -0.14, 0.09, -0.31, 0.65, -0.27, -0.19, -0.15, -0.55, -0.74, -0.06, 0.19, 0.23, -0.28, -0.11, -0.67, -0.12, -0.21, -0.66, -1.16, -0.9, 0.02, 0.01, -0.66, -0.45, -0.88, -0.23, -0.34, -0.59, -0.47, -0.37, -0.4, -0.13, -0.65, -0.37, 0.46]))
    w = sqn.get_position()
    
    sqn.set_options({'sampleFunction': logreg.sample_batch})
    
    if filepath is not None:
        ffile = open(filepath, "w+")
        wfile = open(filepath+"_w.txt", "w+")
    
    sep = ","
    results = []
    locations = []
    f_evals = []
    for k in itertools.count():
        
        if filepath is not None:
            if len(results) > 0: 
                    line = sep.join([ str(r) for r in results[-1] ])[:-1] + "\n"
                    ffile.write(line)
            wfile.write(sep.join(["0.2%f" %l for l in w.flat[:]]) + "\n")
        else:    
            print(k, logreg.adp, "%0.2f, %0.2f" % (float(sqn.f_vals[-1]), float(sqn.g_norms[-1])))
            
            
        w = sqn.solve_one_step(logreg.F, logreg.G, X, y, k=k)
        
        #X_S, z_S = sqn._draw_sample(b = 100)
        #f_evals.append(logreg.F(w, X_S, z_S))
        #print(np.mean(f_evals))
        
        #if k%20 == 0 and sqn._is_stationary():
        #        print sqn._get_test_variance()
      #          print sqn.options['batch_size'], sqn.options['batch_size_H']
   #             if sqn.options['batch_size'] <= 1e4 and sqn.options['batch_size_H'] < 4e3:
#                    sqn.set_options({'batch_size': sqn.options['batch_size']+1000, 'batch_size_H': sqn.options['batch_size_H']+400})
                
        
        results.append([k, logreg.fevals, logreg.gevals, logreg.adp, sqn.f_vals[-1], sqn.g_norms[-1], timeit.default_timer()-t_start])
        locations.append(w)
        
        if k > sqn.options['max_iter'] or sqn.termination_counter > 4:
            iterations = k
            break
    if filepath is not None:
        ffile.close()
        wfile.close()
    
    return results


def benchmark(batch_size_G, batch_size_H, updates_per_batch, options):
        folderpath = "../outputs/eeg/"
        filepath =  folderpath + "%d_%d_%d.txt" %(b_G, b_H, updates_per_batch)
        options['batch_size'] = b_G
        options['batch_size_H'] = b_H
        options['updates_per_batch'] = updates_per_batch
       # if batch_size_H == 0:
         #       sqn = SGD(options)
            #    print "SGD"
        #else:
        sqn = SQN(options)
        print_f_vals(sqn, options, filepath)

"""
Main
"""
if __name__ == "__main__":
    
        """
        Runs SQN-LogReg on the Higgs-Dataset,
        which is a 7.4GB csv file for binary classification
        that can be obtained here:
        https://archive.ics.uci.edu/ml/datasets/HIGGS
        the file should be in <Git Project root directory>/datasets/
        """
        options = { 'dim':600, 
                            'L': 10, 
                            'M': 5, 
                            'beta':5., 
                            'max_iter': 1000, 
                            'batch_size': 100, 
                            'batch_size_H': 0, 
                            'updates_per_batch': 1, 
                            'testinterval': 0
                        }
        
        
        import sys
        if len(sys.argv) > 1:
                print sys.argv
                b_G, b_H = int(sys.argv[1]), int(sys.argv[2])
                updates_per_batch = 1
                if len(sys.argv) > 2:
                        options['max_iter'] = int(sys.argv[3])
                benchmark(b_G, b_H, updates_per_batch, options)
        else:
                batch_sizes_G = [100, 1000]#, 10000]        
                batch_sizes_H = [0, 100]#, 1000]
                updates_per_batch = 1
                
                for b_G in batch_sizes_G:
                        for b_H in batch_sizes_H:
                                p = Process(target=benchmark(b_G, b_H, updates_per_batch, options))
                                p.start()
                
    