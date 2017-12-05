from bioportainer.MultiCmdContainer import MultiCmdContainer


class Bcf_tools_v1_3_1(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_annotate_params()
        self.set_call_params()
        self.set_cnv_params()
        self.set_concat_params()
        self.set_consensus_params()
        self.set_convert_params()
        self.set_filter_params()
        self.set_gtcheck_params()
        self.set_index_params()
        self.set_merge_params()
        self.set_norm_params()
        self.set_plugin_params()
        self.set_query_params()
        self.set_reheader_params()
        self.set_view_params()
        self.set_roh_params()
        self.set_stats_params()
        self.set_plot_vcfstats_params()

    @MultiCmdContainer.impl_set_opt_params
    def set_annotate_params(self, a=False, c=False, e=False, h=False, I=False, i=False, m=False,
                            O=False, r=False, R=False, s=False, S=False, x=False):
        """About:   Annotate and edit VCF/BCF files.
Usage:   bcftools annotate [options] <in.vcf.gz>

Options:
   -a, --annotations <file>       VCF file or tabix-indexed file with annotations: CHR\tPOS[\tVALUE]+
   -c, --columns <list>           list of columns in the annotation file, e.g. CHROM,POS,REF,ALT,-,INFO/TAG. See man page for details
   -e, --exclude <expr>           exclude sites for which the expression is true (see man page for details)
   -h, --header-lines <file>      lines which should be appended to the VCF header
   -I, --set-id [+]<format>       set ID column, see man page for details
   -i, --include <expr>           select sites for which the expression is true (see man page for details)
   -m, --mark-sites [+-]<tag>     add INFO/tag flag to sites which are ("+") or are not ("-") listed in the -a file
       --no-version               do not append version and command line to the header
   -o, --output <file>            write output to a file [standard output]
   -O, --output-type <b|u|z|v>    b: compressed BCF, u: uncompressed BCF, z: compressed VCF, v: uncompressed VCF [v]
   -r, --regions <region>         restrict to comma-separated list of regions
   -R, --regions-file <file>      restrict to regions listed in a file
       --rename-chrs <file>       rename sequences according to map file: from\tto
   -s, --samples [^]<list>        comma separated list of samples to annotate (or exclude with "^" prefix)
   -S, --samples-file [^]<file>   file of samples to annotate (or exclude with "^" prefix)
   -x, --remove <list>            list of annotations to remove (e.g. ID,INFO/DP,FORMAT/DP,FILTER). See man page for details
       --threads <int>            number of extra output compression threads [0]
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_call_params(self, O=False, r=False, R=False, s=False, S=False, t=False, T=False, A=False,
                        f=False, g=False, i=False, M=False, V=False, v=False, c=False, C=False,
                        m=False, n=False, p=False, P=False):
        """About:   SNP/indel variant calling from VCF/BCF. To be used in conjunction with samtools mpileup.
         This command replaces the former "bcftools view" caller. Some of the original
         functionality has been temporarily lost in the process of transition to htslib,
         but will be added back on popular demand. The original calling model can be
         invoked with the -c option.
Usage:   bcftools call [options] <in.vcf.gz>

File format options:
       --no-version                do not append version and command line to the header
   -o, --output <file>             write output to a file [standard output]
   -O, --output-type <b|u|z|v>     output type: 'b' compressed BCF; 'u' uncompressed BCF; 'z' compressed VCF; 'v' uncompressed VCF [v]
       --ploidy <assembly>[?]      predefined ploidy, 'list' to print available settings, append '?' for details
       --ploidy-file <file>        space/tab-delimited list of CHROM,FROM,TO,SEX,PLOIDY
   -r, --regions <region>          restrict to comma-separated list of regions
   -R, --regions-file <file>       restrict to regions listed in a file
   -s, --samples <list>            list of samples to include [all samples]
   -S, --samples-file <file>       PED file or a file with an optional column with sex (see man page for details) [all samples]
   -t, --targets <region>          similar to -r but streams rather than index-jumps
   -T, --targets-file <file>       similar to -R but streams rather than index-jumps
       --threads <int>             number of extra output compression threads [0]

Input/output options:
   -A, --keep-alts                 keep all possible alternate alleles at variant sites
   -f, --format-fields <list>      output format fields: GQ,GP (lowercase allowed) []
   -g, --gvcf <int>,[...]          group non-variant sites into gVCF blocks by minimum per-sample DP
   -i, --insert-missed             output also sites missed by mpileup but present in -T
   -M, --keep-masked-ref           keep sites with masked reference allele (REF=N)
   -V, --skip-variants <type>      skip indels/snps
   -v, --variants-only             output variant sites only

Consensus/variant calling options:
   -c, --consensus-caller          the original calling method (conflicts with -m)
   -C, --constrain <str>           one of: alleles, trio (see manual)
   -m, --multiallelic-caller       alternative model for multiallelic and rare-variant calling (conflicts with -c)
   -n, --novel-rate <float>,[...]  likelihood of novel mutation for constrained trio calling, see man page for details [1e-8,1e-9,1e-9]
   -p, --pval-threshold <float>    variant if P(ref|D)<FLOAT with -c [0.5]
   -P, --prior <float>             mutation rate (use bigger for greater sensitivity) [1.1e-3]"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_cnv_params(self, c=False, f=False, o=False, p=False, r=False, R=False, s=False, t=False,
                       T=False, a=False, b=False, d=False, e=False, k=False, l=False, L=False,
                       O=False, P=False, x=False):
        """About:   Copy number variation caller, requires Illumina's B-allele frequency (BAF) and Log R
         Ratio intensity (LRR). The HMM considers the following copy number states: CN 2
         (normal), 1 (single-copy loss), 0 (complete loss), 3 (single-copy gain)
Usage:   bcftools cnv [OPTIONS] <file.vcf>
General Options:
    -c, --control-sample <string>      optional control sample name to highlight differences
    -f, --AF-file <file>               read allele frequencies from file (CHR\tPOS\tREF,ALT\tAF)
    -o, --output-dir <path>
    -p, --plot-threshold <float>       plot aberrant chromosomes with quality at least 'float'
    -r, --regions <region>             restrict to comma-separated list of regions
    -R, --regions-file <file>          restrict to regions listed in a file
    -s, --query-sample <string>        query samply name
    -t, --targets <region>             similar to -r but streams rather than index-jumps
    -T, --targets-file <file>          similar to -R but streams rather than index-jumps
HMM Options:
    -a, --aberrant <float[,float]>     fraction of aberrant cells in query and control [1.0,1.0]
    -b, --BAF-weight <float>           relative contribution from BAF [1]
    -d, --BAF-dev <float[,float]>      expected BAF deviation in query and control [0.04,0.04]
    -e, --err-prob <float>             uniform error probability [1e-4]
    -k, --LRR-dev <float[,float]>      expected LRR deviation [0.2,0.2]
    -l, --LRR-weight <float>           relative contribution from LRR [0.2]
    -L, --LRR-smooth-win <int>         window of LRR moving average smoothing [10]
    -O, --optimize <float>             estimate fraction of aberrant cells down to <float> [1.0]
    -P, --same-prob <float>            prior probability of -s/-c being the same [0.5]
    -x, --xy-prob <float>              P(x|y) transition probability [1e-9]"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_concat_params(self, a=False, c=False, d=False, D=False, f=False, l=False, n=False,
                          O=False, q=False, r=False, R=False, threads="threads"):
        """About:   Concatenate or combine VCF/BCF files. All source files must have the same sample
         columns appearing in the same order. The program can be used, for example, to
         concatenate chromosome VCFs into one VCF, or combine a SNP VCF and an indel
         VCF into one. The input files must be sorted by chr and position. The files
         must be given in the correct order to produce sorted VCF on output unless
         the -a, --allow-overlaps option is specified. With the --naive option, the files
         are concatenated without being recompressed, which is very fast but dangerous
         if the BCF headers differ.
