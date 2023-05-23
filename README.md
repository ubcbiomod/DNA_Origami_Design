# UBC BIOMOD's Cadnano2.0 Repo
<p align="center">
<img src="https://user-images.githubusercontent.com/61441923/162942506-541854b0-2b55-437b-8d8c-7ad454fa6090.png">
</p>


## Team Member Contribution
### Primary Author
Ethan Rajkumar 

### Developers
Fumiya Inaba \
Qiyang Geng 

## Special Thanks to
Rickey Lee  \
Soresu Juyo \
Charlie Sushams \
Melanie Law \
Stephanie Nyugen \
Rajeshwar Lally 

## Purpose
The 2022 BIOMOD Directory was done by Ethan Elliot Rajkumar as part of his contribution to the 2022 nanohinge project.

The 2023 BIOMOD Directory was developed by Ethan Elliot Rajkumar, Qiyang Geng, and Fumiya Inaba as part of the 2023-2024 enzymosome project. 

The CadNAno-VALidation (NANOVAL) tool was developed by Fumiya Inaba, Ethan Elliot Rajkumar, and Qiyang Geng for ease of use. 

To centralize our python code in one github repo. We also hope to share the NanoValidation tool with Shawn Douglas, so we can possibly integrate the existing code with the current CADNANO GUI. 

## Documentation: 

To get our thought process behind our python files, please consult the following masterlog: 
https://docs.google.com/document/d/1j4pZxjeS6DUqvh8vKzby_XLvqkQkB3oTLp5f8Ao7lFQ/edit?usp=sharing

## NANOVAL Documentation: 
**Note**: Curently this tool is run from the terminal/cmd, but the eventual goal of this project will implement a GUI, also providing more informatics such as suggested thermal annealing ramp, basic staple stand statistics etc. 


## Team Member Contributions: 
### Primary Author
Fumi Inaba

### Developers 
Ethan Elliot Rajkumar \
Qiyang Geng


## Prerequisites
This documentation assumes basic knowledge of caDNAno2, and DNA origami concepts including thermodynamics, structure, design etc.   
Users should be familiar with the caDNAno2 interface and the representations of staple/scaffold strands.

## Introduction
caDNAno is a very popular tool for computer-aided DNA origami design. This project aims to analyze caDNAno design files (.json), identifying potentially problematic staple strands such as 'kinetic traps', or 'sandwich strands', a term coined by Dr.Stephanie Lauback. The inclusion of such strands in the design are thought to affect parameters of the DNA origami structure formed in the lab such as stability and formation yield. This tool was developed for the DNA origami design pipeline at UBC BIOMOD.

## Usage  
### Dependencies  
```
numpy >= 1.23.0
```  
### Workflow
After users have a design file exported from caDNAno2, users can analyze their designs for staple strands which may be potentially problematic to the formation of the structure <i>in vitro</i>. These strands are explained in the <a href = "#bg">Background</a> section below.   
#### First Steps
Users should first clone or download the repository. To get the full functionality of this program, users should complete the following two steps.  
1. Setup SciTools API access and get their own IDT API access credentials - [learn how here.](https://www.idtdna.com/pages/tools/apidoc)
2.  Input IDT API credentials into <i>idt_api_credentials_template.json</i> and rename the file to <i>idt_api_credentials.json</i>.

To make an IDT (Integrated DNA Technologies) account and set up API access, follow the link to the SciTools Plus API Overview Docs [here](https://www.idtdna.com/pages/tools/apidoc). Once the SciTools API access is set up, users should edit the <i>idt_api_credentials_template.json</i> file with their API access details, and rename that file to <i>idt_api_credentials.json</i>. Program functionality relevant to staple strand melting temperature <b>will not work</b> if the above has not been completed.  

Users should run the following command from the location where this program is downloaded. Replace <i>"download_location"</i> with the path where this repository is downloaded.

```
C:\Users\username\download_location> python mainscript.py path\to\design\file.json
username@macos download_location ~ % python3 mainscript.py path/to/design/file.json
username@ubuntu download_location ~ $ python3 mainscript.py path/to/design/file.json
```
Providing the path to the caDNAno design file when running the script from terminal is optional. If it is not provided, the script will display a prompt where users can browse through their filesystem to search for the design file to analyze.  
```
C:\Users\username\download_location> python mainscript.py
username@macos download_location ~ % python3 mainscript.py
username@ubuntu ~ $ python3 mainscript.py
```

Once the analysis is complete, users can reopen the design file on caDNAno2, and will see that the problematic strands are colored red, while the others are colored green. The script also outputs a text file <i>name_of_design_file_summary</i>.txt, with the date and time of the analysis, along with the coordinates fo the problematic strands provided in the format <b>"helix_number[longitudinal_index]"</b>. Sample analyses files and results are available in the Examples folder.  

Additionally, a histogram of the melting temperatures of staple strands in 1<sup>o</sup>C wide bins will be saved. Finally, the 

<div id = 'bg'>
<h2>Background</h2>
DNA Origami nanostructures are formed typically using one long 'scaffold' DNA strand (3000 - 8000 bp) and hundreds of smaller 'staple' DNA strands (24 - 64 bp) which bind to specific regions of the scaffold strand, holding it in a programmable structure/conformation. 
<br><br>
An important concept in the formation of DNA origami structures are 'cross overs'. This is when a single DNA strand in a double-stranded DNA (dsDNA) double helix crosses over from one dsDNA helix to another, resulting in one DNA strand being a part of two or more double helices. 
</div>

