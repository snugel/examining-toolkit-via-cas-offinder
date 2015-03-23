Examining toolkit of potential off-target sites via Cas-OFFinder
==

We used Cas-OFFinder, a web-based program accessible at (http://www.rgenome.net/cas-offinder/) to list potential off-target sites that differed from on-target sites by up to 8 nucleotides or that differed by 2 nucleotides with a DNA or RNA bulge. We developed a computer program to compare sequence reads aligned around each of the resulting hundreds of thousands of potential off-target sites with the reference sequence.

Instructions
--

1. To find most common cigar string near the target site, run
   
   `python 1.find_most_common_cigar.py [Reference] [BAM_File] [threshold=0]`
   
   example of [Reference] is HS_gene_library.txt

2. To see differences between the two output files, run
   
   `python 2.compare_cigar.py [Output_WT] [Output_RGEN]`