Usage:   bcftools concat [options] <A.vcf.gz> [<B.vcf.gz> [...]]

Options:
   -a, --allow-overlaps           First coordinate of the next file can precede last record of the current file.
   -c, --compact-PS               Do not output PS tag at each site, only at the start of a new phase set block.
   -d, --rm-dups <string>         Output duplicate records present in multiple files only once: <snps|indels|both|all|none>
   -D, --remove-duplicates        Alias for -d none
   -f, --file-list <file>         Read the list of files from a file.
   -l, --ligate                   Ligate phased VCFs by matching phase at overlapping haplotypes
       --no-version               do not append version and command line to the header
   -n, --naive                    Concatenate BCF files without recompression (dangerous, use with caution)
   -o, --output <file>            Write output to a file [standard output]
   -O, --output-type <b|u|z|v>    b: compressed BCF, u: uncompressed BCF, z: compressed VCF, v: uncompressed VCF [v]
   -q, --min-PQ <int>             Break phase set if phasing quality is lower than <int> [30]
   -r, --regions <region>         Restrict to comma-separated list of regions
   -R, --regions-file <file>      Restrict to regions listed in a file
       --threads <int>            Number of extra output compression threads [0]
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_consensus_params(self, f=False, H=False, i=False, m=False, o=False, c=False, s=False):
        """About:   Create consensus sequence by applying VCF variants to a reference
         fasta file.
Usage:   bcftools consensus [OPTIONS] <file.vcf>
Options:
    -f, --fasta-ref <file>     reference sequence in fasta format
    -H, --haplotype <1|2>      apply variants for the given haplotype
    -i, --iupac-codes          output variants in the form of IUPAC ambiguity codes
    -m, --mask <file>          replace regions with N
    -o, --output <file>        write output to a file [standard output]
    -c, --chain <file>         write a chain file for liftover
    -s, --sample <name>        apply variants of the given sample
Examples:
   # Get the consensus for one region. The fasta header lines are then expected
   # in the form ">chr:from-to".
   samtools faidx ref.fa 8:11870-11890 | bcftools consensus in.vcf.gz > out.fa
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_convert_params(self, e=False, i=False, r=False, R=False, s=False, S=False, t=False,
                           T=False, no_version=False, O=False, threads="threads", G=False, g=False,
                           tag=False, chrom=False, vcf_ids=False, gvcf2vcf=False, f=False,
                           hapsample2vcf=False, hapsample=False, haploid2diploid=False, H=False,
                           h=False, tsv2vcf=False, c=False):
        """About:   Converts VCF/BCF to other formats and back. See man page for file
         formats details. When specifying output files explicitly instead
         of with <prefix>, one can use '-' for stdout and '.' to suppress.
