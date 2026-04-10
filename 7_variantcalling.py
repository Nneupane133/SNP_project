#!/usr/bin/env python3
import os
import subprocess


def run_variant_calling(input_bam="viral_results/viral.sorted.bam",
                        reference_fasta="avian_reovirus.fa",
                        output_dir="viral_results",
                        raw_vcf_name="viral_variants.vcf",
                        filtered_vcf_name="viral_variants.filtered.vcf",
                        min_qual=20,
                        min_depth=10):
    """Call and filter variants from a mapped BAM file using bcftools.

    Parameters
    ----------
    input_bam : str
        Path to the sorted BAM file used for variant calling.
    reference_fasta : str
        Path to the reference FASTA file.
    output_dir : str
        Directory where VCF output files will be saved.
    raw_vcf_name : str
        Filename for the raw VCF output.
    filtered_vcf_name : str
        Filename for the filtered VCF output.
    min_qual : int
        Minimum QUAL score required to keep a variant.
    min_depth : int
        Minimum read depth (DP) required to keep a variant.

    Returns
    -------
    str
        Success message with paths to the raw and filtered VCF files.

    Raises
    ------
    FileNotFoundError
        If the input BAM file or reference FASTA file is not found.
    subprocess.CalledProcessError
        If any bcftools command fails.
    """
    if not os.path.exists(input_bam):
        raise FileNotFoundError(f"Input BAM file not found: {input_bam}")

    if not os.path.exists(reference_fasta):
        raise FileNotFoundError(f"Reference FASTA file not found: {reference_fasta}")

    os.makedirs(output_dir, exist_ok=True)

    raw_vcf = os.path.join(output_dir, raw_vcf_name)
    filtered_vcf = os.path.join(output_dir, filtered_vcf_name)

    filter_expression = f"QUAL>{min_qual} && DP>{min_depth}"

    # Step 1: Call variants
    mpileup = subprocess.Popen(
        ["bcftools", "mpileup", "-Ou", "-f", reference_fasta, input_bam],
        stdout=subprocess.PIPE
    )

    subprocess.run(
        ["bcftools", "call", "-mv", "-Ov", "-o", raw_vcf],
        stdin=mpileup.stdout,
        check=True
    )

    # Step 2: Filter variants
    subprocess.run(
        [
            "bcftools", "filter",
            "-i", filter_expression,
            raw_vcf,
            "-Ov",
            "-o", filtered_vcf
        ],
        check=True
    )

    return (
        f"Variant calling completed successfully!\n"
        f"Raw VCF: {raw_vcf}\n"
        f"Filtered VCF: {filtered_vcf}"
    )


if __name__ == "__main__":
    try:
        message = run_variant_calling(
            input_bam="viral_results/viral.sorted.bam",
            reference_fasta="avian_reovirus.fa",
            output_dir="viral_results",
            raw_vcf_name="viral_variants.vcf",
            filtered_vcf_name="viral_variants.filtered.vcf",
            min_qual=20,
            min_depth=10
        )
        print(message)
    except Exception as e:
        print(f"Error: {e}")