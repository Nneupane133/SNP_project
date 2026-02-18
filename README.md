# Project proposal for Scripting for Biologist:

A study of genomic changes in the field strain of Avian Reovirus compared to the vaccine strain. 

Avian reovirus is a 10 segmented double-stranded RNA (dsRNA) virus belonging to the family Reoviridae. During replications, these genome segmentscan undergo genetic reassortment  and mutate resulting in new strains of Avian reovirus emerging in the field condition. Determining the genomic structure of this field strain is therefore important for vaccine production. The objective of this project is to identify single nucleotide polymorphisms (SNPs), point mutations, insertions/ deletions (indels) in the Avian Reovirus by comparing the field sample sequence against the reference strains, S1133 (primary reference). This strain of ARV, along with 2408, 1733, SS412 are commonly used for vaccine production. 

## Data pre-processing:

We will download the raw sequencing data from the Sequence Read Archive(SRA), NCBI. As the sample often contains high levels of host (avian) DNA, the initial quality assessment of the data will be performed using FASTQC. Following that, the reads will be trimmed for adapter sequences, low-quality region, and short reads. Post-trimming quality will again be assessed using FastQC. 

Mapping

The sequence that maps to the Gallus gallus (chicken) genome will be filtered out. The contigs from the non-host reads and viral contigs will be determined using NCBI-BLAST which will help to find contigs with sequences matching GenBank reovirus sequences. The clean reads will then be aligned with the reference genome. Before mapping, the reference genome will be indexed. The non-host sequences will then be aligned to identified viral contigs to determine the number of viral reads. The gene sequence will be then compared to vaccine strain S1133 full genome. 

## Proposed bioinformatics pipeline

1.	Quality control and trimming: FastQC and Trimmomatic
2.	Alignment and Filtering tools: Bowtie2 or BWA-MEM, Samtools, HiSAT2
3.	Variant calling and assembly: To generate VCF (BCF tools)
4.	Python Analysis Scripts
    a.	Filter VCF files = extract only “High Impact” mutations.
    b.	Automate BLAST/DIAMOND
    c.	Calculate Identity