Usage:   bcftools convert [OPTIONS] <input_file>

VCF input options:
   -e, --exclude <expr>        exclude sites for which the expression is true
   -i, --include <expr>        select sites for which the expression is true
   -r, --regions <region>      restrict to comma-separated list of regions
   -R, --regions-file <file>   restrict to regions listed in a file
   -s, --samples <list>        list of samples to include
   -S, --samples-file <file>   file of samples to include
   -t, --targets <region>      similar to -r but streams rather than index-jumps
   -T, --targets-file <file>   similar to -R but streams rather than index-jumps

VCF output options:
       --no-version               do not append version and command line to the header
   -o, --output <file>            output file name [stdout]
   -O, --output-type <b|u|z|v>    b: compressed BCF, u: uncompressed BCF, z: compressed VCF, v: uncompressed VCF [v]
       --threads <int>            number of extra output compression threads [0]

GEN/SAMPLE conversion (input/output from IMPUTE2):
   -G, --gensample2vcf <...>   <prefix>|<gen-file>,<sample-file>
   -g, --gensample <...>       <prefix>|<gen-file>,<sample-file>
       --tag <string>          tag to take values for .gen file: GT,PL,GL,GP [GT]
       --chrom                 output chromosome in first column instead of CHROM:POS_REF_ALT
       --vcf-ids               output VCF IDs in second column instead of CHROM:POS_REF_ALT

gVCF conversion:
       --gvcf2vcf              expand gVCF reference blocks
   -f, --fasta-ref <file>      reference sequence in fasta format

HAP/SAMPLE conversion (output from SHAPEIT):
       --hapsample2vcf <...>   <prefix>|<haps-file>,<sample-file>
       --hapsample <...>       <prefix>|<haps-file>,<sample-file>
       --haploid2diploid       convert haploid genotypes to diploid homozygotes
       --vcf-ids               output VCF IDs instead of CHROM:POS_REF_ALT

HAP/LEGEND/SAMPLE conversion:
   -H, --haplegendsample2vcf <...>  <prefix>|<hap-file>,<legend-file>,<sample-file>
   -h, --haplegendsample <...>      <prefix>|<hap-file>,<legend-file>,<sample-file>
       --haploid2diploid            convert haploid genotypes to diploid homozygotes
       --vcf-ids                    output VCF IDs instead of CHROM:POS_REF_ALT

