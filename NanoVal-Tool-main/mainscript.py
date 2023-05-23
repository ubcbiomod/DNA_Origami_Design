import sys 
import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
import time

from nanoval.analyzer import StrandAnalyzer
from tempstat.tempstat import TempStat

def mainscript_fx(savepath:Path, designfile_path:Path = None, sequence_csv:str = None, scaffold_seq_name:str = "p8064", NaConc:int = 50, MgConc:int = 0, dNTPConc:int = 0, oligoConc:float = 0.25) -> None:
    if designfile_path == None:
        if len(sys.argv) > 1:
            design_filepath = Path(sys.argv[1])
            analyzer = StrandAnalyzer(design_filepath, sequence_csv, scaffold_seq_name)
        else:
            root = tk.Tk(); root.withdraw()
            design_filepath = Path(fd.askopenfilename(title = "Select caDNAno design file (.json)"))
            analyzer = StrandAnalyzer(design_filepath, sequence_csv, scaffold_seq_name)
    else:
        analyzer = StrandAnalyzer(designfile_path, sequence_csv, scaffold_seq_name)
    start_stamp = time.time()
    # ----- Visualize staple connectivity vulnerabilities ----- #
    analyzer.visualize_vulnerabilities('all')
    analyzer.summary()
    end_stamp = time.time()
    print(f"Analysis completed in {end_stamp - start_stamp} seconds.")
    # ----- Melting Temperature Statistics ----- # 
    # Lab settings: 
    tempstat = TempStat(savepath, NaConc, MgConc, dNTPConc, oligoConc)
    x_axis, y_axis = tempstat.make_thermal_ramp_plot(analyzer.seqtable)

if __name__ == "__main__":
    mainscript_fx(Path(r"D:\Portfolio\caDNAno-Design-Validation-Tool\caDNAno-Design-Validation-Tool-main\Examples"))