
#Comparative Genomic Analysis of Avian Reovirus Field Strains Against Vaccine Strain S1133
Avian reovirus (ARV) is a segmented double-stranded RNA virus (family Reoviridae) capable of genetic reassortment and mutation, leading to the emergence of new field strains. These genomic changes may affect vaccine efficacy.

This project aims to identify genomic variations—including single nucleotide polymorphisms (SNPs), insertions/deletions (indels), and point mutations—by comparing field strain sequencing data against reference vaccine strains (primarily S1133, along with 2408, 1733, and SS412).

The pipeline processes raw sequencing data, removes host contamination, identifies viral reads, and performs variant calling to characterize genomic differences relevant to vaccine development.

## Data pre-processing:

We will download the raw sequencing data from the Sequence Read Archive(SRA), NCBI. As the sample often contains high levels of host (avian) DNA, the initial quality assessment of the data will be performed using FASTQC. Following that, the reads will be trimmed for adapter sequences, low-quality region, and short reads. Post-trimming quality will again be assessed using FastQC. 

## Mapping

The sequence that maps to the Gallus gallus (chicken) genome will be filtered out. The contigs from the non-host reads and viral contigs will be determined using NCBI-BLAST which will help to find contigs with sequences matching GenBank reovirus sequences. The clean reads will then be aligned with the reference genome. Before mapping, the reference genome will be indexed. The non-host sequences will then be aligned to identified viral contigs to determine the number of viral reads. The gene sequence will be then compared to vaccine strain S1133 full genome. 

## Proposed bioinformatics pipeline

1.	Quality control and trimming: FastQC and Trimmomatic
2.	Alignment and Filtering tools: Bowtie2 or BWA-MEM, Samtools, HiSAT2
3.	Variant calling and assembly: To generate VCF (BCF tools)
4.	Python Analysis Scripts
    a.	Filter VCF files = extract only “High Impact” mutations.
    b.	Automate BLAST/DIAMOND
    c.	Calculate Identity


# Feedback

Your proposed project should create opportunities for you to use scripting to
help automate sequence processing and analyses and make them more reproducible.
[Biopython](https://biopython.org)
might be a useful Python package for your project.
For example, it has
[modules for interacting iwth NCBI's databases](https://biopython.org/docs/latest/Tutorial/chapter_entrez.html).
This could allow you to automate searching for and downloading data from the
SRA.
This is just an idea (not required).

Try to keep your code as general as possible.
For example, it would be ideal of your code can easily be used with other
viruses and hosts.