TSV conversion:
       --tsv2vcf <file>
   -c, --columns <string>      columns of the input tsv file [ID,CHROM,POS,AA]
   -f, --fasta-ref <file>      reference sequence in fasta format
   -s, --samples <list>        list of sample names
   -S, --samples-file <file>   file of sample names"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_filter_params(self, e=False, g=False, G=False, i=False, m=False, O=False, r=False,
                          R=False, s=False, S=False, t=False, T=False, threads="threads"):
        """About:   Apply fixed-threshold filters.
Usage:   bcftools filter [options] <in.vcf.gz>

Options:
    -e, --exclude <expr>          exclude sites for which the expression is true (see man page for details)
    -g, --SnpGap <int>            filter SNPs within <int> base pairs of an indel
    -G, --IndelGap <int>          filter clusters of indels separated by <int> or fewer base pairs allowing only one to pass
    -i, --include <expr>          include only sites for which the expression is true (see man page for details
    -m, --mode [+x]               "+": do not replace but add to existing FILTER; "x": reset filters at sites which pass
        --no-version              do not append version and command line to the header
    -o, --output <file>           write output to a file [standard output]
    -O, --output-type <b|u|z|v>   b: compressed BCF, u: uncompressed BCF, z: compressed VCF, v: uncompressed VCF [v]
    -r, --regions <region>        restrict to comma-separated list of regions
    -R, --regions-file <file>     restrict to regions listed in a file
    -s, --soft-filter <string>    annotate FILTER column with <string> or unique filter name ("Filter%d") made up by the program ("+")
    -S, --set-GTs <.|0>           set genotypes of failed samples to missing (.) or ref (0)
    -t, --targets <region>        similar to -r but streams rather than index-jumps
    -T, --targets-file <file>     similar to -R but streams rather than index-jumps
        --threads <int>           number of extra output compression threads [0]"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_gtcheck_params(self, a=False, g=False, G=False, H=False, p=False, r=False, R=False,
                           s=False, S=False, t=False, T=False):
        """About:   Check sample identity. With no -g BCF given, multi-sample cross-check is performed.
Usage:   bcftools gtcheck [options] [-g <genotypes.vcf.gz>] <query.vcf.gz>

Options:
    -a, --all-sites                 output comparison for all sites
    -g, --genotypes <file>          genotypes to compare against
    -G, --GTs-only <int>            use GTs, ignore PLs, using <int> for unseen genotypes [99]
    -H, --homs-only                 homozygous genotypes only (useful for low coverage data)
    -p, --plot <prefix>             plot
    -r, --regions <region>          restrict to comma-separated list of regions
    -R, --regions-file <file>       restrict to regions listed in a file
    -s, --query-sample <string>     query sample (by default the first sample is checked)
    -S, --target-sample <string>    target sample in the -g file (used only for plotting)
    -t, --targets <region>          similar to -r but streams rather than index-jumps
    -T, --targets-file <file>       similar to -R but streams rather than index-jumps"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_index_params(self, c=False, f=False, m=False, t=False, n=False, s=False):
        """About:   Index bgzip compressed VCF/BCF files for random access.
Usage:   bcftools index [options] <in.bcf>|<in.vcf.gz>

Indexing options:
    -c, --csi            generate CSI-format index for VCF/BCF files [default]
    -f, --force          overwrite index if it already exists
    -m, --min-shift INT  set minimal interval size for CSI indices to 2^INT [14]
    -t, --tbi            generate TBI-format index for VCF files

Stats options:
    -n, --nrecords       print number of records based on existing index file
    -s, --stats   print per contig stats based on existing index file
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_merge_params(self, force_samples=False, print_header=False, use_header=False, f=False,
                         i=False, l=False, O=False, r=False, R=False, threads="theads"):
        """About:   Merge multiple VCF/BCF files from non-overlapping sample sets to create one multi-sample file.
         Note that only records from different files can be merged, never from the same file. For
         "vertical" merge take a look at "bcftools norm" instead.
Usage:   bcftools merge [options] <A.vcf.gz> <B.vcf.gz> [...]

