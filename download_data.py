#!/usr/bin/env python3
import os
import subprocess

srr_id = "SRR12620879"
output_dir = "data"

os.makedirs(output_dir, exist_ok=True)

try:
    # Step 1: Download from NCBI (internet)
    subprocess.run([
        "prefetch",
        srr_id
    ], check=True)


    # Step 2: Convert to FASTQ
    subprocess.run([
        "fasterq-dump",
        srr_id,
        "-O", output_dir,
        "--split-files",   # for paired-end data
        "--threads", "4"
    ], check=True)

    # Step 3: Compress output
    subprocess.run(f"gzip {output_dir}/*.fastq", shell=True, check=True)

    print("Download + conversion completed successfully!")

except subprocess.CalledProcessError as e:
    print("Error:", e)