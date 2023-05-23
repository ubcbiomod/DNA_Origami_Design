from pathlib import Path
import numpy as np
from nanoval.initialize import Initializer
from copy import deepcopy
import time
from datetime import date, datetime
import json
import sys
sys.setrecursionlimit(8100)

class StrandLinker(Initializer):
    '''
    StrandLinker class linking together linked lists into 'staple' or 'scaffold' strands. Runs analyses while linking the strand components,
    including boolean values whether each linked strand is a sandwich strand, kinetic trap strand or has binding domains which are too short.
    '''
    def __init__(self, design_filepath:Path) -> None:
        super(StrandLinker, self).__init__(design_filepath)
        self.sandwich_addresses = []
        self.kinetic_trap_addresses = []
        self.insufficient_bind_len_addresses = []
        self.staple_analysis_list = self.construct_all_staples()
    
    # -------------------- Staple Node Linking Methods -------------------- # 
    def find_node_index(self, nucleotide_node:list) -> str:
        # Only supports 5' terminus for now
        five_p_helix, five_p_index, three_p_helix, three_p_index = nucleotide_node
        even = three_p_helix % 2 == 0
        if even:
            nt_index = three_p_index + 1
        else:
            nt_index = three_p_index - 1
        return f"{three_p_helix}[{nt_index}]"
    
    def find_node_index(self, nucleotide_node:list) -> dict:
        helix_num, index = 0, 0
        five_p_helix, five_p_index, three_p_helix, three_p_index = nucleotide_node
        if five_p_helix != three_p_helix:
            if five_p_helix == -1:
                helix_num = three_p_helix
                index = three_p_index + 1 if helix_num % 2 == 0 else three_p_index - 1
            if three_p_index == -1:
                helix_num = five_p_helix
                index = five_p_index - 1 if helix_num % 2 == 0 else five_p_index + 1
            if -1 not in nucleotide_node:
                if five_p_helix % 2 == 0:
                    helix_num = three_p_helix
                    index = five_p_index
                else:
                    helix_num = five_p_helix
                    index = three_p_index
        else:
            helix_num = five_p_helix
            index = int(np.mean([five_p_index, three_p_index]))

        return {'helix':int(helix_num), 'index':int(index)}

    def get_start_nodes(self, strand_type:str = 'stap') -> np.ndarray:
        fiveprime_terminis = np.array([[0, 1, 2, 3]], dtype = 'uint8')
        for vHelix in self.design_content['vstrands']:
            stapleHelix = np.array(vHelix[strand_type])
            fiveprime_termini = stapleHelix[(stapleHelix[:, 0] == -1) & (stapleHelix[:, -1] != -1)]
            fiveprime_terminis = np.append(fiveprime_terminis, fiveprime_termini, axis = 0)
        return list(fiveprime_terminis[1:])

    def tracelink_nodes(self, node:list, node_list:list[list] = None, split:bool = True, strand_type:str = 'stap') -> list[list]:
        '''
        Recursively link the nodes (nucleotides) together by finding the next node one by one.
        '''
        linked_nodes = [list(node)] if node_list == None else node_list
        five_p_helix, five_p_index, three_p_helix, three_p_index = node
        next_node = self.design_content['vstrands'][three_p_helix][strand_type][three_p_index]
        linked_nodes.append(next_node)
        if next_node[-1] == -1:
            linked_nodes = self.split_at_xover(linked_nodes) if split else linked_nodes
            return linked_nodes
        else:
            return self.tracelink_nodes(next_node, linked_nodes, strand_type = strand_type, split = split)
    
    def split_at_xover(self, linked_nodes:list) -> list[list]:
        indices = []
        for node in linked_nodes:
            if node[0] != node[2]:
                if linked_nodes.index(node) == 0:
                    continue
                if linked_nodes.index(node) in indices:
                    continue
                if node == linked_nodes[-1]:
                    continue
                indices.append(linked_nodes.index(node)+1)

        linked_nodes = np.split(linked_nodes, indices)
        linked_nodes = [fragment.tolist() for fragment in linked_nodes]

        return linked_nodes
    
    def construct_all_staples(self) -> list:
        '''
        Runs the actual analysis all at once while constructing staples
        '''
        print("PROCESS: Staple linking and analysis start")
        start_stamp = time.time()
        staples = []
        sandwich_strands = []
        kinetic_traps = []
        too_short = []
        fiveprime_termini = self.get_start_nodes()
        for fiveprime_terminus in fiveprime_termini:
            staple = self.tracelink_nodes(fiveprime_terminus)
            is_sandwich = self.check_sandwich(staple)
            is_kinetic_trap = self.check_kinetic_trap(staple, 4)
            is_insufficient_bindlen = self.bind_domain_len(staple, 4)
            staples.append(staple)
            sandwich_strands.append(is_sandwich)
            kinetic_traps.append(is_kinetic_trap)
            too_short.append(is_insufficient_bindlen)
        end_stamp = time.time()
        print(f"\nREPORT: --> Staple strand linked and connectivity analyzed in {round(end_stamp - start_stamp, 5)}s")
        complete_staples =  list(zip(staples, sandwich_strands, kinetic_traps, too_short))

        return complete_staples
    
    def extract_staple_coords(self) -> list:
        staples_with_info = deepcopy(self.staple_analysis_list)
        staple_coords_only = list(list(zip(*staples_with_info))[0])
        return staple_coords_only

    # -------------------- Sandwich Strand Analysis Methods -------------------- #
    def check_sandwich(self, split_staple:list) -> bool:
        lengths = [len(fragment) for fragment in split_staple]
        current_max_length = 0
        descent_started = False
        for length in lengths:
            if descent_started == False:
                if length >= current_max_length:
                    current_max_length = length
                else:
                    descent_started = True
                    current_min_length = current_max_length
            if descent_started == True:
                if length <= current_min_length:
                    current_min_length = length
                else:
                    node_index = split_staple[0][0][3] + 1 if split_staple[0][0][2] % 2 == 0 else split_staple[0][0][3] - 1
                    print(f"INFO: Sandwich Strand detected @ {split_staple[0][0][2]}[{node_index}]")
                    self.sandwich_addresses.append(f"{split_staple[0][0][2]}[{node_index}]")
                    return True
        return False

    # -------------------- Kinetic Trap Strand Analysis Methods -------------------- #                
    def check_kinetic_trap(self, staple_strand_nodes:list[list], scan_size:int) -> bool: 
        xover_nodes = []
        for fragment in staple_strand_nodes:
            end_node = fragment[-1]
            if -1 not in end_node:
                xover_nodes.append(end_node)
        for xover_node in xover_nodes:
            is_kt = self.local_node_scan(xover_node, scan_size)
            if is_kt:
                return True
            
        return False

    def local_node_scan(self, node:list, scan_size:int) -> bool:
        scan_size += 1
        vstrand_map = self.design_content['vstrands']
        five_p_helix, five_p_index, three_p_helix, three_p_index = node
        helix_nums = [five_p_helix, three_p_helix]
        for helix_num in helix_nums:
            node_index = three_p_index 

            for i in range(scan_size+1):
                helix = vstrand_map[helix_num]['scaf']
                upstream_node = helix[node_index - i]
                downstream_node = helix[node_index + i]
                if upstream_node[0] != upstream_node[2]:
                    print(f"INFO: Kinetic Trap detected @ {helix_num}[{node_index}]")
                    self.kinetic_trap_addresses.append(f"{helix_num}[{node_index}]")
                    return True
                if downstream_node[0] != downstream_node[2]:
                    print(f"INFO: Kinetic Trap detected @ {helix_num}[{node_index}]")
                    self.kinetic_trap_addresses.append(f"{helix_num}[{node_index}]")
                    return True
        return False
    
    # -------------------- Check staple binding domain length method -------------------- #
    def bind_domain_len(self, staple_nodes_split:list, minimum_binding_domain_len:int = 4) -> bool:
        binding_domain_lens = np.array([len(fragment) for fragment in staple_nodes_split])
        sufficient_binding = np.uint8(binding_domain_lens <= minimum_binding_domain_len)
        if np.sum(sufficient_binding) >= 1:
            node_index = staple_nodes_split[0][0][3] + 1 if staple_nodes_split[0][0][2] % 2 == 0 else staple_nodes_split[0][0][3] - 1
            helix_num = staple_nodes_split[0][0][2]
            self.insufficient_bind_len_addresses.append(f"{helix_num}[{node_index}]")
            print(f"INFO: Insufficient binding domain length @ {helix_num}[{node_index}]")
            return True
        
        return False

    # -------------------- Post-processing and summary methods -------------------- #
    def visualize_vulnerabilities(self, vulnerability_type:str) -> None:
        match vulnerability_type:
            case 'sandwich':
                condition = 1
            case 'kinetic_trap':
                condition = 2
            case 'binding_len':
                condition = 3
            case 'all':
                condition = None
            case _:
                raise Exception("vulnerability_type parameter must be 'sandwich', 'kinetic_trap', 'binding_len' or 'all'.")

        for staple in self.staple_analysis_list:
            if condition != None:
                if staple[condition]:
                    self.change_color(staple[0])
            else:
                if staple[1] or staple[2] or staple[3]:
                    self.change_color(staple[0])

        with open(self.path, 'w') as to_write:
            to_write.write(json.dumps(self.design_content))
        
        print("Potentially problematic strands have been colored red on caDNAno design file.")
        print("Reload the json file to view those strands. Note not all red-colored strands need to be fixed.")
    
    def change_color(self, single_staple:list[list], to_color:str = 'AF2219') -> None:
        '''
        General implementation -> change color of staple to red if it is potentially problematic
        '''
        _, __, helix_num, node_index = single_staple[0][0]
        if helix_num % 2 == 0:
            node_index = node_index + 1
        else:
            node_index = node_index - 1
        helix_colors = self.design_content['vstrands'][helix_num]['stap_colors']
        for helix_color in helix_colors:
            if helix_color[0] == node_index:
                helix_color[1] = int(to_color, 16)
    
    def summary(self) -> None:
        output_name = f"{self.path.stem}_summary.txt"
        output_path = self.path.parent / output_name
        today = date.today()
        now = datetime.now()
        today_str = today.strftime("%B %d, %Y")
        current_time = now.strftime("%H:%M:%S")

        with open(output_path, 'w') as summary_txt:
            summary_txt.write("caDNAno Design Analysis - Strand Connectivity Analysis:\n")
            summary_txt.write(f"Filename: {self.design_content['name']}")
            summary_txt.write(f"\tAnalysis Date: {today_str}\t")
            summary_txt.write(f"Analysis Time: {current_time}\n\n")

            summary_txt.write("Detected sandwich strands: \n")
            for ss in self.sandwich_addresses:
                summary_txt.write(f"\t{ss}\n")
            summary_txt.write("Detected kinetic traps: \n")
            for kt in self.kinetic_trap_addresses:
                summary_txt.write(f"\t{kt}\n")
            summary_txt.write("Detected insufficient binding domain lengths: \n")
            for short in self.insufficient_bind_len_addresses:
                summary_txt.write(f"\t{short}\n")