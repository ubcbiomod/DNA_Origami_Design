# UBC BIOMOD
### Cadnano python files:
-Diameter Calculator
-Sandwich Checker
-Kinetic Trap


# Documentation

## BACKGROUND
The importance of DNA nanotechnology
Once deemed as a fantasy created by science fiction, the field of nanotechnology has expanded immensely. Introduced in 1986,  K. Eric Drexler’s book allowed for the creation of a multi-billion dollar industry [1]. In 2006, Paul Rothemund introduced DNA origami, a procedure that takes advantage of the intrinsic self-assembling capabilities of DNA to construct complex nanoscale structures [2]. Additionally, DNA origami is now one of the most commonly used techniques in DNA nanotechnology. Paul Rothemund discovered this technique by the mixing of short strands of DNA with specific sequences such that when mixed with a long single-stranded DNA ‘scaffold’, the short strands ‘staple’ the scaffold at precise locations to fold the structure into a predetermined confirmation [2]. 

The introduction to DNA origami revolutionized the current landscape of nanotechnology in applications in fields such as drug delivery, biomedical diagnostics and even in climate change [3, 4, 5]. The customizability and precise controls that DNA origami produces, relative to other technological methods, make it unprecedented and incredibly appealing. 

Crossover principles in the fabrication of 3D DNA nanostructures
DNA nanofabrication using DNA origami often takes a "bottom-up" approach, called self-assembly, which makes use of the physical forces operating at the nanoscale in a certain chemical environment to assemble basic units into larger-scale structures with sub-nanometer precision [6]. Hence, consider a piece of single stranded DNA (ssDNA) as one single unit. Like all 3D structures, an ssDNA has an x, y and z-axis. From the top-down view or the x-axis, the ssDNA resembles a coil-like shape (Figure 1).  


Figure 1. A side view of ssDNA vs. the top-down (X-Axis) view 

Going down the coil, there are geometrical parameters of 0.34 nm per base rise and of 34.3°per base average twist equating to 240° per 7 base pairs [7].  Every set of three 240° rotations results in the coil returning to the same rotational position. This returning position allows the coil to be shown as a reduced representation when translated top to bottom through the x-axis. This reduced representation is a rod called a helice shown in Figure 2. 

                                            Figure 2. Reduced ‘rod-like’ representations of the coil are called helices

Taking the circular cross sections of the rod or the face of the helice, if the twist or the rotations of two non-complementary single strands line up with each other, they can form linkages or crossovers. The phosphate linkages can form crossovers in a semi-circular fashion allowing for the bridging of these ssDNA strands (Figure 3). Figure 3 shows both the reduced representation and the approximate 3D representation of a crossover.



   Figure 3. Crossover occurring at position 5  at both DNA strand 1 and 2 in a semi-circular fashion. 

The formation of crossovers that result from the alignment of the two circular faces is called the crossover principle. This principle forms the basis of DNA nanofabrication through 3D structures. However, some rules exist for this principle such that only certain rotations are thermodynamically favorable. In practice this principle presents thermodynamically favorable crossovers every 240° of rotation. The rod approximation and the crossover principle is often used in DNA origami structural design, which is described in the next section. 

3D DNA origami with Scaffolds and Staples

In this paper, ssDNA is a linear line with squares representing the 5’ end of the DNA and triangles representing the 3’ end. Experimentally, researchers often take ssDNA from a plasmid and use a thermocycler to control the temperatures at which the ssDNA strand folds itself (Figure 4). This strand is called a scaffold. In Figure 4 the strand can computationally be approximated as 6 helices each forming crossovers with each other to form the scaffold. 



 Figure 4. A ssDNA folding itself into a scaffold via its chemical environment.

To ensure that the scaffold maintains its shape, staple strands are added. Staple strands are complementary sequences that can form hydrogen bonds and crossovers to ensure that one scaffold is completely connected to another. These crossovers can result in folding of a 2D structure to a 3D one as shown in Figure 5.

Figure 5. Staple crossovers shown in part a) can fold 2D scaffold  into intermediate b resulting in structure c or can fold directly into structure c. Taken without permission from [6].

