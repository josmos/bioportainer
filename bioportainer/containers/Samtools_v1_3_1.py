import os

from bioportainer.MultiCmdContainer import MultiCmdContainer

from bioportainer.Config import config


class Samtools_v1_3_1(MultiCmdContainer):
    # TODO: impelment idxstats, flagstats, stats, bedcov, depth, merge, faidx, tview, split, quickcheck, dict, fixmate, mpileupm, flags, fastq/a, collate, reheader, cat, rmdup, addreplacerg, calmd, targetcut, phase, depad,
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_view_params()
        self.set_sort_params()
        self.set_index_params()
        self.set_faidx_params()
        self.set_mpileup_params()

    def get_opt_params(self, param_attr):
        """
        return optional parameter dictionary as parameter-string-list
        :param param_attr: string: "get_<sub command>_params"
        :return: list of strings
        """
        p = getattr(self, param_attr)
        l = []
        for k, v in p.items():
            if k == "REGIONS":
                self.regions = [string for string in v]
            if k == "threads":
                k = "@"
            if v == "threads":
                v = str(config.container_threads)
            if k.startswith("_"):
                k = k[1:]
            if type(v) == bool and v is True:
                l += ["-" + k]
            elif type(v) == bool and v is False:
                continue
            elif len(k) == 1:
                l += ["-" + k, v]
            else:
                if k != "REGIONS":
                    k = k.replace("_", "-")
                    l += ["--" + k, v]

        return l

    @MultiCmdContainer.impl_set_opt_params
    def set_mpileup_params(self, _6=False, A=False, b=False, B=False, C=False, d=False, E=False,
                           f=False, G=False, l=False, q=False, Q=False, r=False, R=False, rf=False,
                           ff=False, x=False, g=False, v=False, O=False, s=False, t=False, u=False,
                           e=False, F=False, h=False, I=False, L=False, m=False, o=False, p=False,
                           P=False):
        """Usage: samtools mpileup [options] in1.bam [in2.bam [...]]

Input options:
  -6, --illumina1.3+      quality is in the Illumina-1.3+ encoding
  -A, --count-orphans     do not discard anomalous read pairs
  -b, --bam-list FILE     list of input BAM filenames, one per line
  -B, --no-BAQ            disable BAQ (per-Base Alignment Quality)
  -C, --adjust-MQ INT     adjust mapping quality; recommended:50, disable:0 [0]
  -d, --max-depth INT     max per-file depth; avoids excessive memory usage [250]
  -E, --redo-BAQ          recalculate BAQ on the fly, ignore existing BQs
  -f, --fasta-ref FILE    faidx indexed reference sequence file
  -G, --exclude-RG FILE   exclude read groups listed in FILE
  -l, --positions FILE    skip unlisted positions (chr pos) or regions (BED)
  -q, --min-MQ INT        skip alignments with mapQ smaller than INT [0]
  -Q, --min-BQ INT        skip bases with baseQ/BAQ smaller than INT [13]
  -r, --region REG        region in which pileup is generated
  -R, --ignore-RG         ignore RG tags (one BAM = one sample)
  --rf, --incl-flags STR|INT  required flags: skip reads with mask bits unset []
  --ff, --excl-flags STR|INT  filter flags: skip reads with mask bits set
                                            [UNMAP,SECONDARY,QCFAIL,DUP]
  -x, --ignore-overlaps   disable read-pair overlap detection

Output options:
  -o, --output FILE       write output to FILE [standard output]
  -g, --BCF               generate genotype likelihoods in BCF format
  -v, --VCF               generate genotype likelihoods in VCF format

Output options for mpileup format (without -g/-v):
  -O, --output-BP         output base positions on reads
  -s, --output-MQ         output mapping quality

Output options for genotype likelihoods (when -g/-v is used):
  -t, --output-tags LIST  optional tags to output:
               DP,AD,ADF,ADR,SP,INFO/AD,INFO/ADF,INFO/ADR []
  -u, --uncompressed      generate uncompressed VCF/BCF output

SNP/INDEL genotype likelihoods options (effective with -g/-v):
  -e, --ext-prob INT      Phred-scaled gap extension seq error probability [20]
  -F, --gap-frac FLOAT    minimum fraction of gapped reads [0.002]
  -h, --tandem-qual INT   coefficient for homopolymer errors [100]
  -I, --skip-indels       do not perform indel calling
  -L, --max-idepth INT    maximum per-file depth for INDEL calling [250]
  -m, --min-ireads INT    minimum number gapped reads for indel candidates [1]
  -o, --open-prob INT     Phred-scaled gap open seq error probability [40]
  -p, --per-sample-mF     apply -m and -F per-sample for increased sensitivity
  -P, --platforms STR     comma separated list of platforms for indels [all]
      --input-fmt-option OPT[=VAL]
               Specify a single input file format option in the form
               of OPTION or OPTION=VALUE
      --reference FILE
               Reference sequence FASTA FILE [null]

Notes: Assuming diploid individuals.
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_view_params(self, threads="threads", b=False, _1=False, C=False,
                        u=False, h=False, H=False,c=False,U=False, t=False, T=False, r=False, q="0",
                        l=False, m="0", f="0", F="0", x=False, B=False, s="0", REGIONS=()):
        """Usage: samtools view [options] <in.bam>|<in.sam>|<in.cram> [region ...]

