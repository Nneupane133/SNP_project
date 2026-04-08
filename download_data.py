#!/usr/bin/env python3 
import os
import subprocess

def download_sra_data(srr_id, output_dir):
    """Download and convert SRA data from NCBI using prefetch and fasterq-dump.
    
    Args:
        srr_id (str): The SRA ID (e.g., 'SRR12620879') to be downloaded.
        output_dir (str): Directory to store the output data.
    
    Returns:
        str: A message indicating success or failure.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Step 1: Download from NCBI using prefetch
        subprocess.run([
            "prefetch",
            srr_id
        ], check=True)

        # Step 2: Convert to FASTQ format using fasterq-dump
        subprocess.run([
            "fasterq-dump",
            srr_id,
            "-O", output_dir,
            "--split-files",   # for paired-end data
            "--threads", "4"
        ], check=True)



        return "Download and conversion completed successfully!"

    except subprocess.CalledProcessError as e:
        return f"Error occurred: {e}"

if __name__ == '__main__':
    # Example usage
    srr_id = "SRR12620879"
    output_dir = "data"
    
    result_message = download_sra_data(srr_id, output_dir)
    print(result_message)