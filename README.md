# GBK analysis
some python programs to extract data from .gbk files

Promoter Aligner:
Given the gene name (must be an exact match to the /gene=[Name]) will produce an alignment-ready text file containing the DNA code from -100 to the end of the gene, as it’s labelled on the .gbk file.

Genewise Aligner:
Given the gene name (must be an exact match to the /gene=[Name]) will produce the names of the products of the x genes up and downstream of your query. 
Useful for identifying gene insertions or deletions, or finding transposable elements.
