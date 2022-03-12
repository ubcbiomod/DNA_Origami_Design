"""
    Author: Qiyang Geng, Ethan Rajkumar
    Date created: 2022/03/12
    Date last modified: 2022/03/12

    Takes two argument in the case of D2B, the first to indicate D2B, the second to provide the diameter in nm.
"""

import numpy as np
import pandas as pd
import sys

D2B = True if len(sys.argv) > 1 and sys.argv[1] in ['D', 'd', 'D2B', 'd2b'] else False   # mode
nEdges = np.linspace(3, 8, num=8-3+1).astype(int)                                        # number of edges
nHelix = 6                                                                      # number of helices per edge
conversion_factor = 0.664                                                       # conversion factor in nm per nucleotide

print("Mode: " + ("diameter to number of bases." if D2B else "number of bases to diameter."))

if D2B:
    diameter = 100 if len(sys.argv) < 3 else float(sys.argv[2])
    print(f"Diameter: {diameter} nm.")
    longSide = np.ceil(diameter / 2 * np.sqrt(2))          # length of longer edges in nt
    shortSide = np.ceil(diameter * np.sin(np.pi / nEdges) / conversion_factor)    # length of shorter edges in nt
    nBases = (nHelix * nEdges * (longSide * 2 + shortSide)).astype(int)         # number of nucleotides for the scaffold
    # print(f'Number of Bases = {nBases}.')
    print(pd.DataFrame(nBases, columns=["nBases"], index=nEdges)
          .rename_axis("nEdges", axis="columns"))
else:
    lScaffold = np.array([[7249, 7560, 8064]]).T         # length of the scaffold in nucleotides
    cfLong = 1 / 2 * np.sqrt(2)                        # conversion factor for long side (edges on axial (y-axis))
    cfShort = np.sin(np.pi / nEdges)                   # conversion factor for short side (edges on equatorial (x-axis))
    diameter = lScaffold / (2 * nEdges * nHelix * (cfShort + 2 * cfLong) / conversion_factor)    # diameter in nm
    # print(f'Diameter = {diameter.T}.')
    print(pd.DataFrame(diameter.T, columns=[7249, 7560, 8064], index=nEdges)
          .rename_axis("nEdges\\lScaffold", axis="columns"))
