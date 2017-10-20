import os

from bioportainer.MultiCmdContainer import MultiCmdContainer

from bioportainer.Config import config


class Bowtie2(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_bowtie2_build_params()
        self.set_bowtie2_inspect_params()
        self.set_bowtie2_params()

    @MultiCmdContainer.impl_set_opt_params
    def set_bowtie2_params(self, qseq=False, f=False, skip="none", upto=False, trim5="0", trim3="0",
                           phred33=True, phred64=False, int_quals=False, end_to_end=True,
                           very_fast=False, fast=False, sensitive=True, very_sensitive=False,
                           local=False, very_fast_local=False, fast_local=False,
                           sensitive_local=False, very_sensitive_local=False, N="0", L="22",
                           i="S,1,1.15", n_ceil="L,0,0.15", dpad="15", gbar="4", ignore_quals=False,
                           nofw=False, norc=False, no_1mm_upfront=False, ma="0", mp="6", np="1",
                           rdg="5,3", rfg="5,3", score_min="L,-0.6,-0.6", k=False, all=False, D="0",
                           R="2", minins="0", maxins="500", no_mixed=False, no_discordant=False,
                           no_dovetail=False, no_contain=False, no_overlap=False, time=False,
                           un=False, al=False, un_conc=False, al_conc=False, un_gz=False,
                           quiet=False, met_file=False, met_stderr=False, met=False, no_unal=False,
                           no_head=False, no_sq=False, rg_id=False, omit_sec_seq=False,
                           reorder=False, mm=False, qc_filter=False, seed="0",
                           non_deterministic=False, threads="threads"):
        """
        Bowtie 2 version 2.2.9 by Ben Langmead (langmea@cs.jhu.edu, www.cs.jhu.edu/~langmea)
	Usage:
	  bowtie2 [options]* -x <bt2-idx> {-1 <m1> -2 <m2> | -U <r>} [-S <sam>]

	  <bt2-idx>  Index filename prefix (minus trailing .X.bt2).
	             NOTE: Bowtie 1 and Bowtie 2 indexes are not compatible.
	  <m1>       Files with #1 mates, paired with files in <m2>.
	             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
	  <m2>       Files with #2 mates, paired with files in <m1>.
	             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
	  <r>        Files with unpaired reads.
	             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
	  <sam>      File for SAM output (default: stdout)

	  <m1>, <m2>, <r> can be comma-separated lists (no whitespace) and can be
	  specified many times.  E.g. '-U file1.fq,file2.fq -U file3.fq'.

	Options (defaults in parentheses):

	 Input:
	  -q                 query input files are FASTQ .fq/.fastq (default)
	  --qseq             query input files are in Illumina's qseq format
	  -f                 query input files are (multi-)FASTA .fa/.mfa
	  -r                 query input files are raw one-sequence-per-line
	  -c                 <m1>, <m2>, <r> are sequences themselves, not files
	  -s/--skip <int>    skip the first <int> reads/pairs in the input (none)
	  -u/--upto <int>    stop after first <int> reads/pairs (no limit)
	  -5/--trim5 <int>   trim <int> bases from 5'/left end of reads (0)
	  -3/--trim3 <int>   trim <int> bases from 3'/right end of reads (0)
	  --phred33          qualities are Phred+33 (default)
	  --phred64          qualities are Phred+64
	  --int-quals        qualities encoded as space-delimited integers

	 Presets:                 Same as:
	  For --end-to-end:
	   --very-fast            -D 5 -R 1 -N 0 -L 22 -i S,0,2.50
	   --fast                 -D 10 -R 2 -N 0 -L 22 -i S,0,2.50
	   --sensitive            -D 15 -R 2 -N 0 -L 22 -i S,1,1.15 (default)
	   --very-sensitive       -D 20 -R 3 -N 0 -L 20 -i S,1,0.50

	  For --local:
	   --very-fast-local      -D 5 -R 1 -N 0 -L 25 -i S,1,2.00
	   --fast-local           -D 10 -R 2 -N 0 -L 22 -i S,1,1.75
	   --sensitive-local      -D 15 -R 2 -N 0 -L 20 -i S,1,0.75 (default)
	   --very-sensitive-local -D 20 -R 3 -N 0 -L 20 -i S,1,0.50

	 Alignment:
	  -N <int>           max # mismatches in seed alignment; can be 0 or 1 (0)
	  -L <int>           length of seed substrings; must be >3, <32 (22)
	  -i <func>          interval between seed substrings w/r/t read len (S,1,1.15)
	  --n-ceil <func>    func for max # non-A/C/G/Ts permitted in aln (L,0,0.15)
	  --dpad <int>       include <int> extra ref chars on sides of DP table (15)
	  --gbar <int>       disallow gaps within <int> nucs of read extremes (4)
	  --ignore-quals     treat all quality values as 30 on Phred scale (off)
	  --nofw             do not align forward (original) version of read (off)
	  --norc             do not align reverse-complement version of read (off)
	  --no-1mm-upfront   do not allow 1 mismatch alignments before attempting to
	                     scan for the optimal seeded alignments
	  --end-to-end       entire read must align; no clipping (on)
	   OR
	  --local            local alignment; ends might be soft clipped (off)

	 Scoring:
	  --ma <int>         match bonus (0 for --end-to-end, 2 for --local)
	  --mp <int>         max penalty for mismatch; lower qual = lower penalty (6)
	  --np <int>         penalty for non-A/C/G/Ts in read/ref (1)
	  --rdg <int>,<int>  read gap open, extend penalties (5,3)
	  --rfg <int>,<int>  reference gap open, extend penalties (5,3)
	  --score-min <func> min acceptable alignment score w/r/t read length
	                     (G,20,8 for local, L,-0.6,-0.6 for end-to-end)

	 Reporting:
	  (default)          look for multiple alignments, report best, with MAPQ
	   OR
	  -k <int>           report up to <int> alns per read; MAPQ not meaningful
	   OR
	  -a/--all           report all alignments; very slow, MAPQ not meaningful

	 Effort:
	  -D <int>           give up extending after <int> failed extends in a row (15)
	  -R <int>           for reads w/ repetitive seeds, try <int> sets of seeds (2)

	 Paired-end:
	  -I/--minins <int>  minimum fragment length (0)
	  -X/--maxins <int>  maximum fragment length (500)
	  --fr/--rf/--ff     -1, -2 mates align fw/rev, rev/fw, fw/fw (--fr)
	  --no-mixed         suppress unpaired alignments for paired reads
	  --no-discordant    suppress discordant alignments for paired reads
	  --no-dovetail      not concordant when mates extend past each other
	  --no-contain       not concordant when one mate alignment contains other
	  --no-overlap       not concordant when mates overlap at all

	 Output:
	  -t/--time          print wall-clock time taken by search phases
	  --un <path>           write unpaired reads that didn't align to <path>
	  --al <path>           write unpaired reads that aligned at least once to <path>
	  --un-conc <path>      write pairs that didn't align concordantly to <path>
	  --al-conc <path>      write pairs that aligned concordantly at least once to <path>
	  (Note: for --un, --al, --un-conc, or --al-conc, add '-gz' to the option name, e.g.
	  --un-gz <path>, to gzip compress output, or add '-bz2' to bzip2 compress output.)
	  --quiet            print nothing to stderr except serious errors
	  --met-file <path>  send metrics to file at <path> (off)
	  --met-stderr       send metrics to stderr (off)
	  --met <int>        report internal counters & metrics every <int> secs (1)
	  --no-unal          suppress SAM records for unaligned reads
	  --no-head          suppress header lines, i.e. lines starting with @
	  --no-sq            suppress @SQ header lines
	  --rg-id <text>     set read group id, reflected in @RG line and RG:Z: opt field
	  --rg <text>        add <text> ("lab:value") to @RG line of SAM header.
	                     Note: @RG line only printed when --rg-id is set.
	  --omit-sec-seq     put '*' in SEQ and QUAL fields for secondary alignments.

	 Performance:
	  -p/--threads <int> number of alignment threads to launch (1)
	  --reorder          force SAM output order to match order of input reads
	  --mm               use memory-mapped I/O for index; many 'bowtie's can share

	 Other:
	  --qc-filter        filter out reads that are bad according to QSEQ filter
	  --seed <int>       seed for random number generator (0)
	  --non-deterministic seed rand. gen. arbitrarily instead of using read attributes
	  --version          print version information and quit
	  -h/--help          print this usage message
        :return:
        """
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_bowtie2_build_params(self, threads="threads", f=False,
                                 large_index=False, noauto=False, packed=False, bmax=False,
                                 bmaxdivn="4", dcv="1024", nodc=False, noref=False, justref=False,
                                 offrate="5", ftabchars="10", seed=False, quiet=True):
        """
        bowtie2-build [options]* <reference_in> <bt2_index_base>
            reference_in            comma-separated list of files with ref sequences
            bt2_index_base          write bt2 data to files with this host_dir/basename

        :param threads: of threads
        :param f: reference files are Fasta (default)
        :param large_index: force generated index to be 'large', even if ref
                            has fewer than 4 billion nucleotides
        :param noauto: disable automatic -p/--bmax/--dcv memory-fitting
        :param packed: use packed strings internally; slower, less memory
        :param bmax: max bucket sz for blockwise suffix-array builder
        :param bmaxdivn: max bucket sz as divisor of ref len (default: 4)
        :param dcv: diff-cover period for blockwise (default: 1024)
        :param nodc: disable diff-cover (algorithm becomes quadratic)
        :param noref: don't build .3/.4 index files
        :param justref:  just build .3/.4 index files
        :param offrate:  SA is sampled every 2^<int> BWT chars (default: 5)
        :param ftabchars: of chars consumed in initial lookup (default: 10)
        :param seed: seed for random number generator <int or False>
        :param quiet: verbose output (for debugging)
        :return:
        """
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_bowtie2_inspect_params(self, large_index=False, across="60", names=False, summary=False,
                                   bt2_ref=False):
        """
        Bowtie 2 version 2.2.9 by Ben Langmead (langmea@cs.jhu.edu, www.cs.jhu.edu/~langmea)
	Usage: bowtie2-inspect [options]* <bt2_base>
	  <bt2_base>         bt2 filename minus trailing .1.bt2/.2.bt2

	  By default, prints FASTA records of the indexed nucleotide sequences to
	  standard out.  With -n, just prints names.  With -s, just prints a summary of
	  the index parameters and sequences.  With -e, preserves colors if applicable.

	Options:
	  --large-index      force inspection of the 'large' index, even if a
	                     'small' one is present.
	  -a/--across <int>  Number of characters across in FASTA output (default: 60)
	  -n/--names         Print reference sequence names only
	  -s/--summary       Print summary incl. ref names, lengths, index properties
	  -e/--bt2-ref      Reconstruct reference from .bt2 (slow, preserves colors)
	  -v/--verbose       Verbose output (for debugging)
	  -h/--help          print detailed description of tool and its options
	  --help             print this usage message
        :param h:
        :return:
        """
        return self

    @MultiCmdContainer.impl_run
    def run(self, paired_io, unpaired_io, ref_io, subcmd="bowtie2"):
        """
        :param sampleIO: input object with input files
        :param subcmd: "bowtie2" or "bowtie2-build" or "bowtie2-inspect"
        :return: sampleIO object with output files
        """
        if subcmd == "bowtie2":
            self.index_prefix = os.path.splitext(os.path.basename(ref_io.files[0].name))[0]
            self.output_type = "sam"
            if paired_io:
                out = paired_io.id + ".sam"
                self.input_allowed = ["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz"]
                input = ["-1", paired_io.files[0].name, "-2", paired_io.files[1].name]
                if unpaired_io is not None: #and unpaired_io.io_type == "fastq-pe" or "fastq-pe-gz":
                    input += ["-U", ",".join([f.name for f in unpaired_io.files])]

            elif unpaired_io and unpaired_io.io_type == "fastq-se" or "fastq-se-gz":
                out = unpaired_io.id + ".sam"
                input = ["-U", ",".join([f.name for f in unpaired_io.files])]
            else:
                raise IOError

            self.cmd = [subcmd] + self.get_opt_params("bowtie2_params") + \
                       ["-x", self.index_prefix] + input + ["-S", out]

        elif subcmd == "bowtie2-build":
            self.output_type = "bt2"
            self.input_allowed = ["fasta-se"]
            self.sample_dir = os.path.join(config.work_dir, ref_io.host_dir)
            self.index_prefix = os.path.splitext(os.path.basename(ref_io.files[0].name))[0]
            self.index_path = os.path.split(ref_io.files[0].file_path)[0]
            self.cmd = [subcmd] + self.get_opt_params("bowtie2_build_params") + \
                       [",".join([f.name for f in ref_io.files]), self.index_prefix]

        elif subcmd == "bowtie2-inspect":
            self.input_allowed = ["bt2"]
            self.cmd = [subcmd] + self.get_opt_params("bowtie2_inspect_params") + [self.index_prefix]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, ref_io, paired_io, unpaired_io, subcmd="bowtie2"):
        pass


