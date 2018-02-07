from bioportainer.MultiCmdContainer import MultiCmdContainer
import os
import distutils.dir_util
import os
import time
import uuid
from abc import ABCMeta
from functools import wraps, partial
from inspect import stack
from multiprocessing import Pool, Manager

import bioportainer.Config as Conf
import bioportainer.SampleIO as Sio
import docker
from requests.exceptions import HTTPError

import bioportainer.SampleList as Cio
from bioportainer import config


class Quast_v4_6_1(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_quast_params()
        self.set_metaquast_params()

    @MultiCmdContainer.impl_set_opt_params
    def set_quast_params(self, min_contig=False, threads="threads", scaffolds=False, labels=False,
                         L=False, eukaryote=False, gene_finding=False, glimmer=False, mgm=False,
                         gene_thresholds=False, est_ref_size=False, gage=False,
                         contig_thresholds=False, use_all_alignments=False, min_alignment=False,
                         min_identity=False, ambiguity_usage=False, ambiguity_score=False,
                         strict_NA=False, extensive_mis_size=False, scaffold_gap_max_size=False,
                         unaligned_partsize=False, fragmented=False, fragmented_max_indent=False,
                         plots_format=False, memory_efficient=False, space_efficient=False,
                         sv_bedpe=False, no_check=False, no_plots=False, no_html=False,
                         no_icarus=False, no_snps=False, no_gc=False, no_sv=False, no_gzip=False,
                         fast=False, silent=False):
        """WARNING: Python locale settings can't be changed
	QUAST: QUality ASsessment Tool for Genome Assemblies
	Version: 4.6.1

	Usage: python /usr/local/bin/quast.py [options] <files_with_contigs>

	Options:
	-o  --output-dir  <dirname>   Directory to store all result files [default: quast_results/results_<datetime>]
	-R                <filename>  Reference genome file
	-G  --genes       <filename>  File with gene coordinates in the reference (GFF, BED, NCBI or TXT)
	-O  --operons     <filename>  File with operon coordinates in the reference (GFF, BED, NCBI or TXT)
	-m  --min-contig  <int>       Lower threshold for contig length [default: 500]
	-t  --threads     <int>       Maximum number of threads [default: 25% of CPUs]

	Advanced options:
	-s  --scaffolds                       Assemblies are scaffolds, split them and add contigs to the comparison
	-l  --labels "label, label, ..."      Names of assemblies to use in reports, comma-separated. If contain spaces, use quotes
	-L                                    Take assembly names from their parent directory names
	-e  --eukaryote                       Genome is eukaryotic
	-f  --gene-finding                    Predict genes using GeneMarkS (prokaryotes, default) or GeneMark-ES (eukaryotes, use --eukaryote)
	    --glimmer                         Use GlimmerHMM for gene prediction (instead of the default finder, see above)
	    --mgm                             Use MetaGeneMark for gene prediction (instead of the default finder, see above)
	    --gene-thresholds <int,int,...>   Comma-separated list of threshold lengths of genes to search with Gene Finding module
	                                      [default: 0,300,1500,3000]
	    --est-ref-size <int>              Estimated reference size (for computing NGx metrics without a reference)
	    --gage                            Use GAGE (results are in gage_report.txt)
	    --contig-thresholds <int,int,...> Comma-separated list of contig length thresholds [default: 0,1000,5000,10000,25000,50000]
	-u  --use-all-alignments              Compute genome fraction, # genes, # operons in QUAST v1.* style.
	                                      By default, QUAST filters Nucmer's alignments to keep only best ones
	-i  --min-alignment <int>             Nucmer's parameter: the minimum alignment length [default: 0]
	    --min-identity <float>            Nucmer's parameter: the minimum alignment identity (80.0, 100.0) [default: 95.0]
	-a  --ambiguity-usage <none|one|all>  Use none, one, or all alignments of a contig when all of them
	                                      are almost equally good (see --ambiguity-score) [default: one]
	    --ambiguity-score <float>         Score S for defining equally good alignments of a single contig. All alignments are sorted
	                                      by decreasing LEN * IDY% value. All alignments with LEN * IDY% < S * best(LEN * IDY%) are
	                                      discarded. S should be between 0.8 and 1.0 [default: 0.99]
	    --strict-NA                       Break contigs in any misassembly event when compute NAx and NGAx
	                                      By default, QUAST breaks contigs only by extensive misassemblies (not local ones)
	-x  --extensive-mis-size  <int>       Lower threshold for extensive misassembly size. All relocations with inconsistency
	                                      less than extensive-mis-size are counted as local misassemblies [default: 1000]
	    --scaffold-gap-max-size  <int>    Max allowed scaffold gap length difference. All relocations with inconsistency
	                                      less than scaffold-gap-size are counted as scaffold gap misassemblies [default: 10000]
	    --unaligned-part-size  <int>      Lower threshold for detecting partially unaligned contigs. Such contig should have
	                                      at least one unaligned fragment >= the threshold [default: 500]
	    --fragmented                      Reference genome may be fragmented into small pieces (e.g. scaffolded reference)
	    --fragmented-max-indent  <int>    Mark translocation as fake if both alignments are located no further than N bases
	                                      from the ends of the reference fragments [default: 85]
	                                      Requires --fragmented option.
	    --plots-format  <str>             Save plots in specified format [default: pdf]
	                                      Supported formats: emf, eps, pdf, png, ps, raw, rgba, svg, svgz
	    --memory-efficient                Run Nucmer using one thread, separately per each assembly and each chromosome
	                                      This may significantly reduce memory consumption on large genomes
	    --space-efficient                 Create only reports and plots files. .stdout, .stderr, .coords and other aux files will not be created
	                                      This may significantly reduce space consumption on large genomes. Icarus viewers also will not be built
	-1  --reads1  <filename>              File with forward reads (in FASTQ format, may be gzipped)
	-2  --reads2  <filename>              File with reverse reads (in FASTQ format, may be gzipped)
	    --sam  <filename>                 SAM alignment file
	    --bam  <filename>                 BAM alignment file
	                                      Reads (or SAM/BAM file) are used for structural variation detection and
	                                      coverage histogram building in Icarus
	    --sv-bedpe  <filename>            File with structural variations (in BEDPE format)

	Speedup options:
	    --no-check                        Do not check and correct input fasta files. Use at your own risk (see manual)
	    --no-plots                        Do not draw plots
	    --no-html                         Do not build html reports and Icarus viewers
	    --no-icarus                       Do not build Icarus viewers
	    --no-snps                         Do not report SNPs (may significantly reduce memory consumption on large genomes)
	    --no-gc                           Do not compute GC% and GC-distribution
	    --no-sv                           Do not run structural variation detection (make sense only if reads are specified)
	    --no-gzip                         Do not compress large output files
	    --fast                            A combination of all speedup options except --no-check

	Other:
	    --silent                          Do not print detailed information about each step to stdout (log file is not affected)
	    --test                            Run QUAST on the data from the test_data folder, output to quast_test_output
	    --test-sv                         Run QUAST with structural variants detection on the data from the test_data folder,
	                                      output to quast_test_output
	-h  --help                            Print full usage message
	-v  --version                         Print version

	Online QUAST manual is available at http://quast.sf.net/manual
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_metaquast_params(self, min_contig=False, threads="threads", scaffolds=False,
                             labels=False, L=False, eukaryote=False, gene_finding=False,
                             glimmer=False, gene_thresholds=False, max_ref_number=False,
                             blast_db=False, use_input_ref_order=False, gage=False,
                             contig_thresholds=False, use_all_alignments=False, min_alignment=False,
                             min_identity=False, ambiguity_usage=False, ambiguity_score=False,
                             unique_mapping=False, strict_NA=False, extensive_mis_size=False,
                             scaffold_gap_max_size=False, unaligned_partsize=False,
                             fragmented=False, fragmented_max_indent=False, plots_format=False,
                             memory_efficient=False, space_efficient=False, sv_bedpe=False,
                             no_check=False, no_plots=False, no_html=False, no_icarus=False,
                             no_snps=False, no_gc=False, no_sv=False, no_gzip=False, fast=False,
                             silent=False):
        """MetaQUAST: QUality ASsessment Tool for Metagenome Assemblies
	Version: 4.6.1

	Usage: python /usr/local/bin/metaquast.py [options] <files_with_contigs>

	Options:
	-o  --output-dir  <dirname>   Directory to store all result files [default: quast_results/results_<datetime>]
	-R   <filename,filename,...>  Comma-separated list of reference genomes or directory with reference genomes
	--references-list <filename>  Text file with list of reference genomes for downloading from NCBI
	-G  --genes       <filename>  File with gene coordinates in the references (GFF, BED, NCBI or TXT)
	-O  --operons     <filename>  File with operon coordinates in the reference (GFF, BED, NCBI or TXT)
	-m  --min-contig  <int>       Lower threshold for contig length [default: 500]
	-t  --threads     <int>       Maximum number of threads [default: 25% of CPUs]

	Advanced options:
	-s  --scaffolds                       Assemblies are scaffolds, split them and add contigs to the comparison
	-l  --labels "label, label, ..."      Names of assemblies to use in reports, comma-separated. If contain spaces, use quotes
	-L                                    Take assembly names from their parent directory names
	-e  --eukaryote                       Genome is eukaryotic
	-f  --gene-finding                    Predict genes using MetaGeneMark
	    --glimmer                         Use GlimmerHMM for gene prediction (instead of the default finder, see above)
	    --gene-thresholds <int,int,...>   Comma-separated list of threshold lengths of genes to search with Gene Finding module
	                                      [default: 0,300,1500,3000]
	    --max-ref-number <int>            Maximum number of references (per each assembly) to download after looking in SILVA database
	                                      Set 0 for not looking in SILVA at all [default: 50]
	    --blast-db <filename>             Custom BLAST database (.nsq file). By default, MetaQUAST searches references in SILVA database
	    --use-input-ref-order             Use provided order of references in MetaQUAST summary plots (default order: by the best average value).
	    --gage                            Use GAGE (results are in gage_report.txt)
	    --contig-thresholds <int,int,...> Comma-separated list of contig length thresholds [default: 0,1000,5000,10000,25000,50000]
	-u  --use-all-alignments              Compute genome fraction, # genes, # operons in QUAST v1.* style.
	                                      By default, QUAST filters Nucmer's alignments to keep only best ones
	-i  --min-alignment <int>             Nucmer's parameter: the minimum alignment length [default: 0]
	    --min-identity <float>            Nucmer's parameter: the minimum alignment identity (80.0, 100.0) [default: 95.0]
	-a  --ambiguity-usage <none|one|all>  Use none, one, or all alignments of a contig when all of them
	                                      are almost equally good (see --ambiguity-score) [default: one]
	    --ambiguity-score <float>         Score S for defining equally good alignments of a single contig. All alignments are sorted
	                                      by decreasing LEN * IDY% value. All alignments with LEN * IDY% < S * best(LEN * IDY%) are
	                                      discarded. S should be between 0.8 and 1.0 [default: 0.99]
	    --unique-mapping                  Disable --ambiguity-usage=all for the combined reference run,
	                                      i.e. use user-specified or default ('one') value of --ambiguity-usage
	    --strict-NA                       Break contigs in any misassembly event when compute NAx and NGAx
	                                      By default, QUAST breaks contigs only by extensive misassemblies (not local ones)
	-x  --extensive-mis-size  <int>       Lower threshold for extensive misassembly size. All relocations with inconsistency
	                                      less than extensive-mis-size are counted as local misassemblies [default: 1000]
	    --scaffold-gap-max-size  <int>    Max allowed scaffold gap length difference. All relocations with inconsistency
	                                      less than scaffold-gap-size are counted as scaffold gap misassemblies [default: 10000]
	    --unaligned-part-size  <int>      Lower threshold for detecting partially unaligned contigs. Such contig should have
	                                      at least one unaligned fragment >= the threshold [default: 500]
	    --fragmented                      Reference genome may be fragmented into small pieces (e.g. scaffolded reference)
	    --fragmented-max-indent  <int>    Mark translocation as fake if both alignments are located no further than N bases
	                                      from the ends of the reference fragments [default: 85]
	                                      Requires --fragmented option.
	    --plots-format  <str>             Save plots in specified format [default: pdf]
	                                      Supported formats: emf, eps, pdf, png, ps, raw, rgba, svg, svgz
	    --memory-efficient                Run Nucmer using one thread, separately per each assembly and each chromosome
	                                      This may significantly reduce memory consumption on large genomes
	    --space-efficient                 Create only reports and plots files. .stdout, .stderr, .coords and other aux files will not be created
	                                      This may significantly reduce space consumption on large genomes. Icarus viewers also will not be built
	-1  --reads1  <filename>              File with forward reads (in FASTQ format, may be gzipped)
	-2  --reads2  <filename>              File with reverse reads (in FASTQ format, may be gzipped)
	    --sam  <filename>                 SAM alignment file
	    --bam  <filename>                 BAM alignment file
	                                      Reads (or SAM/BAM file) are used for structural variation detection and
	                                      coverage histogram building in Icarus
	    --sv-bedpe  <filename>            File with structural variations (in BEDPE format)

	Speedup options:
	    --no-check                        Do not check and correct input fasta files. Use at your own risk (see manual)
	    --no-plots                        Do not draw plots
	    --no-html                         Do not build html reports and Icarus viewers
	    --no-icarus                       Do not build Icarus viewers
	    --no-snps                         Do not report SNPs (may significantly reduce memory consumption on large genomes)
	    --no-gc                           Do not compute GC% and GC-distribution
	    --no-sv                           Do not run structural variation detection (make sense only if reads are specified)
	    --no-gzip                         Do not compress large output files
	    --fast                            A combination of all speedup options except --no-check

	Other:
	    --silent                          Do not print detailed information about each step to stdout (log file is not affected)
	    --test                            Run MetaQUAST on the data from the test_data folder, output to quast_test_output
	    --test-no-ref                     Run MetaQUAST without references on the data from the test_data folder, output to quast_test_output
	                                      MetaQUAST will download SILVA 16S rRNA database (~170 Mb) for searching reference genomes
	                                      Internet connection is required
	-h  --help                            Print full usage message
	-v  --version                         Print version

	Online QUAST manual is available at http://quast.sf.net/manual"""
        return self

    @MultiCmdContainer.impl_run_with_list
    def run(self, sample_list, subcmd="quast",
            mount=("ref-dir", "genes", "operons", "reads1", "reads2", "sam", "bam"),
            subdir=""):
        file_list = [f.files[0].name for f in sample_list]
        params = ["-R", "-G", "-O", "--reads1", "--reads2", "--sam", "--bam"]

        mount_args = []
        for f, p in zip(mount, params):
            if f:
                mount_args += [p, os.path.split(f)[1]]

        if subcmd == "quast":
            self.cmd = [subcmd + ".py", "-o", subdir] + mount_args + \
                       self.get_opt_params("quast_params") + file_list

        elif subcmd == "metaquast":
            cmd = [subcmd + ".py", "-o", subdir] + mount_args + \
                       self.get_opt_params("metaquast_params") + file_list
            self.cmd = cmd


