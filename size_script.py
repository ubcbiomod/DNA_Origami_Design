"""
    Author: Qiyang Geng, Ethan Rajkumar, Fumiya Inaba
    Date created: 2022/03/12
    Date last modified: 2022/03/12

    Takes two argument in the case of D2B, the first to indicate D2B, the second to provide the diameter in nm.
"""

import numpy as np
import pandas as pd
import sys

D2B = True if len(sys.argv) > 1 and sys.argv[1] in ['D', 'd', 'D2B', 'd2b'] else False                  # mode
nStart = 3                                                                                              # lower bound for n
nEnd = 6                                                                                                # upper bound for n
nEdges = np.linspace(nStart, nEnd, num=nEnd-nStart+1).astype(int)                                       # number of edges
nHelix = 6                                                                                              # number of helices per edge
conversion_factor = 0.664                                                                               # conversion factor in nm per nucleotide
cfLong = np.pi / 4 * np.ones(nEdges.shape)                                                              # conversion factor for long side (edges on axial (y-axis))
cfShort = np.pi / nEdges                                                                                # conversion factor for short side (edges on equatorial (x-axis))

print("Mode: " + ("diameter to number of bases." if D2B else "number of bases to diameter."))

if D2B:
    diameter = 100 if len(sys.argv) < 3 else float(sys.argv[2])
    print(f"Diameter: {diameter} nm.")
    longSide = np.round(diameter * cfLong / conversion_factor)                                                    # length of longer edges in nt
    shortSide = np.round(diameter * cfShort / conversion_factor)                                                  # length of shorter edges in nt
    nBases = (nHelix * nEdges * (longSide * 2 + shortSide)).astype(int)                                 # number of nucleotides for the scaffold
    # print(f'Number of Bases = {nBases}.')
    print(pd.DataFrame(np.c_[nBases, shortSide, longSide], columns=["nBases", "nShort", "nLong"], index=nEdges)
          .rename_axis("nEdges", axis="columns"))
else:
    lScaffold = np.array([[7249, 7560, 8064]]).T                                                        # length of the scaffold in nucleotides
    diameter = lScaffold / (nEdges * nHelix * (cfShort + 2 * cfLong) / conversion_factor)               # diameter in nm
    # print(f'Diameter = {diameter.T}.')
    print(pd.DataFrame(diameter.T, columns=lScaffold.T[0], index=nEdges)
          .rename_axis("nEdges\\lScaffold", axis="columns"))
