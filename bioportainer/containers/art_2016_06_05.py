import os
from bioportainer.MultiCmdContainer import MultiCmdContainer
from bioportainer.Config import config


class Art_2016_06_05(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_art_illumina_params()
        self.set_art_profiler_illumina_params()

    @MultiCmdContainer.impl_set_opt_params
    def set_art_profiler_illumina_params(self, threads="threads"):
        """This tool is to create an Illumina read quality profile from multiple fastq or gzipped fastq files

USAGE:
	./art_profiler_illumina output_profile_name input_fastq_dir fastq_filename_extension [max_number_threads]

PARAMETERS:
	output_profile_name:  the name of read quality profile to be generated
	input_fastq_dir:   the directory of input fastq or zipped fastq files
	fastq_filename_extension: fastq or gzipped fastq filename extension
	max_number_threads:: maximum number of threads/cores to be used for the run (default: all cores)

EXAMPLES:
	1) create hiseq2k profiles from all *.fq.gz in the directory fastq_dat_dir
		./art_profiler_illumina hiseq2k fastq_dat_dir fq.gz
	2) create miseq2500 profiles from all *.fq in the directory fastq_dat_dir
		./art_profiler_illumina miseq250 fastq_dat_dir fq
	3) create hiseq1k profiles from all *.fq in the directory fastq_dat_dir using 20 threads
		./art_profiler_illumina hiseq1k fastq_dat_dir fq 20

NOTES: For paired-end fastq files, e.g., *.fq or *.fq.gz,
       the filenames of the 1st reads must be *_1.fq/*_1.fq.gz, or *.1.fq/*.1.fq.gz
       and those of the 2nd reads must be *_2.fq./*_2.fq.gz, or *.2.fq or *.2.fq.gz

CONTACT: Weichun Huang at whduke@gmail.com
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_art_illumina_params(self,qprof1=False, qprof2=False, amplicon=False, rcount=False,
                                id=False, errfree=False, fcov=False, insRate=False, insRate2=False,
                                delRate=False, delRate2=False, maxIndel=False, mflen=False,
                                matepair=False, cigarM=False, maskN=False, noALN=False, paired=False,
                                quiet=False, minQ=False, maxQ=False, qShift=False, qShift2=False,
                                rndSeed=42, sdev=False, samout=False, sepProf=False):
        """    ====================ART====================
             ART_Illumina (2008-2016)
          Q Version 2.5.8 (June 6, 2016)
     Contact: Weichun Huang <whduke@gmail.com>
    -------------------------------------------

===== USAGE =====

art_illumina [options] -ss <sequencing_system> -sam -i <seq_ref_file> -l <read_length> -f <fold_coverage> -o <outfile_prefix>
art_illumina [options] -ss <sequencing_system> -sam -i <seq_ref_file> -l <read_length> -c <num_reads_per_sequence> -o <outfile_prefix>
art_illumina [options] -ss <sequencing_system> -sam -i <seq_ref_file> -l <read_length> -f <fold_coverage> -m <mean_fragsize> -s <std_fragsize> -o <outfile_prefix>
art_illumina [options] -ss <sequencing_system> -sam -i <seq_ref_file> -l <read_length> -c <num_reads_per_sequence> -m <mean_fragsize> -s <std_fragsize> -o <outfile_prefix>

===== PARAMETERS =====

  -1   --qprof1   the first-read quality profile
  -2   --qprof2   the second-read quality profile
  -amp --amplicon amplicon sequencing simulation
  -c   --rcount   number of reads/read pairs to be generated per sequence/amplicon (not be used together with -f/--fcov)
  -d   --id       the prefix identification tag for read ID
  -ef  --errfree  indicate to generate the zero sequencing errors SAM file as well the regular one
                  NOTE: the reads in the zero-error SAM file have the same alignment positions
                  as those in the regular SAM file, but have no sequencing errors
  -f   --fcov     the fold of read coverage to be simulated or number of reads/read pairs generated for each amplicon
  -h   --help     print out usage information
  -i   --in       the filename of input DNA/RNA reference
  -ir  --insRate  the first-read insertion rate (default: 0.00009)
  -ir2 --insRate2 the second-read insertion rate (default: 0.00015)
  -dr  --delRate  the first-read deletion rate (default:  0.00011)
  -dr2 --delRate2 the second-read deletion rate (default: 0.00023)
  -k   --maxIndel the maximum total number of insertion and deletion per read (default: up to read length)
  -l   --len      the length of reads to be simulated
  -m   --mflen    the mean size of DNA/RNA fragments for paired-end simulations
  -mp  --matepair indicate a mate-pair read simulation
  -M  --cigarM    indicate to use CIGAR 'M' instead of '=/X' for alignment match/mismatch
  -nf  --maskN    the cutoff frequency of 'N' in a window size of the read length for masking genomic regions
                  NOTE: default: '-nf 1' to mask all regions with 'N'. Use '-nf 0' to turn off masking
  -na  --noALN    do not output ALN alignment file
  -o   --out      the prefix of output filename
  -p   --paired   indicate a paired-end read simulation or to generate reads from both ends of amplicons
                  NOTE: art will automatically switch to a mate-pair simulation if the given mean fragment size >= 2000
  -q   --quiet    turn off end of run summary
  -qL  --minQ     the minimum base quality score
  -qU  --maxQ     the maxiumum base quality score
  -qs  --qShift   the amount to shift every first-read quality score by
  -qs2 --qShift2  the amount to shift every second-read quality score by
                  NOTE: For -qs/-qs2 option, a positive number will shift up quality scores (the max is 93)
                  that reduce substitution sequencing errors and a negative number will shift down
                  quality scores that increase sequencing errors. If shifting scores by x, the error
                  rate will be 1/(10^(x/10)) of the default profile.
  -rs  --rndSeed  the seed for random number generator (default: system time in second)
                  NOTE: using a fixed seed to generate two identical datasets from different runs
  -s   --sdev     the standard deviation of DNA/RNA fragment size for paired-end simulations.
  -sam --samout   indicate to generate SAM alignment file
  -sp  --sepProf  indicate to use separate quality profiles for different bases (ATGC)
  -ss  --seqSys   The name of Illumina sequencing system of the built-in profile used for simulation
       NOTE: sequencing system ID names are:
            GA1 - GenomeAnalyzer I (36bp,44bp), GA2 - GenomeAnalyzer II (50bp, 75bp)
           HS10 - HiSeq 1000 (100bp),          HS20 - HiSeq 2000 (100bp),      HS25 - HiSeq 2500 (125bp, 150bp)
           HSXn - HiSeqX PCR free (150bp),     HSXt - HiSeqX TruSeq (150bp),   MinS - MiniSeq TruSeq (50bp)
           MSv1 - MiSeq v1 (250bp),            MSv3 - MiSeq v3 (250bp),        NS50 - NextSeq500 v2 (75bp)
===== NOTES =====

* ART by default selects a built-in quality score profile according to the read length specified for the run.

* For single-end simulation, ART requires input sequence file, output file prefix, read length, and read count/fold coverage.

* For paired-end simulation (except for amplicon sequencing), ART also requires the parameter values of
  the mean and standard deviation of DNA/RNA fragment lengths

===== EXAMPLES =====

 1) single-end read simulation
 	art_illumina -ss HS25 -sam -i reference.fa -l 150 -f 10 -o single_dat

 2) paired-end read simulation
       art_illumina -ss HS25 -sam -i reference.fa -p -l 150 -f 20 -m 200 -s 10 -o paired_dat

 3) mate-pair read simulation
       art_illumina -ss HS10 -sam -i reference.fa -mp -l 100 -f 20 -m 2500 -s 50 -o matepair_dat

 4) amplicon sequencing simulation with 5' end single-end reads
 	art_illumina -ss GA2 -amp -sam -na -i amp_reference.fa -l 50 -f 10 -o amplicon_5end_dat

 5) amplicon sequencing simulation with paired-end reads
       art_illumina -ss GA2 -amp -p -sam -na -i amp_reference.fa -l 50 -f 10 -o amplicon_pair_dat

 6) amplicon sequencing simulation with matepair reads
       art_illumina -ss MSv1 -amp -mp -sam -na -i amp_reference.fa -l 150 -f 10 -o amplicon_mate_dat

 7) generate an extra SAM file with zero-sequencing errors for a paired-end read simulation
       art_illumina -ss HSXn -ef -i reference.fa -p -l 150 -f 20 -m 200 -s 10 -o paired_twosam_dat

 8) reduce the substitution error rate to one 10th of the default profile
       art_illumina -i reference.fa -qs 10 -qs2 10 -l 50 -f 10 -p -m 500 -s 10 -sam -o reduce_error

 9) turn off the masking of genomic regions with unknown nucleotides 'N'
       art_illumina -ss HS20 -nf 0  -sam -i reference.fa -p -l 100 -f 20 -m 200 -s 10 -o paired_nomask

 10) masking genomic regions with >=5 'N's within the read length 50
       art_illumina -ss HSXt -nf 5 -sam -i reference.fa -p -l 150 -f 20 -m 200 -s 10 -o paired_maskN5

"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="art_illumina", out_name="", seqSys="MSv3", len="250",  mount=None):
        self.input_type = "fasta-se"
        if subcmd == "art_illumina":
            self.cmd = [subcmd, "--seqSys", seqSys, "-i", sample_io.files[0].name, "-l", len,
                        "-o", out_name] + self.get_opt_params("art_illumina_params")
        if subcmd == "art_profiler_illumina":
            ext = ".".join(sample_io.files[0].name.split(os.extsep)[1:])
            t = self.get_opt_params("art_profiler_illumina_params")[1]
            self.cmd = [subcmd, out_name, ".", ext, t]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="art_illumina", out_name="", input_type="fastq-pe", mount=None):
        pass



