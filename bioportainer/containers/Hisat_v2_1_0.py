import os

from bioportainer.MultiCmdContainer import MultiCmdContainer

from bioportainer.Config import config


class Hisat_v2_1_0(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_hisat2_build_params()
        self.set_hisat2_inspect_params()
        self.set_hisat2_params()

    @MultiCmdContainer.impl_set_opt_params
    def set_hisat2_params(self, q=True, qseq=False, f=False, r=False , s=False, u=False, trim5="0",
                          trim3="0", phred33=True, phred64=False, int_quals=False, sra_acc=False,
                          n_ceil="L,0,0.15", ignore_quals=False, nofw=False, norc=False,
                          pen_cansplice="0", pen_noncansplice="12", pen_canintronlen="G,-8,1",
                          pen_noncanintronlen="G,-8,1", min_intronlen="20", max_intronlen="500000",
                          known_splicesite_infile=False, novel_splicesite_outfile=False,
                          novel_splicesite_infile=False, no_temp_splicesite=False,
                          no_spliced_alignment=False, rna_strandness="unstranded", tmo=False, dta=False,
                          dta_cufflinks=False, avoid_pseudogene=False, no_templatelen_adjustment=False,
                          mp="6,2", sp="2,1", no_softclip=False, np="1", rdg="5,3", rfg="5,3",
                          score_min="L,0.0,-0.2", k="5", minins=False,maxins=False, fr=True, rf=False,
                          ff=False, no_mixed=False, no_discordant=False, time=True, un=False,
                          al=False, un_conc=False, al_conc=False, summary_file=False, new_summary=False,
                          quiet=False, met_file=False, met_stderr=False, met="1", no_head=False, no_sq=False,
                          rg_id=False, rg=False,omit_sec_seq=False, offrate=False, p="threads", reorder="False",
                          mm=False, qc_filter=False, seed="0", non_deterministic=False, remove_chrname=False,
                          dd_chrname=False):
        """HISAT2 version 2.1.0 by Daehwan Kim (infphilo@gmail.com, www.ccb.jhu.edu/people/infphilo)
Usage:
  hisat2 [options]* -x <ht2-idx> {-1 <m1> -2 <m2> | -U <r> | --sra-acc <SRA accession number>} [-S <sam>]

  <ht2-idx>  Index filename prefix (minus trailing .X.ht2).
  <m1>       Files with #1 mates, paired with files in <m2>.
             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
  <m2>       Files with #2 mates, paired with files in <m1>.
             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
  <r>        Files with unpaired reads.
             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
  <SRA accession number>        Comma-separated list of SRA accession numbers, e.g. --sra-acc SRR353653,SRR353654.
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
  --sra-acc          SRA accession ID

 Alignment:
  --n-ceil <func>    func for max # non-A/C/G/Ts permitted in aln (L,0,0.15)
  --ignore-quals     treat all quality values as 30 on Phred scale (off)
  --nofw             do not align forward (original) version of read (off)
  --norc             do not align reverse-complement version of read (off)

 Spliced Alignment:
  --pen-cansplice <int>              penalty for a canonical splice site (0)
  --pen-noncansplice <int>           penalty for a non-canonical splice site (12)
  --pen-canintronlen <func>          penalty for long introns (G,-8,1) with canonical splice sites
  --pen-noncanintronlen <func>       penalty for long introns (G,-8,1) with noncanonical splice sites
  --min-intronlen <int>              minimum intron length (20)
  --max-intronlen <int>              maximum intron length (500000)
  --known-splicesite-infile <path>   provide a list of known splice sites
  --novel-splicesite-outfile <path>  report a list of splice sites
  --novel-splicesite-infile <path>   provide a list of novel splice sites
  --no-temp-splicesite               disable the use of splice sites found
  --no-spliced-alignment             disable spliced alignment
  --rna-strandness <string>          specify strand-specific information (unstranded)
  --tmo                              reports only those alignments within known transcriptome
  --dta                              reports alignments tailored for transcript assemblers
  --dta-cufflinks                    reports alignments tailored specifically for cufflinks
  --avoid-pseudogene                 tries to avoid aligning reads to pseudogenes (experimental option)
  --no-templatelen-adjustment        disables template length adjustment for RNA-seq reads

 Scoring:
  --mp <int>,<int>   max and min penalties for mismatch; lower qual = lower penalty <6,2>
  --sp <int>,<int>   max and min penalties for soft-clipping; lower qual = lower penalty <2,1>
  --no-softclip      no soft-clipping
  --np <int>         penalty for non-A/C/G/Ts in read/ref (1)
  --rdg <int>,<int>  read gap open, extend penalties (5,3)
  --rfg <int>,<int>  reference gap open, extend penalties (5,3)
  --score-min <func> min acceptable alignment score w/r/t read length
                     (L,0.0,-0.2)

 Reporting:
  -k <int> (default: 5) report up to <int> alns per read

 Paired-end:
  -I/--minins <int>  minimum fragment length (0), only valid with --no-spliced-alignment
  -X/--maxins <int>  maximum fragment length (500), only valid with --no-spliced-alignment
  --fr/--rf/--ff     -1, -2 mates align fw/rev, rev/fw, fw/fw (--fr)
  --no-mixed         suppress unpaired alignments for paired reads
  --no-discordant    suppress discordant alignments for paired reads

 Output:
  -t/--time          print wall-clock time taken by search phases
  --un <path>           write unpaired reads that didn't align to <path>
  --al <path>           write unpaired reads that aligned at least once to <path>
  --un-conc <path>      write pairs that didn't align concordantly to <path>
  --al-conc <path>      write pairs that aligned concordantly at least once to <path>
  (Note: for --un, --al, --un-conc, or --al-conc, add '-gz' to the option name, e.g.
  --un-gz <path>, to gzip compress output, or add '-bz2' to bzip2 compress output.)
  --summary-file     print alignment summary to this file.
  --new-summary      print alignment summary in a new style, which is more machine-friendly.
  --quiet            print nothing to stderr except serious errors
  --met-file <path>  send metrics to file at <path> (off)
  --met-stderr       send metrics to stderr (off)
  --met <int>        report internal counters & metrics every <int> secs (1)
  --no-head          supppress header lines, i.e. lines starting with @
  --no-sq            supppress @SQ header lines
  --rg-id <text>     set read group id, reflected in @RG line and RG:Z: opt field
  --rg <text>        add <text> ("lab:value") to @RG line of SAM header.
                     Note: @RG line only printed when --rg-id is set.
  --omit-sec-seq     put '*' in SEQ and QUAL fields for secondary alignments.

 Performance:
  -o/--offrate <int> override offrate of index; must be >= index's offrate
  -p/--threads <int> number of alignment threads to launch (1)
  --reorder          force SAM output order to match order of input reads
  --mm               use memory-mapped I/O for index; many 'hisat2's can share

 Other:
  --qc-filter        filter out reads that are bad according to QSEQ filter
  --seed <int>       seed for random number generator (0)
  --non-deterministic seed rand. gen. arbitrarily instead of using read attributes
  --remove-chrname   remove 'chr' from reference names in alignment
  --add-chrname      add 'chr' to reference names in alignment
  --version          print version information and quit
  -h/--help          print this usage message
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_hisat2_build_params(self, c=False, large_index=False, noauto=False, p="threads", bmax=False,
                                bmaxdivn="4", dcv="1024", nodc=False, noref=False, justref=False,
                                offrate="5", ftabchars="10", localoffrate="3", localftabchars="6",
                                snp=False, haplotype=False, ss=False, exon=False, seed=False, quiet=True):
        """HISAT2 version 2.1.0 by Daehwan Kim (infphilo@gmail.com, http://www.ccb.jhu.edu/people/infphilo)
Usage: hisat2-build [options]* <reference_in> <ht2_index_base>
    reference_in            comma-separated list of files with ref sequences
    hisat2_index_base       write ht2 data to files with this dir/basename
Options:
    -c                      reference sequences given on cmd line (as
                            <reference_in>)
    --large-index           force generated index to be 'large', even if ref
                            has fewer than 4 billion nucleotides
    -a/--noauto             disable automatic -p/--bmax/--dcv memory-fitting
    -p                      number of threads
    --bmax <int>            max bucket sz for blockwise suffix-array builder
    --bmaxdivn <int>        max bucket sz as divisor of ref len (default: 4)
    --dcv <int>             diff-cover period for blockwise (default: 1024)
    --nodc                  disable diff-cover (algorithm becomes quadratic)
    -r/--noref              don't build .3/.4.ht2 (packed reference) portion
    -3/--justref            just build .3/.4.ht2 (packed reference) portion
    -o/--offrate <int>      SA is sampled every 2^offRate BWT chars (default: 5)
    -t/--ftabchars <int>    # of chars consumed in initial lookup (default: 10)
    --localoffrate <int>    SA (local) is sampled every 2^offRate BWT chars (default: 3)
    --localftabchars <int>  # of chars consumed in initial lookup in a local index (default: 6)
    --snp <path>            SNP file name
    --haplotype <path>      haplotype file name
    --ss <path>             Splice site file name
    --exon <path>           Exon file name
    --seed <int>            seed for random number generator
    -q/--quiet              verbose output (for debugging)
    -h/--help               print detailed description of tool and its options
    --usage                 print this usage message
    --version               print version information and quit"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_hisat2_inspect_params(self, large_index=False, across="60", summary=False, names=False,
                                  snp=False, ss=False, ss_all=False, exon=False, ht2_ref=False):
        """
        HISAT2 version 2.1.0 by Daehwan Kim (infphilo@gmail.com, http://www.ccb.jhu.edu/people/infphilo)
Usage: hisat2-inspect [options]* <ht2_base>
  <ht2_base>         ht2 filename minus trailing .1.ht2/.2.ht2

  By default, prints FASTA records of the indexed nucleotide sequences to
  standard out.  With -n, just prints names.  With -s, just prints a summary of
  the index parameters and sequences.  With -e, preserves colors if applicable.

Options:
  --large-index      force inspection of the 'large' index, even if a
                     'small' one is present.
  -a/--across <int>  Number of characters across in FASTA output (default: 60)
  -s/--summary       Print summary incl. ref names, lengths, index properties
  -n/--names         Print reference sequence names only
  --snp              Print SNPs
  --ss               Print splice sites
  --ss-all           Print splice sites including those not in the global index
  --exon             Print exons
  -e/--ht2-ref       Reconstruct reference from .ht2 (slow, preserves colors)
  -v/--verbose       Verbose output (for debugging)
  -h/--help          print detailed description of tool and its options
  --help             print this usage message"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, paired_io, ref_io, unpaired_io, subcmd="hisat2"):
        """
        :param paired_io: sample_io object with paired end fastq files
        :param ref_io: sample_io object with reference
        :param unpaired_io: sample_io object with unpaired fastq files
        :param subcmd: hisat2 or hisat2-build or hisat2-inspect
        :return:
        """
        if subcmd == "hisat2":
            self.output_type = "sam"
            if paired_io:
                out = paired_io.id + ".sam"
                self.input_allowed = ["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz"]
                input = ["-1", paired_io.files[0].name, "-2", paired_io.files[1].name]
                if unpaired_io is not None:  # and unpaired_io.io_type == "fastq-pe" or "fastq-pe-gz":
                    input += ["-U", ",".join([f.name for f in unpaired_io.files])]

            elif unpaired_io and unpaired_io.io_type == "fastq-se" or "fastq-se-gz":
                out = unpaired_io.id + ".sam"
                input = ["-U", ",".join([f.name for f in unpaired_io.files])]
            else:
                raise IOError

            self.cmd = [subcmd] + self.get_opt_params("hisat2_params") + \
                       ["-x", self.index_prefix] + input + ["-S", out]

        elif subcmd == "hisat2-build":
            self.output_type = "bt2"
            self.input_allowed = ["fasta-se"]
            self.sample_dir = os.path.join(config.work_dir, ref_io.host_dir)
            self.index_path = self.out_dir
            self.index_prefix = os.path.splitext(os.path.basename(ref_io.files[0].name))[0]
            self.cmd = [subcmd] + self.get_opt_params("hisat2_build_params") + \
                       [",".join([f.name for f in ref_io.files]), self.index_prefix]

        elif subcmd == "hisat2-inspect":
            self.input_allowed = ["bt2"]
            self.cmd = [subcmd] + self.get_opt_params("hisat2_inspect_params") + [self.index_prefix]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, paired_io, ref_io, unpaired_io, subcmd="hisat2"):
        pass


