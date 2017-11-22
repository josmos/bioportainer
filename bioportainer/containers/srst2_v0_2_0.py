import os

from bioportainer.MultiCmdContainer import MultiCmdContainer

from bioportainer.Config import config


class Srst2_v0_2_0(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.change_out_err_log = True
        self.set_srst2_params()
        self.set_getmlst_params()

    def get_opt_params(self, param_attr):
        """
        return optional parameter dictionary as parameter-string-list
        :param param_attr: string: "get_<sub command>_params"
        :return: list of strings
        """
        p = getattr(self, param_attr)
        l = []
        for k, v in p.items():
            if v == "threads":
                v = str(config.container_threads)
            if type(v) == bool and v is True:
                l += ["--" + k]
            elif type(v) == bool and v is False:
                continue
            elif len(k) == 1:
                l += ["-" + k, v]
            else:
                l += ["--" + k, v]

        return l

    @MultiCmdContainer.impl_set_opt_params
    def set_srst2_params(self, merge_paired=False, forward=False, reverse=False, read_type=False,
                         mlst_db=False, mlst_delimiter=False, mlst_definitions=False,
                         mlst_max_mismatch=False, gene_db=False, no_gene_details=False,
                         gene_max_mismatch=False, min_coverage=False, max_divergence=False,
                         min_depth=False, min_edge_depth=False, prob_err=False,
                         truncation_score_tolerance=False, stop_after=False, other=False,
                         max_unaligned_overlap=False, mapq=False, baseq=False, samtools_args=False,
                         log=False, save_scores=False, report_new_consensus=False,
                         report_all_consensus=False, use_existing_bowtie2_sam=False,
                         use_existing_pileup=False, use_existing_scores=False,
                         keep_interim_alignment=False, threads="threads"):
        """usage: srst2 [-h] [--version] [--input_se INPUT_SE [INPUT_SE ...]]
                     [--input_pe INPUT_PE [INPUT_PE ...]] [--merge_paired]
                     [--forward FORWARD] [--reverse REVERSE] [--read_type {q,qseq,f}]
                     [--mlst_db MLST_DB] [--mlst_delimiter MLST_DELIMITER]
                     [--mlst_definitions MLST_DEFINITIONS]
                     [--mlst_max_mismatch MLST_MAX_MISMATCH]
                     [--gene_db GENE_DB [GENE_DB ...]] [--no_gene_details]
                     [--gene_max_mismatch GENE_MAX_MISMATCH]
                     [--min_coverage MIN_COVERAGE] [--max_divergence MAX_DIVERGENCE]
                     [--min_depth MIN_DEPTH] [--min_edge_depth MIN_EDGE_DEPTH]
                     [--prob_err PROB_ERR]
                     [--truncation_score_tolerance TRUNCATION_SCORE_TOLERANCE]
                     [--stop_after STOP_AFTER] [--other OTHER]
                     [--max_unaligned_overlap MAX_UNALIGNED_OVERLAP] [--mapq MAPQ]
                     [--baseq BASEQ] [--samtools_args SAMTOOLS_ARGS] --output OUTPUT
                     [--log] [--save_scores] [--report_new_consensus]
                     [--report_all_consensus] [--use_existing_bowtie2_sam]
                     [--use_existing_pileup] [--use_existing_scores]
                     [--keep_interim_alignment] [--threads THREADS]
                     [--prev_output PREV_OUTPUT [PREV_OUTPUT ...]]

        SRST2 - Short Read Sequence Typer (v2)

        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit
          --input_se INPUT_SE [INPUT_SE ...]
                                Single end read file(s) for analysing (may be gzipped)
          --input_pe INPUT_PE [INPUT_PE ...]
                                Paired end read files for analysing (may be gzipped)
          --merge_paired        Switch on if all the input read sets belong to a
                                single sample, and you want to merge their data to get
                                a single result
          --forward FORWARD     Designator for forward reads (only used if NOT in
                                MiSeq format sample_S1_L001_R1_001.fastq.gz; otherwise
                                default is _1, i.e. expect forward reads as
                                sample_1.fastq.gz)
          --reverse REVERSE     Designator for reverse reads (only used if NOT in
                                MiSeq format sample_S1_L001_R2_001.fastq.gz; otherwise
                                default is _2, i.e. expect forward reads as
                                sample_2.fastq.gz
          --read_type {q,qseq,f}
                                Read file type (for bowtie2; default is q=fastq; other
                                options: qseq=solexa, f=fasta).
          --mlst_db MLST_DB     Fasta file of MLST alleles (optional)
          --mlst_delimiter MLST_DELIMITER
                                Character(s) separating gene name from allele number
                                in MLST database (default "-", as in arcc-1)
          --mlst_definitions MLST_DEFINITIONS
                                ST definitions for MLST scheme (required if mlst_db
                                supplied and you want to calculate STs)
          --mlst_max_mismatch MLST_MAX_MISMATCH
                                Maximum number of mismatches per read for MLST allele
                                calling (default 10)
          --gene_db GENE_DB [GENE_DB ...]
                                Fasta file/s for gene databases (optional)
          --no_gene_details     Switch OFF verbose reporting of gene typing
          --gene_max_mismatch GENE_MAX_MISMATCH
                                Maximum number of mismatches per read for gene
                                detection and allele calling (default 10)
          --min_coverage MIN_COVERAGE
                                Minimum %coverage cutoff for gene reporting (default
                                90)
          --max_divergence MAX_DIVERGENCE
                                Maximum %divergence cutoff for gene reporting (default
                                10)
          --min_depth MIN_DEPTH
                                Minimum mean depth to flag as dubious allele call
                                (default 5)
          --min_edge_depth MIN_EDGE_DEPTH
                                Minimum edge depth to flag as dubious allele call
                                (default 2)
          --prob_err PROB_ERR   Probability of sequencing error (default 0.01)
          --truncation_score_tolerance TRUNCATION_SCORE_TOLERANCE
                                % increase in score allowed to choose non-truncated
                                allele
          --stop_after STOP_AFTER
                                Stop mapping after this number of reads have been
                                mapped (otherwise map all)
          --other OTHER         Other arguments to pass to bowtie2 (must be escaped,
                                e.g. "\--no-mixed".
          --max_unaligned_overlap MAX_UNALIGNED_OVERLAP
                                Read discarded from alignment if either of its ends
                                has unaligned overlap with the reference that is
                                longer than this value (default 10)
          --mapq MAPQ           Samtools -q parameter (default 1)
          --baseq BASEQ         Samtools -Q parameter (default 20)
          --samtools_args SAMTOOLS_ARGS
                                Other arguments to pass to samtools mpileup (must be
                                escaped, e.g. "\-A").
          --output OUTPUT       Prefix for srst2 output files
          --log                 Switch ON logging to file (otherwise log to stdout)
          --save_scores         Switch ON verbose reporting of all scores
          --report_new_consensus
                                If a matching alleles is not found, report the
                                consensus allele. Note, only SNP differences are
                                considered, not indels.
          --report_all_consensus
                                Report the consensus allele for the most likely
                                allele. Note, only SNP differences are considered, not
                                indels.
          --use_existing_bowtie2_sam
                                Use existing SAM file generated by Bowtie2 if
                                available, otherwise they will be generated
          --use_existing_pileup
                                Use existing pileups if available, otherwise they will
                                be generated
          --use_existing_scores
                                Use existing scores files if available, otherwise they
                                will be generated
          --keep_interim_alignment
                                Keep interim files (sam & unsorted bam), otherwise
                                they will be deleted after sorted bam is created
          --threads THREADS     Use multiple threads in Bowtie and Samtools
          --prev_output PREV_OUTPUT [PREV_OUTPUT ...]
                                SRST2 results files to compile (any new results from
                                this run will also be incorporated)
        """
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_getmlst_params(self, repository_url=False, species=False, force_scheme_name=False):
        """usage: getmlst.py [-h] [--repository_url URL] --species NAME
                  [--force_scheme_name]

Download MLST datasets by speciesfrom pubmlst.org.

optional arguments:
  -h, --help            show this help message and exit
  --repository_url URL  URL for MLST repository XML index
  --species NAME        The name of the species that you want to download
                        (e.g. "Escherichia coli")
  --force_scheme_name   Flage to force downloading of specific scheme name
                        (e.g. "Clostridium difficile")
"""

        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="srst2", output_postfix="", input_type="fastq-pe", mount=None):
        self.input_type = input_type
        if subcmd == "srst2":
            self.output_type = "txt"
            out = sample_io.id + output_postfix
            self.input_allowed = ["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz"]

            if self.input_type in ["fastq-pe", "fastq-pe-gz"]:
                input = ["--input_pe", sample_io.files[0].name, sample_io.files[1].name]

            elif self.input_type in ["fastq-se", "fastq-se-gz"]:
                input = ["--input_se"] + [f.name for f in sample_io.files]

            else:
                raise IOError

            self.cmd = [subcmd, "--output", out] + self.get_opt_params("srst2_params") + input

        elif subcmd == "getmlst":
            self.cmd = [subcmd + ".py"] + self.get_opt_params("getmlst_params")

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="srst2", output_postfix="", input_type="fastq-pe", mount=None):
        pass
