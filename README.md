
#Comparative Genomic Analysis of Avian Reovirus Field Strains Against Vaccine Strain S1133
Avian reovirus (ARV) is a segmented double-stranded RNA virus (family Reoviridae) capable of genetic reassortment and mutation, leading to the emergence of new field strains. These genomic changes may affect vaccine efficacy.

This project aims to identify genomic variations—including single nucleotide polymorphisms (SNPs), insertions/deletions (indels), and point mutations—by comparing field strain sequencing data against reference vaccine strains (primarily S1133, along with 2408, 1733, and SS412).

The pipeline processes raw sequencing data, removes host contamination, identifies viral reads, and performs variant calling to characterize genomic differences relevant to vaccine development.

## Data Pre-processing

Raw sequencing data were obtained from the NCBI Sequence Read Archive (SRA). Given that field samples typically contain a high proportion of host (Gallus gallus) DNA, an initial quality control (QC) step was performed to assess sequencing quality, base composition, and adapter contamination.

Quality assessment was conducted using FastQC both before and after trimming. Reads were processed to remove adapter sequences, low-quality bases, and short reads using Cutadapt (or Trimmomatic). This step ensured that only high-quality reads were retained for downstream analyses.

Post-trimming QC confirmed improvements in read quality, including reduced adapter contamination and improved per-base sequence quality.

To ensure reproducibility, all preprocessing steps are implemented as Python scripts that automate tool execution and file handling.

## Host Filtering and Viral Read Identification

To remove host contamination, cleaned reads were aligned to the Gallus gallus reference genome using a short-read aligner (e.g., BWA-MEM or Bowtie2). Reads mapping to the host genome were filtered out using SAMtools, and only unmapped (non-host) reads were retained for viral analysis.

The resulting non-host reads were subjected to sequence similarity searches using BLAST against the NCBI nucleotide database to identify viral contigs. This step enabled the detection of reads corresponding to Avian Reovirus and other potential viral sequences.

This filtering strategy ensures that downstream analyses focus specifically on viral genomic content while minimizing host-derived noise.

## Viral Mapping and Reference Alignment

The Avian Reovirus reference genome (S1133 strain) was used as the primary reference for alignment. Additional vaccine strains (2408, 1733, SS412) may also be used for comparative purposes.

Prior to alignment, the reference genome was indexed using BWA or Bowtie2. Non-host reads were then aligned to the viral reference genome to identify viral read coverage and genomic regions of interest.

Aligned reads were processed using SAMtools to generate sorted and indexed BAM files, which were used for downstream variant analysis. 

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
