# GBK analysis

Some python programs to extract data from .gbk files


# Description

### <ins> Promoter Aligner:</ins>
Given the gene name (must be an exact match to the /gene=[Name]) will produce an alignment-ready text file containing the DNA code from -100 to the end of the gene, as it’s labelled on the .gbk file.

Searches all .gbk files in the program's directory

inputs: gene name i.e. groL
output: .txt file with >filename-productOfGene (DNA sequence of gene from position[-100] to end, with starting codon capitalized)

ex: result.txt with gene searched groL 

\>mygbkfile.gbk-60 kDa chaperonin
gttgctgctccataacatcaaacatcgacccacggcgtaacgcgcttgctgcttggatgcccgaggcatagactgtacaaaaaaacagtcataacaagccATGaaaaccgccactgcgccgttaccaccgctgcgttcggtcaaggttctggaccagttgcgtgagcgcatacgctacttgcattacagcttaccaaccgaacaggcttatgtccactgggttcgtgccttcatccgtttccacggtgtgcgtcacccggcaaccttgggcagcagcgaagtcgaggcatttctgtcctggctggcgaacgagcgcaaggtttcggtctccacgcatcgtcaggcattggcggccttgctgttcttctacggcaaggtgctgtgcacggatctgccctggcagggcatcaacgaagaccagaacctgggcatcgccatcacccgccgtgcgctggaagccccgctgcgcgccatcgtggccaacgccggtgaagaaccgagcgtgatcgtggccaacgtcaaggccggcgaaggcagctacggctacaacgccgccaccggcgagttcggcgacatgatcgccatgggcatcctggacccgaccaaggtgacccgctcggccctgcagcacgccgcttccgtcgccggccttgcgatcacgaccgaagtggtcgtggccgaagtgccgaagaaggaagagccggccatgccgggtgctggcggtatgggcggtatgggcggcatgggcggcatggatttctga

etc...


### <ins>Genewise Aligner:</ins>
Given the gene name (must be an exact match to the /gene=[Name]) will produce the names of the products of the x genes up and downstream of your query. 
Useful for identifying gene insertions or deletions, or finding transposable elements.

Searches all .gbk files in the program's directory

inputs: gene name i.e. pse1
	depth: the number of genes or products to search for either direction of the gene

output: .csv file with searched gene at position 0, and all found genes/products at positions -depth to depth


# Instructions of use

-Set program in same directory with .gbk files to analyse

-Run program