Options:
  -b       output BAM
  -C       output CRAM (requires -T)
  -1       use fast BAM compression (implies -b)
  -u       uncompressed BAM output (implies -b)
  -h       include header in SAM output
  -H       print SAM header only (no alignments)
  -c       print only the count of matching records
  -o FILE  output file name [stdout]
  -U FILE  output reads not selected by filters to FILE [null]
  -t FILE  FILE listing reference names and lengths (see long help) [null]
  -L FILE  only include reads overlapping this BED FILE [null]
  -r STR   only include reads in read group STR [null]
  -R FILE  only include reads with read group listed in FILE [null]
  -q INT   only include reads with mapping quality >= INT [0]
  -l STR   only include reads in library STR [null]
  -m INT   only include reads with number of CIGAR operations consuming
           query sequence >= INT [0]
  -f INT   only include reads with all bits set in INT set in FLAG [0]
  -F INT   only include reads with none of the bits set in INT set in FLAG [0]
  -x STR   read tag to strip (repeatable) [null]
  -B       collapse the backward CIGAR operation
  -s FLOAT integer part sets seed of random number generator [0];
           rest sets fraction of templates to subsample [no subsampling]
  -@, --threads INT
           number of BAM/CRAM compression threads [0]
  -?       print long help, including note about region specification
  -S       ignored (input format is auto-detected)
      --input-fmt-option OPT[=VAL]
               Specify a single input file format option in the form
               of OPTION or OPTION=VALUE
  -O, --output-fmt FORMAT[,OPT[=VAL]]...
               Specify output format (SAM, BAM, CRAM)
      --output-fmt-option OPT[=VAL]
               Specify a single output file format option in the form
               of OPTION or OPTION=VALUE
  -T, --reference FILE
               Reference sequence FASTA FILE [null]"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_sort_params(self, l="9", m="768M", n=False, O=False, threads="threads"):
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_index_params(self, b=True, c=False, m=False):
        return self

    def set_faidx_params(self):
        """Usage:   samtools faidx <file.fa|file.fa.gz> [<reg> [...]]"""
        return self


    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="view", mount=None):
        """
        Version: 1.3.1 (using htslib 1.3.1)

Usage:   samtools <command> [options]

Commands:
  -- Indexing
     dict           create a sequence dictionary file
     faidx          index/extract FASTA
     index          index alignment

  -- Editing
     calmd          recalculate MD/NM tags and '=' bases
     fixmate        fix mate information
     reheader       replace BAM header
     rmdup          remove PCR duplicates
     targetcut      cut fosmid regions (for fosmid pool only)
     addreplacerg   adds or replaces RG tags

  -- File operations
     collate        shuffle and group alignments by name
     cat            concatenate BAMs
     merge          merge sorted alignments
     mpileup        multi-way pileup
     sort           sort alignment file
     split          splits a file by read group
     quickcheck     quickly check if SAM/BAM/CRAM file appears intact
     fastq          converts a BAM to a FASTQ
     fasta          converts a BAM to a FASTA

  -- Statistics
     bedcov         read depth per BED region
     depth          compute the depth
     flagstat       simple stats
     idxstats       BAM index stats
     phase          phase heterozygotes
     stats          generate stats (former bamcheck)

  -- Viewing
     flags          explain BAM flags
     tview          text alignment viewer
     view           SAM<->BAM<->CRAM conversion
     depad          convert padded BAM to unpadded BAM

        """
        if subcmd == "view":
            if self.view_params["b"]:
                self.output_type = "bam"
            elif self.view_params["C"]:
                self.output_type = "cram"
            else:
                self.output_type = "sam"
            if self.view_params["U"]:
                self.view_params["U"] = sample_io.id + "_U." + self.output_type
            out = os.path.splitext(sample_io.files[0].name)[0] + "_view." + self.output_type
            self.output_filter = ".*_view." + self.output_type
            self.cmd = ["samtools", subcmd] + self.get_opt_params("view_params") + \
                       ["-o", out, sample_io.files[0].name] + self.regions

        if subcmd == "index":
            self.output_type = "bai"
            self.cmd = ["samtools", subcmd] + self.get_opt_params("index_params") + \
                       [sample_io.files[0].name]

        if subcmd == "faidx":
            self.output_type = "fai"
            self.cmd = ["samtools", subcmd] + [f.name for f in sample_io.files]

        if subcmd == "sort":
            out = os.path.splitext(sample_io.files[0].name)[0] + "_sorted." + self.output_type
            self.output_filter = ".*_sorted." + self.output_type
            self.cmd = ["samtools", subcmd] + self.get_opt_params("sort_params") + \
                       ["-o", out, sample_io.files[0].name]

        if subcmd == "mpileup":
            self.output_filter = None
            if self.mpileup_params["g"]:
                self.output_type = "bcf"
            elif self.mpileup_params["v"]:
                self.output_type = "vcf"
            else:
                self.output_type = "mpi"
            out = os.path.splitext(sample_io.files[0].name)[0] + "_mpileup." + self.output_type
            self.cmd = ["samtools", subcmd] + self.get_opt_params("mpileup_params") + \
                       ["-o", out, sample_io.files[0].name]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="view", mount=None):
        pass