Options:
        --force-samples                resolve duplicate sample names
        --print-header                 print only the merged header and exit
        --use-header <file>            use the provided header
    -f, --apply-filters <list>         require at least one of the listed FILTER strings (e.g. "PASS,.")
    -i, --info-rules <tag:method,..>   rules for merging INFO fields (method is one of sum,avg,min,max,join) or "-" to turn off the default [DP:sum,DP4:sum]
    -l, --file-list <file>             read file names from the file
    -m, --merge <string>               allow multiallelic records for <snps|indels|both|all|none|id>, see man page for details [both]
        --no-version                   do not append version and command line to the header
    -o, --output <file>                write output to a file [standard output]
    -O, --output-type <b|u|z|v>        'b' compressed BCF; 'u' uncompressed BCF; 'z' compressed VCF; 'v' uncompressed VCF [v]
    -r, --regions <region>             restrict to comma-separated list of regions
    -R, --regions-file <file>          restrict to regions listed in a file
        --threads <int>                number of extra output compression threads [0]"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_norm_params(self, c=False, D=False, d=False, f=False, m=False, N=False, no_version=False,
                        O=False, r=False, R=False, s=False, t=False, T=False, w=False):
        """About:   Left-align and normalize indels; check if REF alleles match the reference;
         split multiallelic sites into multiple rows; recover multiallelics from
         multiple rows.
Usage:   bcftools norm [options] <in.vcf.gz>

Options:
    -c, --check-ref <e|w|x|s>         check REF alleles and exit (e), warn (w), exclude (x), or set (s) bad sites [e]
    -D, --remove-duplicates           remove duplicate lines of the same type.
    -d, --rm-dup <type>               remove duplicate snps|indels|both|any
    -f, --fasta-ref <file>            reference sequence
    -m, --multiallelics <-|+>[type]   split multiallelics (-) or join biallelics (+), type: snps|indels|both|any [both]
        --no-version                  do not append version and command line to the header
    -N, --do-not-normalize            do not normalize indels (with -m or -c s)
    -o, --output <file>               write output to a file [standard output]
    -O, --output-type <type>          'b' compressed BCF; 'u' uncompressed BCF; 'z' compressed VCF; 'v' uncompressed VCF [v]
    -r, --regions <region>            restrict to comma-separated list of regions
    -R, --regions-file <file>         restrict to regions listed in a file
    -s, --strict-filter               when merging (-m+), merged site is PASS only if all sites being merged PASS
    -t, --targets <region>            similar to -r but streams rather than index-jumps
    -T, --targets-file <file>         similar to -R but streams rather than index-jumps
        --threads <int>               number of extra output compression threads [0]
    -w, --site-win <int>              buffer for sorting lines which changed position during realignment [1000]"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_plugin_params(self, e=False, i=False, r=False, R=False, t=False, T=False, no_version=False,
                          O=False, threads="threads"):
        """About:   Run user defined plugin
Usage:   bcftools plugin <name> [OPTIONS] <file> [-- PLUGIN_OPTIONS]
         bcftools +name [OPTIONS] <file>  [-- PLUGIN_OPTIONS]

VCF input options:
   -e, --exclude <expr>        exclude sites for which the expression is true
   -i, --include <expr>        select sites for which the expression is true
   -r, --regions <region>      restrict to comma-separated list of regions
   -R, --regions-file <file>   restrict to regions listed in a file
   -t, --targets <region>      similar to -r but streams rather than index-jumps
   -T, --targets-file <file>   similar to -R but streams rather than index-jumps
VCF output options:
       --no-version            do not append version and command line to the header
   -o, --output <file>         write output to a file [standard output]
   -O, --output-type <type>    'b' compressed BCF; 'u' uncompressed BCF; 'z' compressed VCF; 'v' uncompressed VCF [v]
       --threads <int>         number of extra output compression threads [0]
