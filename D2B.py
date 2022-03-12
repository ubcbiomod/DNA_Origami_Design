import numpy as np

# Parameters
diameter = 100                                                    # diameter in nm
numEdges = np.array([3,4,5,6])                                                     # number of edges
numHelix = 6                                                      # number of helices per edge


conversion_factor = 0.664                                               # conversion factor in nanometer per nucleotide 
longSide = round(diameter/2*np.sqrt(2), 3)                              # length of longer edges in nt, round to 3 decimal places
shortSide = round(diameter*np.sin(np.pi/numEdges)/conversion_factor)    # length of shorter edges in nt
numBases = numHelix*numEdges*(longSide*2+shortSide)                     # number of nucleotides for the scaffold
print('Number of Bases = {}'.format(numBases))

#Credits to Qiyang Geng and Ethan Rajkumar

