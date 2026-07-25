from statistics import mean
from typing import List

from snpahoy.core import SNP


def count_heterozygotes(snps: List[SNP]) -> int:
    """Count the number of heterozygous sites."""
    return len([snp for snp in snps if snp.is_heterozygote()])


def mean_minor_allele_frequency(snps: List[SNP]) -> float:
    """Computes the mean minor allele frequency SNPs."""
    if not snps:
        return 0.0
    return mean([snp.minor_allele_frequency() for snp in snps])


def mean_off_genotype_frequency(snps: List[SNP]) -> float:
    """Compute the mean off-genotype frequency of SNPs."""
    if not snps:
        return 0.0
    return mean([snp.off_genotype_frequency() for snp in snps])
