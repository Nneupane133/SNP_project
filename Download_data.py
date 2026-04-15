#!/usr/bin/env python3 
import os
import subprocess

def download_sra_data(srr_id, output_dir):
    """Download and convert SRA data from NCBI using prefetch and fasterq-dump.
    This function uses SRA TOOLkit command "prefetch" and "fasterq-dump" is used to download sequencing data and convert it into FASTQ format.

    Args:
        srr_id (str): The SRA ID (e.g., 'SRR12620879') to be downloaded.
        output_dir (str): Directory to store the output data.

    Parameters
    ----------
    srr_id : str
    SRA accesion ID  (e.g., 'SRR12620879').
    output_dir : str
        Directory where the FASTQ files will be saved.
    
    Returns
    -------
        str: Message indicating success or failure.
    """
    #Create output directory if it doesnot exist
    os.makedirs(output_dir, exist_ok=True)
    #Download SRA file from NCBI
    #Convert SRA file to FASTQ format
    try:
        subprocess.run([
            "prefetch",
            srr_id
        ], check=True)

        subprocess.run([
            "fasterq-dump",
            srr_id,
            "-O", output_dir,
            "--split-files",  
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
