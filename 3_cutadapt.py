#!/usr/bin/env python3
import os
import subprocess


def run_cutadapt(sample_id, input_dir="data", output_dir="trimmed_data",
                 threads=2, trim_5=20, trim_3=20, quality_cutoff=None, min_length=30):
    """
    Trim paired-end FASTQ files using cutadapt.

    This function trims reads from both 5' and 3' ends, performs quality filterings and removes reads below a specified minimum length and also remove adapter if present

    Parameters
    ----------
    sample_id : str
        Sample/SRR ID (e.g., SRR12620879)
    input_dir : str
        Directory containing FASTQ files
    output_dir : str
        Directory to store trimmed files
    threads : int
        Number of CPU threads
    trim_5 : int
       Number of bases to trim from 5' end
    trim_3 : int
        Number of bases to trim from 3' end
    quality_cutoff : int or None
        Quality trimming threshold (e.g., 20). If None,quality trimming is  skipped.
    min_length : int
        Minimum read length to retain after trimming

    Returns
    -------
    str
        Message indicating successful completion or failure.

    Raises
    -----
    FileNotFoundError
        If input FASTQ files are not found.
    subprocess.CalledProcessError
        If cutadapt execution fails.
    """

    #Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    #Define input FASTQ file paths
    r1 = os.path.join(input_dir, f"{sample_id}_1.fastq")
    r2 = os.path.join(input_dir, f"{sample_id}_2.fastq")

     # Define output trimmed file paths
    out_r1 = os.path.join(output_dir, f"{sample_id}_1.trimmed.fastq")
    out_r2 = os.path.join(output_dir, f"{sample_id}_2.trimmed.fastq")

     # Check if input FASTQ files exist
    if not os.path.exists(r1) or not os.path.exists(r2):
        raise FileNotFoundError(f"FASTQ files for {sample_id} not found.")

     # Construct cutadapt command
    cmd = [
        "cutadapt",
        "-j", str(threads),
        "-u", str(trim_5),      # trim 5' end
        "-u", f"-{trim_3}",     # trim 3' end
        "-m", str(min_length),  # minimum length
        "-o", out_r1,
        "-p", out_r2,
        r1,
        r2
    ]

    # Add quality trimming if specified
    if quality_cutoff is not None:
        cmd.insert(1, "-q")
        cmd.insert(2, f"{quality_cutoff},{quality_cutoff}")

    try:
        subprocess.run(cmd, check=True)
        return f"✅ Trimmed files saved in: {output_dir}"

    except subprocess.CalledProcessError as e:
        return f"❌ Error during trimming: {e}"

    #Example sample ID
    if __name__ == "__main__":
    sample_id = "SRR12620879"

    # Run trimming pipeline
    message = run_cutadapt(
        sample_id=sample_id,
        input_dir="data",
        output_dir="trimmed_data",
        threads=4,
        trim_5=20,
        trim_3=20,
        quality_cutoff=20,   # optional (can set None)
        min_length=30
    )

    print(message)
