#!/usr/bin/env python3
import os
import subprocess


def run_command(cmd, description):
    """Execute a shell command.

    Parameters
    ----------
    cmd : list
        Command to execute as a list.
    description : str
        Description of the step being executed.

    Returns
    -------
    None

    Raises
    ------
    subprocess.CalledProcessError
        If the command execution fails.
    """
    print(f"\nRunning: {description}")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def ensure_bwa_index(reference_fasta):
    """Ensure BWA index exists for the reference genome.

    Parameters
    ----------
    reference_fasta : str
        Path to the reference genome FASTA file.

    Returns
    -------
    None
    """
    expected_files = [
        reference_fasta + ext for ext in [".amb", ".ann", ".bwt", ".pac", ".sa"]
    ]
    if not all(os.path.exists(f) for f in expected_files):
        run_command(
            ["bwa", "index", reference_fasta],
            f"Indexing reference genome: {reference_fasta}"
        )


def ensure_fasta_index(reference_fasta):
    """Ensure samtools FASTA index (.fai) exists.

    Parameters
    ----------
    reference_fasta : str
        Path to the reference genome FASTA file.

    Returns
    -------
    None
    """
    fai_file = reference_fasta + ".fai"
    if not os.path.exists(fai_file):
        run_command(
            ["samtools", "faidx", reference_fasta],
            f"Creating FASTA index: {reference_fasta}.fai"
        )


def map_and_extract_unmapped(
    sample_id,
    reference_fasta,
    input_dir="trimmed_data",
    output_dir="refmap_results",
    threads=4
):
    """Align reads to reference genome and extract unmapped reads.

    Parameters
    ----------
    sample_id : str
        Sample identifier (e.g., SRR12620879).
    reference_fasta : str
        Path to the reference genome FASTA file.
    input_dir : str
        Directory containing trimmed FASTQ files.
    output_dir : str
        Directory to save mapping outputs.
    threads : int
        Number of CPU threads to use.

    Returns
    -------
    str
        Summary message with output file locations.

    Raises
    ------
    FileNotFoundError
        If input FASTQ files or reference genome are missing.
    subprocess.CalledProcessError
        If any external command (BWA or samtools) fails.
    """
    os.makedirs(output_dir, exist_ok=True)

    r1 = os.path.join(input_dir, f"{sample_id}_1.trimmed.fastq")
    r2 = os.path.join(input_dir, f"{sample_id}_2.trimmed.fastq")

    if not os.path.exists(r1):
        raise FileNotFoundError(f"Missing read 1 file: {r1}")
    if not os.path.exists(r2):
        raise FileNotFoundError(f"Missing read 2 file: {r2}")
    if not os.path.exists(reference_fasta):
        raise FileNotFoundError(f"Missing reference FASTA: {reference_fasta}")

    sam_file = os.path.join(output_dir, f"{sample_id}.sam")
    bam_file = os.path.join(output_dir, f"{sample_id}.bam")
    sorted_bam = os.path.join(output_dir, f"{sample_id}.sorted.bam")
    unmapped_bam = os.path.join(output_dir, f"{sample_id}.unmapped.bam")
    unmapped_r1 = os.path.join(output_dir, f"{sample_id}_unmapped_1.fastq")
    unmapped_r2 = os.path.join(output_dir, f"{sample_id}_unmapped_2.fastq")
    unmapped_single = os.path.join(output_dir, f"{sample_id}_unmapped_single.fastq")

    ensure_bwa_index(reference_fasta)
    ensure_fasta_index(reference_fasta)

    with open(sam_file, "w") as sam_out:
        print(f"\nRunning: BWA-MEM alignment for {sample_id}")
        subprocess.run(
            ["bwa", "mem", "-t", str(threads), reference_fasta, r1, r2],
            check=True,
            stdout=sam_out
        )

    with open(bam_file, "wb") as bam_out:
        print(f"\nRunning: SAM to BAM conversion for {sample_id}")
        subprocess.run(
            ["samtools", "view", "-@", str(threads), "-bS", sam_file],
            check=True,
            stdout=bam_out
        )

    run_command(
        ["samtools", "sort", "-@", str(threads), "-o", sorted_bam, bam_file],
        f"Sorting BAM for {sample_id}"
    )

    run_command(
        ["samtools", "index", sorted_bam],
        f"Indexing sorted BAM for {sample_id}"
    )

    with open(unmapped_bam, "wb") as out_bam:
        print(f"\nRunning: Extracting unmapped read pairs for {sample_id}")
        subprocess.run(
            ["samtools", "view", "-@", str(threads), "-b", "-f", "12", "-F", "256", sorted_bam],
            check=True,
            stdout=out_bam
        )

    run_command(
        [
            "samtools", "fastq",
            "-@", str(threads),
            "-1", unmapped_r1,
            "-2", unmapped_r2,
            "-0", "/dev/null",
            "-s", unmapped_single,
            "-n",
            unmapped_bam
        ],
        f"Converting unmapped BAM to FASTQ for {sample_id}"
    )

    return (
        f"Host filtering completed for {sample_id}\n"
        f"Sorted BAM: {sorted_bam}\n"
        f"Unmapped BAM: {unmapped_bam}\n"
        f"Unmapped FASTQ R1: {unmapped_r1}\n"
        f"Unmapped FASTQ R2: {unmapped_r2}\n"
        f"Unmapped singletons: {unmapped_single}"
    )


if __name__ == "__main__":
    sample_id = "SRR12620879"

    # Reference file located directly inside SNP_project
    reference_fasta = "GCA_000002315.3_Gallus_gallus-5.0_genomic.fna"

    try:
        message = map_and_extract_unmapped(
            sample_id=sample_id,
            reference_fasta=reference_fasta,
            input_dir="trimmed_data",
            output_dir="refmap_results",
            threads=4
        )
        print("\n" + message)
    except Exception as e:
        print(f"Error: {e}")