Plugin options:
   -h, --help                  list plugin's options
   -l, --list-plugins          list available plugins. See BCFTOOLS_PLUGINS environment variable and man page for details
   -v, --verbose               print debugging information on plugin failure
   -V, --version               print version string and exit"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_query_params(self, c=False, e=False, f=False, H=False, i=False, l=False, r=False,
                         R=False, s=False, S=False, t=False, T=False, u=False, v=False):
        """About:   Extracts fields from VCF/BCF file and prints them in user-defined format
Usage:   bcftools query [options] <A.vcf.gz> [<B.vcf.gz> [...]]

Options:
    -c, --collapse <string>           collapse lines with duplicate positions for <snps|indels|both|all|some|none>, see man page [none]
    -e, --exclude <expr>              exclude sites for which the expression is true (see man page for details)
    -f, --format <string>             see man page for details
    -H, --print-header                print header
    -i, --include <expr>              select sites for which the expression is true (see man page for details)
    -l, --list-samples                print the list of samples and exit
    -o, --output-file <file>          output file name [stdout]
    -r, --regions <region>            restrict to comma-separated list of regions
    -R, --regions-file <file>         restrict to regions listed in a file
    -s, --samples <list>              list of samples to include
    -S, --samples-file <file>         file of samples to include
    -t, --targets <region>            similar to -r but streams rather than index-jumps
    -T, --targets-file <file>         similar to -R but streams rather than index-jumps
    -u, --allow-undef-tags            print "." for undefined tags
    -v, --vcf-list <file>             process multiple VCFs listed in the file

Examples:
	bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%SAMPLE=%GT]\n' file.vcf.gz"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_reheader_params(self, h=False, s=False):
        """About:   Modify header of VCF/BCF files, change sample names.
Usage:   bcftools reheader [OPTIONS] <in.vcf.gz>

