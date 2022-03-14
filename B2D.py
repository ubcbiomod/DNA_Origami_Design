import numpy as np

scaffolds = {'M13mp18': 7249, 'p7560': 7560, 'p8064': 8064}                                   # Dictionary of scaffold strands and their lengths

numEdges = int(input("Input the number of edges: "))                                          # number of edges to define n-gonal bipyramidal shape
numHelix = int(input("Input the number of DNA helices per edge: "))                           # number of helices per edge


conversion_factor = 0.332                                                                     # conversion factor length in nm per nucleotide
cfLong = 1/2*np.sqrt(2)                                                                       # conversion factor for long side (edges on axial (y-axis))
cfShort = np.sin(np.pi/numEdges)                                                              # conversion factor for short side (edges on equatorial (x-axis))

for scaffold in scaffolds.keys():
    diameter_nm = scaffolds[scaffold]/(numEdges*numHelix*(cfShort+2*cfLong)/conversion_factor)
    print('Diameter of the spherical {N}-gonal bipyramidal liposome scaffold is {diameter} nm for the {scaf} scaffold {base_len} bases long.'.format(N = numEdges,diameter = diameter_nm, scaf = scaffold, base_len = scaffolds[scaffold]))


# Credits to Qiyang Geng and Ethan Rajkumar and Fumiya Inaba
