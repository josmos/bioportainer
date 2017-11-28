import os
import psutil
from bioportainer.MultiCmdContainer import MultiCmdContainer
from bioportainer.Config import config


class Cd_hit_v4_6_8(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.change_out_err_log = True
        self.set_cd_hit_est_params()

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
            if v == "max_availiable_g":
                v = "{:.0f}".format(
                int((psutil.virtual_memory().available / 1024 ** 3) / config.threads))
            if v == "max_availiable_m":
                v = "{:.0f}".format(
                int((psutil.virtual_memory().available / 1024 ** 2) / config.threads))
            if type(v) == bool and v is True:
                l += ["--" + k.replace("_", "-")]
            elif type(v) == bool and v is False:
                continue

            else:
                k = k.replace("_", "-")
                l += ["-" + k, v]

        return l

    @MultiCmdContainer.impl_set_opt_params
    def set_cd_hit_est_params(self, c=False, G=False, b=False, M="max_availiable_m", T="threads",
                              n=False, l=False, d=False, s=False, S=False, aL=False, AL=False,
                              aS=False, AS=False, A=False, uL=False, uS=False, U=False, cx=False,
                              cy=False, ap=False, p=False, g=False, r=False, mask=False, match=False,
                              mismatch=False, gap=False, gap_ext=False, bak=False, sc=False, sf=False):
        """		====== CD-HIT version 4.7 (built on Nov 28 2017) ======

Usage: cd-hit-est [Options]

Options

   -i	input filename in fasta format, required
   -j	input filename in fasta/fastq format for R2 reads if input are paired end (PE) files
 	 -i R1.fq -j R2.fq -o output_R1 -op output_R2 or
 	 -i R1.fa -j R2.fa -o output_R1 -op output_R2
   -o	output filename, required
   -op	output filename for R2 reads if input are paired end (PE) files
   -c	sequence identity threshold, default 0.9
 	this is the default cd-hit's "global sequence identity" calculated as:
 	number of identical amino acids in alignment
 	divided by the full length of the shorter sequence
   -G	use global sequence identity, default 1
 	if set to 0, then use local sequence identity, calculated as :
 	number of identical amino acids in alignment
 	divided by the length of the alignment
 	NOTE!!! don't use -G 0 unless you use alignment coverage controls
 	see options -aL, -AL, -aS, -AS
   -b	band_width of alignment, default 20
   -M	memory limit (in MB) for the program, default 800; 0 for unlimitted;
   -T	number of threads, default 1; with 0, all CPUs will be used
   -n	word_length, default 10, see user's guide for choosing it
   -l	length of throw_away_sequences, default 10
   -d	length of description in .clstr file, default 20
 	if set to 0, it takes the fasta defline and stops at first space
   -s	length difference cutoff, default 0.0
 	if set to 0.9, the shorter sequences need to be
 	at least 90% length of the representative of the cluster
   -S	length difference cutoff in amino acid, default 999999
 	if set to 60, the length difference between the shorter sequences
 	and the representative of the cluster can not be bigger than 60
   -aL	alignment coverage for the longer sequence, default 0.0
 	if set to 0.9, the alignment must covers 90% of the sequence
   -AL	alignment coverage control for the longer sequence, default 99999999
 	if set to 60, and the length of the sequence is 400,
 	then the alignment must be >= 340 (400-60) residues
   -aS	alignment coverage for the shorter sequence, default 0.0
 	if set to 0.9, the alignment must covers 90% of the sequence
   -AS	alignment coverage control for the shorter sequence, default 99999999
 	if set to 60, and the length of the sequence is 400,
 	then the alignment must be >= 340 (400-60) residues
   -A	minimal alignment coverage control for the both sequences, default 0
 	alignment must cover >= this value for both sequences
   -uL	maximum unmatched percentage for the longer sequence, default 1.0
 	if set to 0.1, the unmatched region (excluding leading and tailing gaps)
 	must not be more than 10% of the sequence
   -uS	maximum unmatched percentage for the shorter sequence, default 1.0
 	if set to 0.1, the unmatched region (excluding leading and tailing gaps)
 	must not be more than 10% of the sequence
   -U	maximum unmatched length, default 99999999
 	if set to 10, the unmatched region (excluding leading and tailing gaps)
 	must not be more than 10 bases
   -B	1 or 0, default 0, by default, sequences are stored in RAM
 	if set to 1, sequence are stored on hard drive
 	!! No longer supported !!
   -P	input paired end (PE) reads, default 0, single file
 	if set to 1, please use -i R1 -j R2 to input both PE files
   -cx	length to keep after trimming the tail of sequence, default 0, not trimming
 	if set to 50, the program only uses the first 50 letters of input sequence
   -cy	length to keep after trimming the tail of R2 sequence, default 0, not trimming
 	if set to 50, the program only uses the first 50 letters of input R2 sequence
 	e.g. -cx 100 -cy 80 for paired end reads
   -ap	alignment position constrains,  default 0, no constrain
 	if set to 1, the program will force sequences to align at beginings
 	when set to 1, the program only does +/+ alignment
   -p	1 or 0, default 0
 	if set to 1, print alignment overlap in .clstr file
   -g	1 or 0, default 0
 	by cd-hit's default algorithm, a sequence is clustered to the first
 	cluster that meet the threshold (fast cluster). If set to 1, the program
 	will cluster it into the most similar cluster that meet the threshold
 	(accurate but slow mode)
 	but either 1 or 0 won't change the representatives of final clusters
   -r	1 or 0, default 1, by default do both +/+ & +/- alignments
 	if set to 0, only +/+ strand alignment
   -mask	masking letters (e.g. -mask NX, to mask out both 'N' and 'X')
   -match	matching score, default 2 (1 for T-U and N-N)
   -mismatch	mismatching score, default -2
   -gap	gap opening score, default -6
   -gap-ext	gap extension score, default -1
   -bak	write backup cluster file (1 or 0, default 0)
   -sc	sort clusters by size (number of sequences), default 0, output clusters by decreasing length
 	if set to 1, output clusters by decreasing size
   -sf	sort fasta/fastq by cluster size (number of sequences), default 0, no sorting
 	if set to 1, output sequences by decreasing cluster size
   -h	print this help

   Questions, bugs, contact Limin Fu at l2fu@ucsd.edu, or Weizhong Li at liwz@sdsc.edu
   For updated versions and information, please visit: http://cd-hit.org

   cd-hit web server is also available from http://cd-hit.org

   If you find cd-hit useful, please kindly cite:

   "CD-HIT: a fast program for clustering and comparing large sets of protein or nucleotide sequences", Weizhong Li & Adam Godzik. Bioinformatics, (2006) 22:1658-1659
   "CD-HIT: accelerated for clustering the next generation sequencing data", Limin Fu, Beifang Niu, Zhengwei Zhu, Sitao Wu & Weizhong Li. Bioinformatics, (2012) 28:3150-3152
"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="cd-hit-est", output_postfix="_cdhit", input_type="fasta-pe"):
        self.input_type = input_type
        self.output_type = "out"
        if subcmd == "cd-hit-est":
            if self.input_type in ["fastq-pe", "fastq-pe-gz", "fasta-pe", "fasta-pe-gz"]:
                input = ["-i", sample_io.files[0].name, "-j", sample_io.files[1].name, "-P", "1"]
                out = ["-o", sample_io.id + output_postfix + "_1", "-op", sample_io.id + output_postfix + "_2",]
            elif self.input_type in ["fastq-se", "fastq-se-gz", "fasta-se", "fasta-se-gz", "fastq-inter",
                                     "fastq-inter-gz", "fasta-inter", "fasta-inter-gz"]:
                input = ["-i", sample_io.files[0].name]
                out = ["-o", sample_io.id + output_postfix]
            else:
                raise IOError

            self.cmd = [subcmd] + input + out + self.get_opt_params("cd_hit_est_params") + [">", sample_io.id + output_postfix + ".out"]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="cd-hit-est", output_postfix="_cdhit", input_type="fasta-pe"):
        pass
