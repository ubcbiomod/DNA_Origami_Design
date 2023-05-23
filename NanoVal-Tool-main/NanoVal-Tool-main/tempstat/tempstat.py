from tempstat.idtapi import IDTOligoAnalyzer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json

class TempStat(IDTOligoAnalyzer):
    def __init__(self, plot_savepath:Path = None, Na_conc:int = 50, Mg_conc:int = 0, dNTP_conc:int = 0, oligo_conc:float = 0.25):
        super(TempStat, self).__init__()
        self.savepath = plot_savepath / "Results"
        if not self.savepath.exists():
            self.savepath.mkdir(parents = True, exist_ok = True)
        
        if (Na_conc == 50) & (Mg_conc == 0) & (dNTP_conc == 0) & (oligo_conc == 0):
            print("PROCESS: Initialized TempStat object with default settings.")
        else:
            print(f"PROCESS: Initialized tempstat object with settings: \n\t[Na]: {Na_conc}\n\t[Mg]: {Mg_conc}\n\t[dNTP]: {dNTP_conc}\n\t[oligo]: {oligo_conc}")

        self.Na = Na_conc
        self.Mg = Mg_conc
        self.dNTP = dNTP_conc
        self.oligo = oligo_conc

        self.meltemps = []

        self.meltemp_cache_path = Path(__file__).parent / "Data/melting_temps_cache.json"

    def cache_analysis_response(self, response_text:dict) -> None:
        cache_key = f"{self.Na}{self.Mg}{self.dNTP}{self.oligo}{str(response_text['Sequence']).replace(' ', '')}"
        with open(self.meltemp_cache_path, 'r') as cache_f:
            cache_f = cache_f.read()
            if cache_f == "":
                cache = {}
            else:
                cache = json.loads(cache_f)
        cache[cache_key] = response_text
        
        with open(self.meltemp_cache_path, 'w') as cache_w:
            cache_w.write(json.dumps(cache, indent = 4))

        return None

    def search_mt_in_cache(self, cache_key:str) -> bool:
        with open(self.meltemp_cache_path, 'r') as cache_f:
            cache_f = cache_f.read()
            if cache_f == "":
                return False
            else:
                cache = json.loads(cache_f)
        try:
            melting_temperature = cache[cache_key]['MeltTemp']
            return melting_temperature

        except KeyError:
            return False

    def get_melt_temp(self, oligo_sequence:str) -> float:
        '''
        Settings/parameters such as [Na+] and [dNTP] should be set upon initialization of the TempStat object. If custom settings are desired following initialization,
        the object attribute should be reassigned before running this function.
        '''
        cache_key = f"{self.Na}{self.Mg}{self.dNTP}{self.oligo}{oligo_sequence}"
        cache_search = self.search_mt_in_cache(cache_key)
        if cache_search == False:
            oligo_analysis_result = self.post_analyzer_request(oligo_sequence, self.Na, self.Mg, self.oligo, self.dNTP)
            self.cache_analysis_response(oligo_analysis_result)
            melt_temp = oligo_analysis_result['MeltTemp']
        else:
            melt_temp = cache_search

        return melt_temp
    
    def seq_temp_analyses(self, seqtable:pd.DataFrame) -> pd.DataFrame:
        sequences = seqtable['Sequence']
        melting_temps = []
        for sequence in sequences:
            melttemp = self.get_melt_temp(sequence)
            melting_temps.append(melttemp)
        seqtable['MeltTemps'] = melting_temps
        frequency, bin_split = np.histogram(seqtable['MeltTemps'], bins = np.arange(np.floor(min(melting_temps)), np.ceil(max(melting_temps)+1), 1))
        seqtable.to_csv(f"{self.savepath}/SeqTable.csv")
        print(f"\n{seqtable}")

        return bin_split, frequency
    
    def compute_thermal_ramp_axes(self, bin_split:np.ndarray, frequency:np.ndarray) -> tuple[np.ndarray]:
        anneal_time_per_strand = 1 # Minutes per strand 
        x_total_min = np.sum(frequency*anneal_time_per_strand) # Get total length of thermal ramp
        x_axis = np.linspace(0, x_total_min, x_total_min) # Get total number of x-points needed  

        y_axis = np.array([]) # Initialize empty y-axis points
        for hist_bin in range(len(bin_split)-1): 
            # The higher the frequency in each histogram bin, the longer the y values stay in that range
            y_points = np.linspace(bin_split[hist_bin], bin_split[hist_bin + 1], frequency[hist_bin] * anneal_time_per_strand, endpoint = True)
            y_axis = np.append(y_axis, y_points)
        y_axis = np.flip(y_axis)

        return x_axis, y_axis
    
    def make_thermal_ramp_plot(self, _seqtable) -> tuple[np.ndarray]:
        bin_split, frequencies = self.seq_temp_analyses(_seqtable)
        x_axis, y_axis = self.compute_thermal_ramp_axes(bin_split, frequencies)
        fig = plt.figure(figsize = (10,8), dpi = 300)
        fig.suptitle("Tempstat - Melting Temperature Statistics", size = 16)
        ax1 = fig.add_subplot(211)
        ax1.set_title("Frequencies of Staple Melting Temperatures in 1C Ranges", size = 14)
        ax1.set_xlabel("Melting Temperature (C)")
        ax1.set_ylabel("Frequency")
        ax1.hist(bin_split[:-1], bin_split, weights = frequencies)
        ax2 = fig.add_subplot(212)
        ax2.set_title("Annealing Ramp Based on Frequencies of Melting Temperatures", size = 14)
        ax2.set_xlabel("Time (min)")
        ax2.set_ylabel("Annealing Temperature (C)")
        ax2.plot(x_axis, y_axis)
        fig.subplots_adjust(hspace=0.5)
        fig.savefig(f"{self.savepath}/Tempstat_Analysis.png")

        return x_axis, y_axis