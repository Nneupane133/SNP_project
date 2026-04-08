#!/usr/bin/env python3
import os
import subprocess


def run_fastqc(input_dir="trimmed_data", output_dir="fastqc_trimmed", threads=2):
    """Run FastQC on trimmed FASTQ files."""

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Get all trimmed FASTQ files
    fastq_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".fastq") or f.endswith(".fastq.gz")
    ]

    if not fastq_files:
        raise FileNotFoundError("No trimmed FASTQ files found.")

    # Run FastQC
    cmd = ["fastqc", "-t", str(threads), "-o", output_dir] + fastq_files
    subprocess.run(cmd, check=True)

    return f"FastQC completed! Results in: {output_dir}"


if __name__ == "__main__":
    try:
        message = run_fastqc()
        print(message)
    except Exception as e:
        print(f"Error: {e}")