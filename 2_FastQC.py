#!/usr/bin/env python3
import os
import subprocess


def run_fastqc(input_dir="data", output_dir="fastqc_results", threads=2):
    """
    Run FastQC on paired-end FASTQ files in a directory.
    This function identifies FASTQ or FASTQ.GZ files in the input directory and performs quality control(QC) analysis using the FASTQC tool. 

    Parameters
    ----------
    input_dir : str
        Directory containing FASTQ files.
    output_dir : str
        Directory where FastQC output files will be saved.
    threads : int
        Number of threads to use for FastQC.

    Returns
    -------
    str
        Message indicating succesful completion.

    Raises
    ------
    FileNotFoundError
        If input directory or FASTQ files are not found.
    subprocess.CalledProcessError
        If FastQC command fails during execution.
    """
    #Check whether the input directory exists
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    #Collect all FASTQ and FASTQ.GZ files from the input directory
    fastq_files = sorted([
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".fastq") or f.endswith(".fastq.gz")
    ])
    #Raise an error if no FASTQ files are detected
    if not fastq_files:
        raise FileNotFoundError(f"No FASTQ files found in: {input_dir}")

    os.makedirs(output_dir, exist_ok=True)

    cmd = ["fastqc", "-t", str(threads), "-o", output_dir] + fastq_files
    subprocess.run(cmd, check=True)

    return f"FastQC completed successfully! Results are in: {output_dir}"


if __name__ == "__main__":
    try:
        message = run_fastqc(
            input_dir="data",
            output_dir="fastqc_results",
            threads=2
        )
        print(message)
    except Exception as e:
        print(f"Error: {e}")