The temperature and the presence of staple strands tie together in ensuring the scaffold shape occurs. Additionally, the longer the staple strand’s complementary sequence is, the more likely it will bind to the scaffold kinetically in the presence of high temperatures, forming binding domains. 
# 3D DNA Origami Structure Design with CadNano
Designing and visualizing DNA structures often requires a design software. This paper looks at a software called Cadnano 2.0 which uses 2D representations to represent DNA structures. Furthermore, CanDO, a finite element modeling framework converts the Cadnano 2.0 .json output to produce 3D structures.  Computationally, Cadnano takes helices and forms crossovers to fold the scaffold. Then Cadnano can add the staple strands such that the scaffold can assume its intended conformation (Figure 6). 

	
Figure 6. Cadnano 2.0 interface shown along with the outputs from CanDO. Red indicates low thermodynamic stability and blue indicates high thermodynamic stability. 

Cadnano is generally easy to use once the user understands the concepts behind DNA origami. However, Cadnano doesn’t account for other factors that prevent the folding process of DNA that the user designs in the software such as sandwich staples and kinetic traps. As a result, the user must make manual edits to their sequence. For large and complex structures, these manual edits used to account for the presence of these factors are quite tedious and cumbersome.  

Sandwich Staples: 
Sandwich strands are strands that bind to multiple domains on the scaffold or have crossovers that connect multiple helices together. They are generally characterized as type 1 or type 2 sandwich strands [8]. Type 1 sandwich strands have a long binding domain followed by a crossover, then a shorter binding domain relative to the previous binding domain, followed by another crossover that has a longer binding domain relative to the previous binding domain.  In contrast, type 2 sandwich strands have the same length binding domains separated by a single crossover (Figure 7). 

Figure 7. The two types of sandwich strands: Type 1 and Type 2. 

Type 1 sandwich strands present a structural issue due to the fact that the staple DNA and the scaffold DNA need to form a double helix or “wrap” around each other. When one long binding domain binds first, it is difficult kinetically for the shorter binding domain to bind as shorter sequences of staple strands need to wrap around a shorter stretch of scaffold followed again by a long stretch. In other words if the two longer binding domains bind first in a thermocycler, it will be kinetically impossible for the shorter binding domain to properly bind [9]. Type 2 strands are also an issue as there is no sequential binding of the staple to the scaffold. It is improbable for both binding domains to bind at the same time. Difficulty regarding sandwich strands can leave the user feeling frustrated as they can often result in the shape of the scaffold deformed, relative to the intended conformation. [10]


Kinetic Traps: 
Kinetic traps can also provide issues for DNA nanofabricators. They result from either staple crossovers and scaffold crossovers or staple crossovers and staple crossovers being less than 5 bp away from each other and more than 1 base pair away from each other [9,10,11]. It is often said that a kinetic trap potentially occurs 5 bp away, but that is up to debate [11]. Figure 8 shows a kinetic trap between a staple and a scaffold, which are the most common types of kinetic traps observed in literature. 

    
 Figure 8. A kinetic trap occurs between the red crossover (staple) and the blue crossover (scaffold) due to the smallest distance between the crossover “pairs” (red and red + blue and blue) being less than 5 bp. 

Kinetic traps are an issue because if a scaffold strand bends to make a crossover, a staple strand will have to circumvent or bend around the scaffold to ensure that the crossover occurs. Additionally, there is an “angular strain” on the staple strand and a “steric clash” between the staple and the scaffold strands [11]. This is shown in Figure 9 which is a kinetic trap shown from the cross-section of the crossover’s point of view. Overall, the “tight bending” and “angular strain” cause issues when binding.




  Figure 9.  Cross-section of a crossover showing that the staple strand bend or staple  is less than the scaffold strand bend or  scaffold creating a steric strain for the tightly wound staple strand and a steric clash between the scaffold and the staple due to the fact the staple circumvents around the staple. 