Options:
    -h, --header <file>     new header
    -o, --output <file>     write output to a file [standard output]
    -s, --samples <file>    new sample names"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_view_params(self, G=False, header_only=False, no_header=False, l=False, no_version=False,
                        O=False, r=False, R=False, t=False, T=False, a=False, I=False, s=False,
                        S=False, c=False, f=False, g=False, i=False, e=False, k=False, n=False,
                        m=False, M=False, p=False, P=False, q=False, Q=False, u=False, U=False,
                        v=False, V=False, x=False, X=False):
        """About:   VCF/BCF conversion, view, subset and filter VCF/BCF files.
Usage:   bcftools view [options] <in.vcf.gz> [region1 [...]]

Output options:
    -G,   --drop-genotypes              drop individual genotype information (after subsetting if -s option set)
    -h/H, --header-only/--no-header     print the header only/suppress the header in VCF output
    -l,   --compression-level [0-9]     compression level: 0 uncompressed, 1 best speed, 9 best compression [-1]
          --no-version                  do not append version and command line to the header
    -o,   --output-file <file>          output file name [stdout]
    -O,   --output-type <b|u|z|v>       b: compressed BCF, u: uncompressed BCF, z: compressed VCF, v: uncompressed VCF [v]
    -r, --regions <region>              restrict to comma-separated list of regions
    -R, --regions-file <file>           restrict to regions listed in a file
    -t, --targets [^]<region>           similar to -r but streams rather than index-jumps. Exclude regions with "^" prefix
    -T, --targets-file [^]<file>        similar to -R but streams rather than index-jumps. Exclude regions with "^" prefix
        --threads <int>                 number of extra output compression threads [0]

Subset options:
    -a, --trim-alt-alleles        trim alternate alleles not seen in the subset
    -I, --no-update               do not (re)calculate INFO fields for the subset (currently INFO/AC and INFO/AN)
    -s, --samples [^]<list>       comma separated list of samples to include (or exclude with "^" prefix)
    -S, --samples-file [^]<file>  file of samples to include (or exclude with "^" prefix)
        --force-samples           only warn about unknown subset samples

Filter options:
    -c/C, --min-ac/--max-ac <int>[:<type>]      minimum/maximum count for non-reference (nref), 1st alternate (alt1), least frequent
                                                   (minor), most frequent (major) or sum of all but most frequent (nonmajor) alleles [nref]
    -f,   --apply-filters <list>                require at least one of the listed FILTER strings (e.g. "PASS,.")
    -g,   --genotype [^]<hom|het|miss>          require one or more hom/het/missing genotype or, if prefixed with "^", exclude sites with hom/het/missing genotypes
    -i/e, --include/--exclude <expr>            select/exclude sites for which the expression is true (see man page for details)
    -k/n, --known/--novel                       select known/novel sites only (ID is not/is '.')
    -m/M, --min-alleles/--max-alleles <int>     minimum/maximum number of alleles listed in REF and ALT (e.g. -m2 -M2 for biallelic sites)
    -p/P, --phased/--exclude-phased             select/exclude sites where all samples are phased
    -q/Q, --min-af/--max-af <float>[:<type>]    minimum/maximum frequency for non-reference (nref), 1st alternate (alt1), least frequent
                                                   (minor), most frequent (major) or sum of all but most frequent (nonmajor) alleles [nref]
    -u/U, --uncalled/--exclude-uncalled         select/exclude sites without a called genotype
    -v/V, --types/--exclude-types <list>        select/exclude comma-separated list of variant types: snps,indels,mnps,other [null]
    -x/X, --private/--exclude-private           select/exclude sites where the non-reference alleles are exclusive (private) to the subset samples"""

        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_roh_params(self,AF_dflt=False, AF_tag=False, AF_file=False, e=False, G=False, I=False,
                       m=False, M=False, r=False, R=False, s=False, t=False, T=False, a=False,
                       H=False, V=False):
        """About:   HMM model for detecting runs of autozygosity.
Usage:   bcftools roh [options] <in.vcf.gz>

General Options:
        --AF-dflt <float>              if AF is not known, use this allele frequency [skip]
        --AF-tag <TAG>                 use TAG for allele frequency
        --AF-file <file>               read allele frequencies from file (CHR\tPOS\tREF,ALT\tAF)
    -e, --estimate-AF <file>           calculate AC,AN counts on the fly, using either all samples ("-") or samples listed in <file>
    -G, --GTs-only <float>             use GTs, ignore PLs, use <float> for PL of unseen genotypes. Safe value to use is 30 to account for GT errors.
    -I, --skip-indels                  skip indels as their genotypes are enriched for errors
    -m, --genetic-map <file>           genetic map in IMPUTE2 format, single file or mask, where string "{CHROM}" is replaced with chromosome name
    -M, --rec-rate <float>             constant recombination rate per bp
    -r, --regions <region>             restrict to comma-separated list of regions
    -R, --regions-file <file>          restrict to regions listed in a file
    -s, --sample <sample>              sample to analyze
    -t, --targets <region>             similar to -r but streams rather than index-jumps
    -T, --targets-file <file>          similar to -R but streams rather than index-jumps

HMM Options:
    -a, --hw-to-az <float>             P(AZ|HW) transition probability from HW (Hardy-Weinberg) to AZ (autozygous) state [6.7e-8]
    -H, --az-to-hw <float>             P(HW|AZ) transition probability from AZ to HW state [5e-9]
    -V, --viterbi-training             perform Viterbi training to estimate transition probabilities"""

        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_stats_params(self, _1=False, c=False, d=False, e=False, E=False, f=False, F=False,
                         i=False, I=False, r=False, R=False, s=False, S=False, t=False, T=False,
                         u=False, v=False):
        """About:   Parses VCF or BCF and produces stats which can be plotted using plot-vcfstats.
         When two files are given, the program generates separate stats for intersection
         and the complements. By default only sites are compared, -s/-S must given to include
         also sample columns.
Usage:   bcftools stats [options] <A.vcf.gz> [<B.vcf.gz>]

Options:
    -1, --1st-allele-only              include only 1st allele at multiallelic sites
    -c, --collapse <string>            treat as identical records with <snps|indels|both|all|some|none>, see man page for details [none]
    -d, --depth <int,int,int>          depth distribution: min,max,bin size [0,500,1]
    -e, --exclude <expr>               exclude sites for which the expression is true (see man page for details)
    -E, --exons <file.gz>              tab-delimited file with exons for indel frameshifts (chr,from,to; 1-based, inclusive, bgzip compressed)
    -f, --apply-filters <list>         require at least one of the listed FILTER strings (e.g. "PASS,.")
    -F, --fasta-ref <file>             faidx indexed reference sequence file to determine INDEL context
    -i, --include <expr>               select sites for which the expression is true (see man page for details)
    -I, --split-by-ID                  collect stats for sites with ID separately (known vs novel)
    -r, --regions <region>             restrict to comma-separated list of regions
    -R, --regions-file <file>          restrict to regions listed in a file
    -s, --samples <list>               list of samples for sample stats, "-" to include all samples
    -S, --samples-file <file>          file of samples to include
    -t, --targets <region>             similar to -r but streams rather than index-jumps
    -T, --targets-file <file>          similar to -R but streams rather than index-jumps
    -u, --user-tstv <TAG[:min:max:n]>  collect Ts/Tv stats for any tag using the given binning [0:1:100]
    -v, --verbose                      produce verbose per-site and per-sample output"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_plot_vcfstats_params(self, m=False, p=False, P=False, r=False, s=False, t=False, T=False):
        """Usage: plot-vcfstats [OPTIONS] file.chk ...
       plot-vcfstats -p outdir/ file.chk ...
