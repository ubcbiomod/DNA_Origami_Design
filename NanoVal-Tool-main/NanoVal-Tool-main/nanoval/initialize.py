import json
from pathlib import Path

class Initializer:
    def __init__(self, design_filepath:Path) -> None:
        self.path = design_filepath
        self.design_content = self.open_caDNAno_json(design_filepath)
        self.make_staple_color_uniform()
        with open(self.path, 'w') as new:
            new.write(json.dumps(self.design_content))
   
    def open_caDNAno_json(self, design_file:Path) -> dict:
        with open(design_file, 'r') as designf_content:
            design_content = json.loads(designf_content.read())
        try:
            assert design_file.suffix == '.json'
            design_content['vstrands']
        except:
            print("Entered filepath does not lead to caDNAno design file")
        
        return design_content
    
    def make_staple_color_uniform(self) -> None:
        vstrands = self.design_content['vstrands']
        for vHelix in vstrands:
            for colors in vHelix['stap_colors']:
                colors[1] = int('00BD19', 16)
