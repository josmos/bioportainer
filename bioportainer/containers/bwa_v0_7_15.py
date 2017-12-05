import os

from bioportainer.MultiCmdContainer import MultiCmdContainer

from bioportainer.Config import config


class Bwa_v0_7_15(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_index_params()
        self.set_mem_params()


    @MultiCmdContainer.impl_set_opt_params
    def set_index_params(self, a=False, p=False, b=False):
        """Usage:   bwa index [options] <in.fasta>

Options: -a STR    BWT construction algorithm: bwtsw or is [auto]
         -p STR    prefix of the index [same as fasta name]
         -b INT    block size for the bwtsw algorithm (effective with -a bwtsw) [10000000]
         -6        index files named as <in.fasta>.64.* instead of <in.fasta>.*

Warning: `-a bwtsw' does not work for short genomes, while `-a is' and
         `-a div' do not work not for long genomes.
"""

        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_mem_params(self, t="threads", k=False, w=False, d=False, r=False, y=False, c=False,
                           D=False, W=False, m=False, S=False, P=False, A=False,B=False, O=False,
                           E=False, L=False, U=False, x=False, p=False, R=False, H=False, j=False,
                           v=False, T=False, h=False, a=False, C=False, V=False, Y=False, M=False,
                           I=False):
        """Usage: bwa mem [options] <idxbase> <in1.fq> [in2.fq]

Algorithm options:

       -t INT        number of threads [1]
       -k INT        minimum seed length [19]
       -w INT        band width for banded alignment [100]
       -d INT        off-diagonal X-dropoff [100]
       -r FLOAT      look for internal seeds inside a seed longer than {-k} * FLOAT [1.5]
       -y INT        seed occurrence for the 3rd round seeding [20]
       -c INT        skip seeds with more than INT occurrences [500]
       -D FLOAT      drop chains shorter than FLOAT fraction of the longest overlapping chain [0.50]
       -W INT        discard a chain if seeded bases shorter than INT [0]
       -m INT        perform at most INT rounds of mate rescues for each read [50]
       -S            skip mate rescue
       -P            skip pairing; mate rescue performed unless -S also in use

Scoring options:

       -A INT        score for a sequence match, which scales options -TdBOELU unless overridden [1]
       -B INT        penalty for a mismatch [4]
       -O INT[,INT]  gap open penalties for deletions and insertions [6,6]
       -E INT[,INT]  gap extension penalty; a gap of size k cost '{-O} + {-E}*k' [1,1]
       -L INT[,INT]  penalty for 5'- and 3'-end clipping [5,5]
       -U INT        penalty for an unpaired read pair [17]

       -x STR        read type. Setting -x changes multiple parameters unless overriden [null]
                     pacbio: -k17 -W40 -r10 -A1 -B1 -O1 -E1 -L0  (PacBio reads to ref)
                     ont2d: -k14 -W20 -r10 -A1 -B1 -O1 -E1 -L0  (Oxford Nanopore 2D-reads to ref)
                     intractg: -B9 -O16 -L5  (intra-species contigs to ref)

Input/output options:

       -p            smart pairing (ignoring in2.fq)
       -R STR        read group header line such as '@RG\tID:foo\tSM:bar' [null]
       -H STR/FILE   insert STR to header if it starts with @; or insert lines in FILE [null]
       -j            treat ALT contigs as part of the primary assembly (i.e. ignore <idxbase>.alt file)

       -v INT        verbose level: 1=error, 2=warning, 3=message, 4+=debugging [3]
       -T INT        minimum score to output [30]
       -h INT[,INT]  if there are <INT hits with score >80% of the max score, output all in XA [0,0]
       -a            output all alignments for SE or unpaired PE
       -C            append FASTA/FASTQ comment to SAM output
       -V            output the reference FASTA header in the XR tag
       -Y            use soft clipping for supplementary alignments
       -M            mark shorter split hits as secondary

       -I FLOAT[,FLOAT[,INT[,INT]]]
                     specify the mean, standard deviation (10% of the mean if absent), max
                     (4 sigma from the mean if absent) and min of the insert size distribution.
                     FR orientation only. [inferred]

Note: Please read the man page for detailed description of the command line and options.
"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, ref_io, subcmd="mem", output_postfix=""):
        """
        :param sampleIO: input object with input files
        :param subcmd: "bowtie2" or "bowtie2-build" or "bowtie2-inspect"
        :return: sampleIO object with output files
        bwa mem [options] <idxbase> <in1.fq> [in2.fq]
        """
        if subcmd == "mem":
            self.output_type = "sam"
            out = sample_io.id + output_postfix + ".sam"
            if len(sample_io.files) >= 2:
                input = [sample_io.files[0].name, sample_io.files[1].name]
            else:
                input = [sample_io.files[0].name]

            self.cmd = ["bwa", subcmd] + self.get_opt_params("mem_params") + \
                       [self.index_prefix] + input + [">", out]

        elif subcmd == "index":
            self.output_type = None
            self.sample_dir = os.path.join(config.work_dir, ref_io.host_dir)
            self.index_path = self.out_dir
            self.index_prefix = os.path.basename(ref_io.files[0].name)
            self.cmd = ["bwa", subcmd] + self.get_opt_params("index_params") + [ref_io.files[0].name]


    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, ref_io, subcmd="mem", output_postfix=""):
        pass