Cadnano cannot account for sandwich strands and kinetic traps. Although there are other programs that researchers use such as Samson Connect which account for structural formation factors, they are both computationally taxing and expensive. This does not bode-well for novice DNA nanofabricators. They must optimize the structure computationally. Then, they test the structure using imaging techniques such as TEM, SEM and AFM. Afterwards, they will optimize the structure computationally again. Finally, they must perform another structural formation confirmation using the aforementioned techniques [10].  Hence the project described in this report is of great use to these novice DNA nanofabricators. 
## PROJECT GOALS
The goal of this project is to develop and describe scripts that will be able to:
Identify the positions of the crossovers, as well as crossover pairs and,
Check for the number and locations of sandwich strands and kinetic traps within a Cadnano .json input.
 These scripts will be posted in an accessible, centralized platform such as GitHub or GoogleDrive. 

## METHODOLOGY
This section describes the methodology of developing the sandwich strand checker and kinetic trap checker code. To better understand the process of development, this paper outlines an introduction to how Cadnano interprets DNA structures, the conditions to develop the kinetic trap checker, and the conditions to develop the sandwich strand checker.

# Cadnano’s .json output:
The structures in Cadnano exist as a .json file in a dictionary format, where the entire output is a single string in the form of sequential identifiers followed by their corresponding lists. Since this string is a dictionary data type, it is possible to cut the string at certain identifiers such as helice numbers, which results in multiple separate strings. Each of these strings contain the information of the different helices. These strings can separate further to extract the lists of coordinates of the staple and scaffold strands, which can be properly converted into a list. In Python, the code uses the following method:

filehandle = open(“filename.json”, “r”)
line = filehandle.readline()

Where “line” is the input as a dictionary in the format:

{“name”: “filename”, “vstrands”: [{“row”: xz, “col”: yz, “num”: z, “scaf”: [[az1,bz1,cz1,dz1],[az2,bz2,cz2,dz2], …],“stap”: [[az1,bz1,cz1,dz1],[az2,bz2,cz2,dz2], …], …}

Here “num” refers to the helice number z, “row” and “col” indicates its (x,y) coordinates in Cadnano’s lattice. The list following “scaf” contains the scaffold coordinates of helice z, and the list following “stap” contains the staple coordinates.

import json
input = json.loads(line)
lis = input[‘vstrands’]

Now the code separated identifiers such as “line” at the term ‘vstrands’ to only yield the the information of the helices, so “lis” is the following nested list:

{[“row”: xz, “col”: yz, “num”: z, “scaf”: [[az1,bz1,cz1,dz1],[az2,bz2,cz2,dz2], …], “stap”: [[az1,bz1,cz1,dz1],[az2,bz2,cz2,dz2], …], …}

These elements contain the information of the helices. “lis” can be further cut down at the terms “num”, “scaf” and “stap” to obtain the helice numbers, list of scaffold coordinates and list of staple coordinates.

As the code sorts these lists into separate lists of scaffold and staple coordinates, these lists are shown in the form [a, b, c, d]. The values in a and c are equivalent to the helice number. The values in b and d are equivalent to the location of a base pair within said helice. Overall, when the two coordinate systems pair up, the data pinpoints a coordinate that expresses three base pairs within a single 2x1 array. [a, b] represents the coordinate of the base pair on the left. [c, d] represents the coordinate of the base pair on the right. Cadnano’s output implies a third implicit coordinate from the two pairs, meant to represent the coordinate of the base pair in between the two pairs. Additionally, directionality is also implied based on the difference of values between [a,b] and [c,d].

If b > d, then the DNA strand’s directionality moves towards the left.      				        (1)
If b < d, then the DNA strand’s directionality moves towards the right. 				        (2)

Furthermore, the input represents crossover strands in the following:

If a =\= c and b =\= -1 and d =\= -1, then the coordinate is representative of a crossover strand.	        (3)

Finally, to initialize or terminate the sequence, a value of [-1, -1] for only a single pair must be recorded, which can be represented as a square for the starting point where Cadnano starts reading, or an arrowhead which indicates Cadnano to terminate the  DNA sequence. Alternatively this can be represented as:

If (a =\= -1 and b =\= -1 or c =\= -1 and d =\= -1) AND (a, b, c, d =\= -1)   			                       (4)

Additionally if [-1, -1] is recorded for both pairs, then a DNA base does not exist in the recorded location.

Kinetic Trap Checker:
The Kinetic Trap Checker is a script written in Python that takes a Cadnano structure encoded as a .json file and outputs the positions of all kinetic traps of the structure, if any.

The input from the .json file is first processed as described in the “Cadnano’s .json output” section above, where the script breaks down the singular string into a nested list whose elements contain the information of each helice.

For every helice, the kinetic trap checker employs a search function, which searches through a list of indices and returns the coordinates of crossover pairs. Two calls to the search function occur. Once for each type of strand: scaffold and staple. For every list the search function reads, it searches through all indices and checks if the position is non-empty and checks if index a or index c is not equal to the principal helice number. Since index a and index c both indicate the helice number that the current strand is on, they should normally either be equal to the principal helice number or -1 if the position is empty. Otherwise, it means the strand crossed over into a different helice, which the value of index a or index c identifies. As previously established, index b corresponds to the coordinate of index a, and similarly index d is the horizontal coordinate for index c. 



Figure 10. For a general sequence of positions x1, x2, x3, x4 and x5 on helice number U with a crossover pair at coordinates [x2,x3] crossing between U and helice number V, it is observed that x1 has the indices [a,b,c,d] = [U,x1,U,x2]. If x2 has the indices [V,x1,U,x3], then x3 has the indices [U,x3,V,x3] and x4 has the indices [U,x4,U,x5]. Alternatively if the crossover pair’s directionality is reversed, then x2 has the indices [U,x2,V,x2] so that x3 has the indices [V,x2,U,x4] and x4 will still have the indices [U,x4,U,x5]. 

A crossover is therefore identified by the condition:

(a =\= -1 AND a =\= principal helice number) OR (c =\= -1 AND c =\= principal helice number)       (5)

Although this is essentially equivalent to statement (3), (5) is the condition used in the script instead.

Whether index a or c in the crossover satisfies the crossover condition depends on the directionality of the crossover (Figure 10). This crossover directionality depends on whether or not the strand at the crossover position originates at the principal helice and crosses over into another helice, or is crossed over into from a foreign helice. Although by visual inspection of Cadnano structures, users can determine that any given pair of adjacent crossovers necessarily have opposite directionality so that if one crossover of a pair satisfied the condition above with its index a, then its partner must have satisfied the crossover condition with its index c (Figure 11). This is because all scaffold strands on a helice must face the same direction, and all staple strands must face the other direction. It is not possible to construct a helice with two scaffold strands facing opposite directions, and likewise for staple strands.


Figure 11. Taking the squares to be the starting points of the strands and the arrows to be the ending points of the strands, it is not possible to have a crossover pair with the same crossover directions, because that would imply the strands on each helice have opposite directionality, in which case the square and arrow is switched for one of the strands. This is impossible, as such a structure simply cannot be constructed.

To set up an approach that makes debugging easier, we can disregard the specific directionality of strands and simply acknowledge that the directionality of adjacent crossovers must be opposite. Denote the left crossover of a crossover pair a left crossover, and analogously for a right crossover, so that crossover pairs consist of adjacent left and right crossovers. The idea is the script identifies a set of all left crossovers and a set of all right crossovers, then checks them against each other to determine crossover parity, because a crossover pair must contain one crossover from each set. In practice, this is not easily implementable as described directly. Instead, the script groups crossovers separately by whether index a or c satisfied the condition of a crossover identification, which is more convenient. Let us henceforth denote these as ‘a’ crossovers and ‘c’ crossovers respectively. This way, crossovers are not uniquely identifiable to be actually “left” or “right” by inspection of indices a and c; rather the script’s concern lies in pairing crossovers that are identified by opposite directionality as determined by indices a and c. The list of ‘a’ crossovers can have a mix of left and right crossovers, and it would be inconsequential because all of their partners are in the other list of ‘c’ crossovers.


Figure 12. Current workflow: identify crossovers by whether their index a or c satisfies the crossover condition. Classify crossovers into these 2 groups, then pair them together.

At every instance that a position has its index a identified to be a crossover, the script appends coordinate b into an empty list, so that there will be a list of coordinates of crossover positions of ‘a’ crossovers. Additionally, the script appends index a into another empty list to generate a list of helice numbers in which the strands cross over into. Note that the index of the helice number list complements the index of the crossover list, so that the nth element of the helice number list is the helice number that the crossover corresponding to the nth element of the crossover coordinate list crosses over into. The setup of these two lists is equivalent to a 2d array, although the 2 lists are separate. The script also performs an identical function for index c and index d to generate analogous lists for ‘c’ crossovers. Now given these lists, the script must identify the crossover pairs. 

For every potential crossover i in one list, the script searches through the list of crossovers in the other list to find a partner j that satisfies the condition:

|bi – cj| = 1  AND  ai = cj          (6)   

If this condition is satisfied, these crossovers are paired together and their coordinates appended to a new list as a pair to generate a list of crossover pair coordinates. Additionally, the script takes the helice numbers corresponding to these crossovers, index a, and appends them to another new list. This new list is a complementary list of helice numbers that the crossover pairs cross into. Again, since the values are appended into these two lists, the nth element of the helice number list is the helice number that corresponds to the nth element of the crossover pair list. 












*Figure 13. Current workflow: From the lists of “a” crossovers and its corresponding b coordinates and “c” crossovers and its corresponding d coordinates, determine crossover parity to generate a new coordinate pair list with complementary helice number list.*

Now since kinetic traps are known to generally only occur between staples and scaffolds or staples and staples, it is necessary to check the list of crossover pairs of all staple strands with itself and also with the list of crossover pairs on the scaffold strand. As the condition for potential kinetic trap formation is a horizontal distance of 5 or less base pairs between neighbouring crossover pairs that cross over into the same helice, the script now needs to check for all crossover pairs in a set, whether there is another crossover pair in the set the script checked against such that the aforementioned conditions hold true. 

For crossover pairs p and q, the condition for a kinetic trap is:

(|bp – dq| ≤ 5  OR  |bq – dp| ≤ 5)  AND  ap = aq  AND  p =/= q         (7)

If yes, then the positions of these two crossover pairs and the helice number are written to a .txt file and identified to be a kinetic trap location.

This algorithm is then looped over all helices, so that the final output in the .txt file are sequential lines of kinetic trap locations. If no kinetic traps are detected, then the phrase “no kinetic traps detected” will be written.


Sandwich Strand Checker:
A sandwich strand checker script in python is one of the goals for this project. The sandwich checker script first reads the .json file from Cadnano, and will output the location of the sandwich strand, the type, and the number of sandwich strands present within the input. 

The script first filters the dict data type in the input to search for all “stap” type inputs. This provides a list of staple coordinates, of which the script searches for two categories: A list of coordinates that represent the squares/arrows and a list of coordinates that represent crossovers. The .json output section explains the numerical representations of squares, arrows, and crossovers. The script performs this sorting with two conditions: In order to find crossovers the script uses the condition in (3). In order to find squares/arrows, the script uses the condition in (4). Similar to the kinetic trap checker, the script separates these categories into another two lists, of which the coordinates are appended into a list representative of the left hand end of DNA called lisofstapLnum. Inversely, the right hand side is called lisofstapRnum. The script now has two lists of which contents are sorted into an overall list that tracks the location of the coordinates for each individual DNA strand.


Figure 14. An example visual representation of the coordinates stored inside lisof__Lnum and lisof__Rnum. 

In order for the script to compare the lengths between two crossover strands, the script must first sort the two lists of coordinates into an order such that the arrays are reordered in the following: The strand initiates with a square coordinate, continues with a crossover coordinate, and terminates with the arrow coordinate. A second condition also applies: The strand “initiates” with a crossover, continues with a crossover, and “terminates” with a crossover. The conditions required for this search are performed with the workflow below.


Figure 15. A generalized workflow of the sandwich checker as it rearranges lisofstap_num into an overall list. 

The script utilizes an initialization condition such that the search starts with a “square” or a “crossover”, the coordinate is appended into a list called Sandwichsort. The script calls a function with Sandwichsort, which appends selected arrays contained in the lisofstap variables into Sandwichsort. The function performs this search until the list is exhausted for each individual DNA strand. Additionally, strands that initialize with a square will always be even in length while strands that initialize with a crossover will be 1 longer than the number of crossovers. Each time these lists are exhausted for a single DNA strand, the script appends the list back into a new list called Sandwichoverall.


Figure 16. An example nested list for Sandwich overall. 

The script can now compare two lengths between a crossover for two lengths in an overall DNA strand (Figure 16). The script performs another iteration to create a new list of information that contains a strand length between crossovers over the list of DNA strands inside the Sandwichoverall strand. The script will also record the location of the helice number and the coordinate of the middle base location. One approach is to create a condition that checks the directionality of which way the strand is moving from (1) and (2). Recall that Sandwichoverall is the location of DNA strands such that only squares, crossovers, and arrows exist, and that Sandwichoverall is ordered in two ways: An initialization with a square, or an initialization with a crossover. With this information, the script assumes two conditions:

If Sandwichoverall[i] is odd, the ith item initializes with a crossover.  (8)
If Sandwichoverall[i] is even, the ith item initializes with a square.     (9)

For even lengths, the script adds or subtracts values of 1 on each side in [c,d] for the ith item and [a,b] for the ith + 1 item depending on determined directionality from (1) and (2) to account for the fact that the middle base location is an implicit value. Following that, we subtract the absolute value between [c,d] of the ith item and [a,b] of the ith + 1 item to obtain the length of a strand. These lengths are saved in 2x1 arrays to compare later in the code called xstap_overall. Additionally, the script records the helice number and implicit base location of each of the pairs of lengths used in the output. 

For odd lengths, the process is similar except the iteration subtracts 1 from Sandwichoverall[i] such that the last item within the DNA strand is ignored.

Finally, the script checks whether or not the lengths of a pair within xstap_overall are either equal to each other, or the first item in the pair is smaller than the second item in the pair. This presents the overall concept on how the script is developed and run. 
RESULTS
The nano hinge is a structure that is created using two stiff arms which allow for purely contrainsed rotations. Two stiff arms were joined along an edge by flexible ssDNA scaffolds which allowed for fine-tuned rotations within 90 ० degrees. This structure can provide the foundations for nanosurgery, and biomedical diagnostics. Figure 17 shows the nano hinge which was initially designed by a team in Ohio State University using mechanical engineering principles. 

Figure 17: A nanohinge juxtaposed with a mechanical hinge

 	A 7-step iteration of the nanohinge was blinded and given to the team members to ensure that the scripts shown below worked properly. 

Kinetic Trap Checker:
A preliminary test was first used on the kinetic trap checker by testing it on 13 simple structures, 3 of which contained generic kinetic trap patterns. The code correctly identified the kinetic trap positions, and made no false positive outputs. Additionally, the code performed more tests  by running it on the nanohinge.


The nanohinge’s structure was optimized by manually finding the kinetic trap positions, then altering the structure to remove the kinetic traps. So far our code has caught every kinetic trap that was manually identified and never output a false positive, thus the code should be sufficiently robust for large and complex structures. For 7 different iterations of the nanohinge, the number of kinetic traps were caught as follows:



Table 1: Number of Kinetic Traps for Each Iteration of The Nanohinge 
File # of “Optimized Iteration of the Nanohinge”
Kinetic Trap Code
(number of kinetic traps) 
Structure size (number of helices)
1
16
185
2
16
185
3
6
55
4
22
35
5
16
35
6
22
71
7
22
55


Structures 1 and 2 are two different versions of the full nano hinge structure, while structures 3-7 are parts of the nano hinge that are of interest with respect to convenient structural analysis via kinetic trap and sandwich strand identification.

Kinetic traps for all 7 structures were first manually identified, and then the kinetic trap code was used which correctly found every kinetic trap with no false positives. It’s notable that conventionally the number of kinetic traps aren’t explicitly determined, rather they are experimentally observed and then gotten rid of quickly as soon as they are found by altering the structure at the kinetic trap sites.

Thus far, the kinetic trap code has not made any known mistakes, but in theory if two crossover pairs are adjacent to one another so as to have 4 crossovers side by side, the code may incorrectly group together crossover pairs, but this is extremely unlikely to occur. The code also does not account for base pair insertions or deletions, which would alter the list of indices and may result in unidentified potential kinetic traps.

Sandwich Checker:

Similar as the kinetic trap checker, the script also used the input from 13 simple structures as a preliminary test. 12 of the 13 contained some form of sandwich strand. From the simple structures, the script doesn’t appear to create any false positives.

Following this check, the script ran the optimized iteration of the nano hinge to check for the number of detected sandwich strands. This paper also compared the script with another Matlab code written by Stephanie Lauback. Lauback wrote a Matlab code that also identified sandwich strands at a time when researchers had not yet identified and classified the main mechanisms of why sandwich strands formed in the first place [11].

Table 2: Comparison of Sandwich Strands Identified by Python Script vs Lauback MATLAB Code [12]
File # of “Optimized Iteration of the Nanohinge”
Sandwich Code 
(number of sandwich strands) 
Matlab Code by Lauback [12]
1
566 (I:181  II: 385)
568
2
567 (I:189 II: 378)
565
3
183 (I: 63 II:120)
187
4
189 (I: 18 II: 171)
187
5
179 (I: 28 II: 151)
181
6
356 (I: 99 II: 257)
358
7
369 (I: 80 II: 289)
372


The counting of sandwich strands are not 100% equivalent between the sandwich checker and Lauback’s code. This may be the result of several reasons. Lauback’s code accounted for different nucleotides, while the sandwich checker did not. Tracking nucleotides in the script allows for the checking of non-specific binding. Focusing on the case of the sandwich checker, when situations such that complementary base pairing can occur between two staple strands, these can also result in sandwich strands [13]. This limitation can result in the undercounting of sandwich strands. Additionally, after looking at the cases with type 2 sandwich strands in the nanohinge, the script showed false positives (Figure 18) which is likely the reason for the cases the script overcounts.


*Figure 18: Example of false positive result. Type 2 sandwich strands that repeat themselves throughout multiple binding domains result in false positives in the blue circle, while the red circles are non false positives.*

Additionally, the script does not account for the variability of breaks in the DNA strand. Lauback’s code determines all of the combinations in which breaks could occur resulting in variability depending on the user and averages them out. The customizability of the break feature results in DNA staple strands that are shorter or longer at specific locations depending on the number of base pairs the user sets up to loop throughout the strand. These breaks can result in under and overcounting of sandwich staples relative to the script. The script appears viable to use due to the miniscule difference between the under and overcounting of sandwich strands. However, unless the exact number of type 1 and 2 sandwich strands remain unknown in Lauback’s code, these results cannot ascertain whether or not the script performs its functionality correctly. Additionally, the nano hinge structure, though representative of a “real life” case, may not be as viable to test compared to looking at simpler cases such as the 13 tests initially performed. However, as a rudimentary sandwich checker, this script proved to be extremely helpful to set as a foundation for ways to check structural issues in a DNA nanostructure.


# CONCLUSION
DNA Origami is a relatively new revolutionary technique with applications in drug delivery, biomedical diagnostics and even in climate change. Cadnano is a program that enacts the customizability and precise controls that DNA origami produces using 2D reduced representations.  Additionally, Cadnano visualizes and designs DNA origami structures while being free and intuitive. However, Cadnano does not check for certain factors such as sandwich staples and kinetics traps which can cause problems in the structures. The goal is to design and code plugins to check for sandwich staples and kinetics traps and share them on Github so that other users of Cadnano 2.0 could use them for free. This paper shows how to interpret data from Cadnano, and provides a method to check for structural issues such as Kinetic Traps and Sandwich Strands using Python scripts. Both the Kinetic Trap and Sandwich Strand Checkers first tested 13 simple structures giving correct outputs, and subsequently tested on 7 different iterations of the nanohinge structure. The Kinetic Trap checker achieved no inaccuracies over the 7 nanohinge iterations. The Sandwich Strand checker was also tested on the nanohinge iterations and its results compared against Stephanie Lauback’s code, showing that the script achieved high Sandwich Strand detection accuracy, barring certain edge cases [12]. The scripts also had some drawbacks; these include the negligence of base pair insertion/deletions, and the negligence of rare edge cases for Kinetic Traps and Sandwich Strands. Additionally, the scripts have laid a foundation for users to build upon this work to improve the script design. Overall, these scripts can considerably help the arduous design process of DNA origami, while being a free, computationally inexpensive alternative to paid software.


























REFERENCES 
[1] Drexler, E. K. Engines of creation;  Anchor Press/Doubleday, 1986

[2] Rothemund, P. W. K. Folding DNA to create nanoscale shapes and patterns. Nature (London). 2006, 440(7082), 297-302. doi:10.1038/nature04586

[3] Zhang, Q. et al. DNA Origami as an In Vivo Drug Delivery Vehicle for Cancer Therapy. ACS Nano. 2014, 8, 7, 6633-6643. https://doi.org/10.1021/nn502058j

[4] Wang, S. et al. DNA Origami-Enabled Biosensors. Sensors (Basel). 2020, 6899. doi:10.3390/s20236899

[5] Zhang, H. et al. DNA nanostructures coordinate gene silencing in mature plants. PNAS. 2019, 116(15), 7543-7548. https://doi.org/10.1073/pnas.1818290116

[6] Whitesides, G. M.; Mathias, J. P.; Seto, C. T. Molecular Self-Assembly and Nanochemistry: A Chemical Strategy for the Synthesis of Nanostructures. Science. 1991, 254, 5036. doi:10.1126/science.1962191

[7] Douglas, S. M.; Dietz, H.; Liedl, T.; Högberg, B.; Graf, F.; Shih, W. M. Self-assembly of DNA into nanoscale three-dimensional shapes. Nature. 2009, 459(7245), 414-418. doi:10.1038/nature08016

[8] Jung, W. H.; Chen, E.; Veneziano, R.; Gaitanaros, S.; Chen, Y. Stretching DNA origami: effect of nicks and Holliday junctions on the axial stiffness. Nucleic acids research. 2020, 48(21), 12407–12414. https://doi.org/10.1093/nar/gkaa985

[9] Glaser, M.; Deb, S.; Seier, F.; Agrawal, A.; Liedl, T.; Douglas, S.; Gupta, M. K.; Smith, D. M. The Art of Designing DNA Nanostructures with CAD Software. Molecules (Basel, Switzerland). 2021, 26(8), 2287. https://doi.org/10.3390/molecules26082287

[10] Fern. J,; Lu, J.; Schulman, R. The Energy Landscape for the Self-Assembly of a Two-Dimensional DNA Origami Complex. ACS Nano. 2016 10(2), 1836-44. DOI:10.1021/acsnano.5b05309

[11] Garcia, H. G.; Grayson, P.; Han, L.; Inamdar, M.; Kondev, J.; Nelson, P. C.; Phillips, R.; Widom, J.; Wiggins, P. A. Biological consequences of tightly bent DNA: the other life of a macromolecular celebrity. Biopolymers. 2007, 85(2), 115–130. https://doi.org/10.1002/bip.20627

[12] Marras, A. E.; Zhou, L.; Su, H.; Castro, C. E. Programmable motion of DNA origami mechanisms. Proceed. of the Nation. Acad. of Scie. 2015, 112(3), 713-718. doi:10.1073/pnas.1408869112

[13] Miller, H. L.; Contera, S.; Wollman, A.; Hirst, A., Dunn, K. E.; Schröter, S.; O'Connell, D.; Leake, M. C. Biophysical characterisation of DNA origami nanostructures reveals inaccessibility to intercalation binding sites. Nanotech. 2020, 31(23), 235605. https://doi.org/10.1088/1361-6528/ab7a2b
ACKNOWLEDGEMENTS
The authors of this paper would like to thank Dr. Thachuk for supporting them with meetings and providing several insights for coding. They would also like to recognize Fumiya “Fumi” Inaba from UBC BIOMOD for collaboration in creation of the nano hinge iterations to work with and the test cases for the kinetic trap and sandwich checker codes. 
