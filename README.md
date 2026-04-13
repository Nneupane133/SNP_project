
#Comparative Genomic Analysis of Avian Reovirus Field Strains Against Vaccine Strain S1133
Avian reovirus (ARV) is a segmented double-stranded RNA virus (family Reoviridae) capable of genetic reassortment and mutation, leading to the emergence of new field strains. These genomic changes may affect vaccine efficacy.

This project aims to identify genomic variations—including single nucleotide polymorphisms (SNPs), insertions/deletions (indels), and point mutations—by comparing field strain sequencing data against reference vaccine strains (primarily S1133, along with 2408, 1733, and SS412).

The pipeline processes raw sequencing data, removes host contamination, identifies viral reads, and performs variant calling to characterize genomic differences relevant to vaccine development.

## Data Pre-processing

Raw sequencing data were obtained from the NCBI Sequence Read Archive (SRA) and were downloaded using [1_download_data.py](https://github.com/Nneupane133/SNP_project/blob/main/1_download_data.py). An initial quality control (QC) step was performed to assess sequencing quality, base composition, and adapter contamination. 

Quality assessment was conducted using FastQC both before trimming using [2_FastQC.py](https://github.com/Nneupane133/SNP_project/blob/main/2_FastQC.py) and after trimming using [4_trimmed-FastQC.py](https://github.com/Nneupane133/SNP_project/blob/main/4_trimmed_FastQC.py). Reads were processed to remove adapter sequences, low-quality bases, and short reads using Cutadapt with the script [3_cutadapt.py](https://github.com/Nneupane133/SNP_project/blob/main/3_cutadapt.py). This step ensured that only high-quality reads were retained for downstream analyses.

Post-trimming QC confirmed improvements in read quality, including reduced adapter contamination and improved per-base sequence quality.  

## Host Filtering and Viral Read Identification

Given that field samples typically contain a high proportion of host DNA, cleaned reads were aligned to the Gallus gallus reference genome [Gallus gallus](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000002315.4/) using a short-read aligner (e.g., BWA-MEM) with the script [5_Map.py](https://github.com/Nneupane133/SNP_project/blob/main/5_Map.py). Reads mapping to the host genome were filtered out using SAMtools, and only unmapped (non-host) reads were retained for viral analysis.

## Viral Mapping and Reference Alignment

The Avian Reovirus reference genome (S1133 strain) was used as the primary reference [avian_reovirus.fa](https://github.com/Nneupane133/SNP_project/blob/main/avian_reovirus.fa) for alignment. Additional vaccine strains (2408, 1733, SS412) may also be used for comparative purposes.

Prior to alignment, the reference genome was indexed using BWA [6_ViralMap.py](https://github.com/Nneupane133/SNP_project/blob/main/6_ViralMap.py). Non-host reads were then aligned to the viral reference genome to identify viral read coverage and genomic regions of interest [6_ViralMap.py](https://github.com/Nneupane133/SNP_project/blob/main/6_ViralMap.py).

Aligned reads were processed using SAMtools to generate sorted and indexed BAM files [6_ViralMap.py](https://github.com/Nneupane133/SNP_project/blob/main/6_ViralMap.py), which were used for downstream variant analysis. 

## Variant Calling and Analysis

Variants, including single nucleotide polymorphisms (SNPs) and insertions/deletions (indels), were identified using bcftools [7_variantcalling.py](https://github.com/Nneupane133/SNP_project/blob/main/7_variantcalling.py). Variant calling was performed on aligned BAM files to generate Variant Call Format (VCF) files.

## SNP visualization

The generated [viral.sorted.bam](https://github.com/Nneupane133/SNP_project/blob/main/viral_results/viral.sorted.bam.gz) file will be analyzed with the [avian_reovirus.fa](https://github.com/Nneupane133/SNP_project/blob/main/avian_reovirus.fa) using the software [Integrative Genomic Viewer](https://igv.org/) to visualize the SNPs.

## Bioinformatics Pipeline Overview

The pipeline consists of the following steps:

1. Download sequencing data from SRA
2. Perform initial quality control (FastQC)
3. Trim adapters and low-quality reads
4. Perform post-trimming QC
5. Map reads to host genome and remove host contamination
6. Identify viral reads using BLAST
7. Align reads to viral reference genome
8. Perform variant calling using bcftools
9. Visualize the SNPs using the software [Integrative Genomic Viewer](https://igv.org/)

Each step is automated using Python scripts to ensure reproducibility and scalability.

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
