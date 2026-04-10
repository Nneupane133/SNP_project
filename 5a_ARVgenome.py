#!/usr/bin/env python3
import os
import subprocess
import glob

#!/usr/bin/env python3
import glob

def combine_fasta(input_pattern="sequence*.fasta", output_file="avian_reovirus.fa"):
    """Combine multiple FASTA files into a single FASTA file.

    Parameters
    ----------
    input_pattern : str
        Pattern to match input FASTA files (e.g., 'sequence*.fasta').
    output_file : str
        Name of the combined output FASTA file.

    Returns
    -------
    str
        Success message with number of files combined.

    Raises
    ------
    FileNotFoundError
        If no FASTA files are found matching the pattern.
    """
    fasta_files = sorted(glob.glob(input_pattern))

    if not fasta_files:
        raise FileNotFoundError("No FASTA files found matching pattern: sequence*.fasta")

    with open(output_file, "w") as outfile:
        for fasta_file in fasta_files:
            with open(fasta_file, "r") as infile:
                content = infile.read().strip()
                if content:
                    outfile.write(content)
                    outfile.write("\n")

    return f"Combined {len(fasta_files)} FASTA files into {output_file}"


if __name__ == "__main__":
    try:
        message = combine_fasta()
        print(message)
    except Exception as e:
        print(f"Error: {e}")