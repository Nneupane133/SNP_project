## Comparative Genomic Analysis of Avian Reovirus Field Strains Against Vaccine strain S1133

Avian reovirus (ARV) is a segmented double-stranded RNA virus (family Reoviridae) capable of genetic reassortment and mutation, leading to the emergence of new field strains. These genomic changes may affect vaccine efficacy.

This project aims to identify genomic variations—including single nucleotide polymorphisms (SNPs), insertions/deletions (indels), and point mutations—by comparing field strain sequencing data against reference vaccine strains (primarily S1133, along with 2408, 1733, and SS412).

The pipeline processes raw sequencing data, removes host contamination, identifies viral reads, and performs variant calling to characterize genomic differences relevant to vaccine development.

## Conda environment

Since, most of the scripts that we will be working need external modules. Therefore, we created an conda environment called [SNP-project](https://github.com/Nneupane133/SNP_project/blob/main/environment.yml) which will include all the necessary modules that we will be requiring for this project. 

## Data Pre-processing

Raw sequencing data were obtained from the NCBI Sequence Read Archive (SRA) and were downloaded using [Download_data.py](https://github.com/Nneupane133/SNP_project/blob/main/Download_data.py). An initial quality control (QC) step was performed to assess sequencing quality, base composition, and adapter contamination. 

Quality assessment was conducted using FastQC both before trimming using [FastQC.py](https://github.com/Nneupane133/SNP_project/blob/main/FastQC.py) and after trimming using [Trimmed-FastQC.py](https://github.com/Nneupane133/SNP_project/blob/main/Trimmed_FastQC.py). Reads were processed to remove adapter sequences, low-quality bases, and short reads using Cutadapt with the script [Cutadapt.py](https://github.com/Nneupane133/SNP_project/blob/main/Cutadapt.py). This step ensured that only high-quality reads were retained for downstream analyses.

Post-trimming QC confirmed improvements in read quality, including reduced adapter contamination and improved per-base sequence quality. 

## Host Filtering and Viral Read Identification

Given that field samples typically contain a high proportion of host DNA, cleaned reads were aligned to the Gallus gallus reference genome [Gallus gallus](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000002315.4/) using a short-read aligner (e.g., BWA-MEM) with the script [Map_Chicken.py](https://github.com/Nneupane133/SNP_project/blob/main/Map_Chicken.py). Reads mapping to the host genome were filtered out using SAMtools, and only unmapped (non-host) reads were retained for viral analysis.

## Viral Mapping and Reference Alignment

The Avian Reovirus reference genome (S1133 strain) was used as the primary reference [avian_reovirus.fa](https://github.com/Nneupane133/SNP_project/blob/main/avian_reovirus.fa) for alignment. Additional vaccine strains (2408, 1733, SS412) may also be used for comparative purposes.

Prior to alignment, the reference genome was indexed using BWA [ViralMap.py](https://github.com/Nneupane133/SNP_project/blob/main/ViralMap.py). Non-host reads were then aligned to the viral reference genome to identify viral read coverage and genomic regions of interest [ViralMap.py](https://github.com/Nneupane133/SNP_project/blob/main/ViralMap.py).

Aligned reads were processed using SAMtools to generate sorted and indexed BAM files [ViralMap.py](https://github.com/Nneupane133/SNP_project/blob/main/ViralMap.py), which were used for downstream variant analysis. 

## Variant Calling and Analysis

Variants, including single nucleotide polymorphisms (SNPs) and insertions/deletions (indels), were identified using bcftools [Variantcalling.py](https://github.com/Nneupane133/SNP_project/blob/main/Variantcalling.py). Variant calling was performed on aligned BAM files to generate Variant Call Format (VCF) files.

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

## Limitations and Future Work

## Limitations

- The pipeline is currently optimized for a specific dataset and reference genome, which may limit generalization to other viruses or hosts without modification.  
- Variant calling relies on predefined quality and depth thresholds, which may not capture low-frequency variants accurately.  
- The workflow assumes high-quality input FASTQ files; poor sequencing quality can affect downstream results.  


## Future Work

- Generalize the pipeline to support multiple species, hosts, and reference genomes with minimal user input.  
- Implement advanced variant filtering and annotation steps to improve biological interpretation.    
- Develop visualization modules for SNP distribution, phylogenetic analysis, and comparative genomics.  
- Enhance error handling, logging, and user-friendly command-line interfaces. 
 
## Installation

1. Clone the repository:

```bash
git clone https://github.com/Nneupane133/SNP_project.git
cd SNP_project
```
2. Create and activate environment:

```bash
conda env create -f environment.yml
conda activate SNP_project
```

3. Verify installation:

```bash
python --version
```

4.Tutorial:  Run scripts in the following order

```bash
###Step 1: Download example data
python3 Download_data.py 
### Step 2: Run quality control
python3 FastQC.py 
### Step 3: Trim reads
python3 Cutadapt.py 
### Step 4:  Run quality control on trimmed file
python3 Trimmed_FastQC.py 
### Step 5: Run mapping and variant calling
python3 Map_Chicken.py 
python3 ARVgenome_assembly.py 
python3 ViralMap.py 
python3 Variantcalling.py 
```
## Expected Output:
- viral.sorted.bam
- viral_variants.vcf
- QC reports in fastqc_results/

5. Variant visualization

The file "viral.sorted.bam" file generated during Variantcalling.py can be visualized for SNPs using [Integrative Genomic Viewer](https://igv.org/)


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
