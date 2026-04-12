#!/usr/bin/env python3
import os
import subprocess


def run_viral_map(input_dir="refmap_results", output_dir="viral_results",
                  sample_id="SRR12620879", reference_fasta="avian_reovirus.fa",
                  threads=2):
    """Map unmapped paired-end reads to the avian reovirus reference genome.

    This function takes unmapped reads from a previous reference mapping step,
    aligns them to a viral reference genome using BWA-MEM, converts the output
    to BAM format, sorts and indexes the BAM file using samtools.

    Parameters
    ----------
    input_dir : str
        Directory containing unmapped paired-end FASTQ files.
    output_dir : str
        Directory where viral mapping output files will be saved.
    sample_id : str
        Sample identifier used in the FASTQ filenames.
    reference_fasta : str
        Path to the avian reovirus reference FASTA file.
    threads : int
        Number of CPU threads to use for BWA and samtools.

    Returns
    -------
    str
        Success message if viral mapping completes.

    Raises
    ------
    FileNotFoundError
        If input directory, FASTQ files, or reference FASTA are not found.
    subprocess.CalledProcessError
        If BWA or samtools command fails.

    Notes
    -----
    Expected input files:
    - {sample_id}_unmapped_1.fastq
    - {sample_id}_unmapped_2.fastq

    Output files:
    - viral.sam
    - viral.bam
    - viral.sorted.bam
    - viral.sorted.bam.bai
    """
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    read1 = os.path.join(input_dir, f"{sample_id}_unmapped_1.fastq")
    read2 = os.path.join(input_dir, f"{sample_id}_unmapped_2.fastq")

    if not os.path.exists(read1):
        raise FileNotFoundError(f"Read 1 file not found: {read1}")
    if not os.path.exists(read2):
        raise FileNotFoundError(f"Read 2 file not found: {read2}")
    if not os.path.exists(reference_fasta):
        raise FileNotFoundError(f"Reference FASTA not found: {reference_fasta}")

    os.makedirs(output_dir, exist_ok=True)

    sam_file = os.path.join(output_dir, "viral.sam")
    bam_file = os.path.join(output_dir, "viral.bam")
    sorted_bam = os.path.join(output_dir, "viral.sorted.bam")

    # Index reference if needed
    if not os.path.exists(reference_fasta + ".bwt"):
        subprocess.run(["bwa", "index", reference_fasta], check=True)

    # Map reads with BWA-MEM
    with open(sam_file, "w") as sam_out:
        subprocess.run(
            ["bwa", "mem", "-t", str(threads), reference_fasta, read1, read2],
            stdout=sam_out,
            check=True
        )

    # Convert SAM to BAM
    with open(bam_file, "wb") as bam_out:
        subprocess.run(
            ["samtools", "view", "-@", str(threads), "-Sb", sam_file],
            stdout=bam_out,
            check=True
        )

    # Sort BAM
    subprocess.run(
        ["samtools", "sort", "-@", str(threads), bam_file, "-o", sorted_bam],
        check=True
    )

    # Index sorted BAM
    subprocess.run(
        ["samtools", "index", sorted_bam],
        check=True
    )

    return f"Viral mapping completed successfully! Results are in: {output_dir}"

    """
    Execute viral mapping workflow.

    This function runs the viral mapping pipeline using default parameters
    and prints the result or error message.

    Returns
    -------
    None
    """

    if __name__ == "__main__":
    try:
        message = run_viral_map(
            input_dir="refmap_results",
            output_dir="viral_results",
            sample_id="SRR12620879",
            reference_fasta="avian_reovirus.fa",
            threads=2
        )
        print(message)
    except Exception as e:
        print(f"Error: {e}")
