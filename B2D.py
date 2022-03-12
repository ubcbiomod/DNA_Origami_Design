import numpy as np

arrScaffold = np.array([7249, 7560, 8064])                                                    # number of nucleotides for the scaffold
numEdges = 3                                                                                  # number of edges
numHelix = 6                                                                                  # number of helices per edge


conversion_factor = 0.332                                                                     # conversion factor length in nm per nucleotide
cfLong = 1/2*np.sqrt(2)                                                                       # conversion factor for long side (edges on axial (y-axis))
cfShort = np.sin(np.pi/numEdges)                                                              # conversion factor for short side (edges on equatorial (x-axis)) 
Diameter_nm = arrScaffold/(numEdges*numHelix*(cfShort+2*cfLong)/conversion_factor)            # diameter in nm
print('Diameter = {}'.format(Diameter_nm))


# Credits to Qiyang Geng and Ethan Rajkumar
