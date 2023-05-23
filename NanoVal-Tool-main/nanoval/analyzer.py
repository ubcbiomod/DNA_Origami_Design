from nanoval.strandlinker import StrandLinker

from pathlib import Path
import pandas as pd
import json
import time

class StrandAnalyzer(StrandLinker):
    '''
    Completed Strand Analyzer, inheriting from StrandLinker class.
    '''
    def __init__(self, design_filepath:Path, sequence_csv:str = None, scaffold_seq_name:str = "p8064") -> None:
        print("PROCESS: Initializing StrandAnalyzer object.")
        super(StrandAnalyzer, self).__init__(design_filepath)
        self.seq_json_path = Path(__file__).parent / "Data/sequences.json"
        self.linked_staple_coords = self.extract_staple_coords()
        self.scaf_name = scaffold_seq_name
        self.scaf_seq = self.read_scaffold_seq()
        self.seqtable = pd.read_csv(sequence_csv) if sequence_csv != None else self.infer_sequences()
    
    def read_scaffold_seq(self) -> str:
        '''
        Reads in built-in/provided .json file containing sequences of DNA origami scaffold vectors.
        '''
        with open(self.seq_json_path) as seq_data:
            seq_data = json.loads(seq_data.read())
            sequence = seq_data[self.scaf_name]['sequence']
        return sequence
    
    def complementary_nucleotides(self, nucleotide:str) -> str:
        '''
        Given a single char in {A, T, C, G}, return the complement nucleotide base. Alternatively, if a sequence of nucleotides
        are provided as a string, returns the complementary sequence in 5' to 3' directionality
        '''
        complement = {
            'A' : 'T',
            'T' : 'A',
            'C' : 'G', 
            'G' : 'C'
        }
        if type(nucleotide) == str and len(nucleotide) == 1:
            try:
                return complement[nucleotide]
            except:
                raise Exception("Invalid base inputted into complement function.")
        elif type(nucleotide) == list or (type(nucleotide) == str and len(nucleotide) > 1):
            complementary_seq = ""
            for nt in nucleotide:
                try:
                    complementary_seq = complementary_seq + complement[nt]
                except:
                    raise Exception("Invalid base inputted into complement function.")
            return complementary_seq[::-1]

    def infer_sequences(self) -> pd.DataFrame:
        '''
        If the csv of staple sequences are not provided by the user, computes the sequences of the staple strands and returns a pandas dataframe
        containing the starting helix and index, the sequence, and the length of the sequence. 
        '''
        start_stamp = time.time()
        scaf_start = self.get_start_nodes('scaf')[0]
        scaffold_coords = self.tracelink_nodes(scaf_start, strand_type = 'scaf', split = False)
        staple_seqs = []
        for staple in self.linked_staple_coords:
            staple_coord_flat = sum(staple,[])
            staple_nucleotide_seq = ""
            five_p_end_address = self.find_node_index(staple_coord_flat[0])
            for nt_node in staple_coord_flat:
                address_dict = self.find_node_index(nt_node)
                paired_scaf_node = self.design_content['vstrands'][address_dict['helix']]['scaf'][address_dict['index']]
                index_along_linear_scaf = scaffold_coords.index(paired_scaf_node)
                staple_nucleotide_seq = staple_nucleotide_seq + self.complementary_nucleotides(self.scaf_seq[index_along_linear_scaf])
            staple_seqs.append(f"{five_p_end_address['helix']}[{five_p_end_address['index']}],{staple_nucleotide_seq},{len(staple_nucleotide_seq)}")
        seqtable = self.format_staple_info(staple_seqs)
        end_stamp = time.time()
        print(f"\nREPORT: --> Sequences inferred in {round(end_stamp - start_stamp, 5)}s\n")

        return seqtable
    
    def format_staple_info(self, staple_seq_str:list) -> pd.DataFrame:
        address = []
        sequence = []
        length = []
        for seq_info in staple_seq_str:
            as_list = seq_info.split(',')
            address.append(as_list[0])
            sequence.append(as_list[1])
            length.append(as_list[2])
        
        seqtable = pd.DataFrame({"Start":address, "Sequence":sequence, "Length":length})

        return seqtable



