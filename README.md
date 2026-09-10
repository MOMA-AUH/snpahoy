# SNP Ahoy!

[![Conda Version](https://img.shields.io/conda/vn/MOMA-AUH/snpahoy?cacheSeconds=300&style=for-the-badge)](https://anaconda.org/MOMA-AUH/snpahoy) [![Conda Downloads](https://img.shields.io/conda/dn/MOMA-AUH/snpahoy?cacheSeconds=300&style=for-the-badge)](https://anaconda.org/MOMA-AUH/snpahoy)

Just a little tool for checking ID SNPs. It works in both germline and somatic modes as described in the sections below. By default, only sites with at least `30X` coverage are considered, and sites with major allele frequency greater than or equal to `95%` are considered homozygous.

```
$ snpahoy --help
Usage: snpahoy [OPTIONS] COMMAND [ARGS]...

Options:
  --minimum_coverage INTEGER      Only consider SNP positions with at least this
                                  coverage  [default: 30]

  --minimum_base_quality INTEGER  Only count bases with at least this quality
                                  [default: 1]

  --homozygosity_threshold FLOAT  Consider a SNP position homozygote if
                                  frequency of most common allele is this or
                                  higher  [default: 0.95]

  --help                          Show this message and exit.

Commands:
  germline
  somatic
```

## Germline Mode

To run in germline mode, simply provide a BAM/CRAM file using the `--bam_file` option.

```
$ snpahoy germline --help
Usage: snpahoy germline [OPTIONS]

Options:
  --bed_file PATH              BED file with SNP positions  [required]
  --bam_file PATH              BAM file (must be indexed)  [required]
  --reference_fasta_file PATH  Reference FASTA file for CRAM files
  --output_json_file PATH      JSON output file  [required]
  --help                       Show this message and exit.
```

The output JSON file contains input information, genotypes at all SNP positions, and a summary. In case a SNP is not genotyped (as for the `chrY` ones in the example below), the empty string is reported as genotype.

```
{
    "input": {
        "settings": {
            "minimum_coverage": 30,
            "minimum_base_quality": 1,
            "homozygosity_threshold": 0.95
        },
        "files": {
            "bed_file": "snps.bed",
            "bam_file": "germline.bam"
        }
    },
    "output": {
        "details": {
            "chr1:13866176": {
                "depth": 982,
                "counts": {
                    "A": 3,
                    "C": 484,
                    "G": 0,
                    "T": 495
                },
                "alleles": {
                    "major": {
                        "base": "T",
                        "frequency": 0.5041
                    },
                    "minor": {
                        "base": "C",
                        "frequency": 0.4929
                    }
                },
                "genotype": "CT",
                "off_genotype_frequency": 0.0031
            },
            "chr1:22261384": {
                "depth": 323,
                "counts": {
                    "A": 0,
                    "C": 0,
                    "G": 323,
                    "T": 0
                },
                "alleles": {
                    "major": {
                        "base": "G",
                        "frequency": 1.0
                    },
                    "minor": {
                        "base": "",
                        "frequency": 0.0
                    }
                },
                "genotype": "GG",
                "off_genotype_frequency": 0.0
            },

            (...)

            "chrY:9401049": {
                "depth": 0,
                "counts": {
                    "A": 0,
                    "C": 0,
                    "G": 0,
                    "T": 0
                },
                "alleles": {
                    "major": {
                        "base": "",
                        "frequency": 0.0
                    },
                    "minor": {
                        "base": "",
                        "frequency": 0.0
                    }
                },
                "genotype": "",
                "off_genotype_frequency": 0.0
            }
        },
        "summary": {
            "snps": {
                "total": 1041,
                "genotyped": 1016
            },
            "heterozygous_site_fraction": 0.4744,
            "mean_minor_allele_frequency_at_homozygous_sites": 0.0022,
            "mean_off_genotype_frequency": 0.0023
        }
    }
}
```

## Somatic Mode

To run in somatic mode, provide tumor and germline BAM/CRAM files using the `--tumor_bam_file` and `--germline_bam_file` options.

```
$ snpahoy somatic --help
Usage: snpahoy somatic [OPTIONS]

Options:
  --bed_file PATH              BED file with SNP positions  [required]
  --tumor_bam_file PATH        Tumor BAM file (must be indexed)  [required]
  --germline_bam_file PATH     Germline BAM file (must be indexed)  [required]
  --reference_fasta_file PATH  Reference FASTA file for CRAM files
  --output_json_file PATH      JSON output file  [required]
  --help                       Show this message and exit.
```

Output is similar to that in germline mode. Only sites that are genotyped in both tumor and germline are used. In both the tumor and germline summaries, `mean_minor_allele_frequency_at_homozygous_sites` is calculated at sites classified as homozygous in the germline sample.

```
{
    "input": {
        "settings": {
            "minimum_coverage": 30,
            "minimum_base_quality": 1,
            "homozygosity_threshold": 0.95
        },
        "files": {
            "bed_file": "snps.bed",
            "tumor_bam_file": "tumor.bam",
            "germline_bam_file": "germline.bam"
        },
        "output": {
            "details": {
                "tumor": { ... },
                "germline": { ... }
            }
        },
        "summary": {
            "snps": {
                "total": 1041,
                "genotyped": 1000
            },
            "tumor": {
                "heterozygous_site_fraction": 0.474,
                "mean_minor_allele_frequency_at_homozygous_sites": 0.0019,
                "mean_off_genotype_frequency": 0.0019
            },
            "germline": {
                "heterozygous_site_fraction": 0.474,
                "mean_minor_allele_frequency_at_homozygous_sites": 0.0022,
                "mean_off_genotype_frequency": 0.0019
            }
        }
    }
}
```

This tool is developed with the [MSK IMPACT](https://doi.org/10.1016/j.jmoldx.2014.12.006) panel in mind. Suggested cutoffs for identifying sample swaps or contamination are `0.55` for the heterozygous-site fraction and `0.01` for the mean minor allele frequency at homozygous sites.

## Installation

The recommended way to install **snpahoy** is via [conda](https://docs.conda.io/), using the `MOMA-AUH` channel:

```bash
conda install MOMA-AUH::snpahoy
```
