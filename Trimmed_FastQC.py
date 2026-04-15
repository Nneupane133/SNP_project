#!/usr/bin/env python3
import os
import subprocess


def run_fastqc(input_dir="trimmed_data", output_dir="trimmed_fastqc_results", threads=2):
    """
    Run FastQC on trimmed paired-end FASTQ files in a directory.
    This function scans the specified input directory for FASTQ or FASTQ.GZ files,
    and performs quality control analysis using the FastQC tool. The results are
    saved in the specified output directory.

    Parameters
    ----------
    input_dir : str
        Directory containing trimmed FASTQ files.
    output_dir : str
        Directory where FastQC output files will be saved.
    threads : int
        Number of CPU threads to use for processing.

    Returns
    -------
    str
        Message indicating successful completion of FastQC analysis.

    Raises
    ------
    FileNotFoundError
         If the input directory does not exist or contains no FASTQ files.
    subprocess.CalledProcessError
        If the FastQC command fails during execution.
     Notes
    -----
    - This function automatically detects both `.fastq` and `.fastq.gz` files.
    - FastQC must be installed and available in the system PATH.
    - The output includes HTML and ZIP reports for each input file.

    Examples
    --------
    >>> run_fastqc(input_dir="trimmed_data", output_dir="qc_results", threads=4)
    'FastQC completed successfully! Results are in: qc_results'
    """
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    fastq_files = sorted([
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".fastq") or f.endswith(".fastq.gz")
    ])

    if not fastq_files:
        raise FileNotFoundError(f"No FASTQ files found in: {input_dir}")

    os.makedirs(output_dir, exist_ok=True)

    cmd = ["fastqc", "-t", str(threads), "-o", output_dir] + fastq_files
    subprocess.run(cmd, check=True)

    return f"FastQC completed successfully! Results are in: {output_dir}"


if __name__ == "__main__":
    try:
        message = run_fastqc(
            input_dir="trimmed_data",
            output_dir="trimmed_fastqc_results",
            threads=2
        )
        print(message)
    except Exception as e:
        print(f"Error: {e}")