Options:
   -m, --merge                         Merge vcfstats files to STDOUT, skip plotting.
   -p, --prefix <path>                 The output files prefix, add a slash to create new directory.
   -P, --no-PDF                        Skip the PDF creation step.
   -r, --rasterize                     Rasterize PDF images for fast rendering.
   -s, --sample-names                  Use sample names for xticks rather than numeric IDs.
   -t, --title <string>                Identify files by these titles in plots. Can be given multiple times.
   -T, --main-title <string>           Main title for the PDF.
   -h, -?, --help                      This help message."""
        return self

    def get_output_type(self, subcmd, prefix):
        p = getattr(self, subcmd + "_params")
        l = []
        for k, v in p.items():
            if k == "O":
                if v == "u":
                    self.set_output_type("bcf-bz")
                    l = ["-o", prefix + ".bcf.bz"]
                if v == "b":
                    self.set_output_type("bcf")
                    l = ["-o", prefix + ".bcf"]
                if v == "z":
                    self.set_output_type("vcf-bz")
                    l = ["-o", prefix + ".vcf.bz"]
                if v == "v":
                    self.set_output_type("vcf")
                    l = ["-o", prefix + ".vcf"]

        if l == []:
            l = ["-O", "z", "-o", prefix + ".vcf.bz"]

        return l

    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="annotate", output_postfix=""):
        out = sample_io.id + output_postfix
        if subcmd == "annotate":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("annotate_params") \
                       + self.get_output_type(subcmd, out) + [sample_io.files[0].name]

        if subcmd == "call":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("call_params") \
                       + self.get_output_type(subcmd, out) + [sample_io.files[0].name]

        if subcmd == "cnv":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("cnv_params") + [sample_io.files[0].name, ">", out + ".out"]

        if subcmd == "concat":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("concat_params") \
                       + self.get_output_type(subcmd, out) + [sample_io.files[0].name]

        if subcmd == "consensus":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("consensus_params") \
                       + self.get_output_type(subcmd, out)+ [sample_io.files[0].name]

        if subcmd == "convert":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("convert_params") \
                       + self.get_output_type(subcmd, out)+ [sample_io.files[0].name]

        if subcmd == "filter":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("filter_params") \
                       + self.get_output_type(subcmd, out)+ [sample_io.files[0].name]

        if subcmd == "gtcheck":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("gtcheck_params") + [sample_io.files[0].name, ">", out + ".out"]

        if subcmd == "index":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("index_params") + [sample_io.files[0].name]

        if subcmd == "merge":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("merge_params") \
                       + self.get_output_type(subcmd, out)+ [sample_io.files[0].name]

        if subcmd == "norm":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("norm_params") \
                       + self.get_output_type(subcmd, out)+ [sample_io.files[0].name]

        if subcmd == "plugin":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("plugin_params") \
                       + self.get_output_type(subcmd, out)+ [sample_io.files[0].name]

        if subcmd == "query":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("query_params") \
                       + self.get_output_type(subcmd, out)+ [sample_io.files[0].name]

        if subcmd == "reheader":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("reheader_params") + [sample_io.files[0].name, ">", out + ".out"]

        if subcmd == "view":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("view_params") + [sample_io.files[0].name, ">", out + ".out"]

        if subcmd == "stats":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("stats_params") + [sample_io.files[0].name, ">", out + ".out"]

        if subcmd == "roh":
            self.cmd = ["bcftools", subcmd] + self.get_opt_params("roh_params") + [sample_io.files[0].name, ">", out + ".out"]

        if subcmd == "plot_vcfstats":
            self.cmd = ["plot-vcfstats", "-p", "plots/"] + self.get_opt_params("plot_vcfstats_params") + [sample_io.files[0].name]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="annotate", output_postfix=""):
        pass


