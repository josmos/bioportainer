from bioportainer.MultiCmdContainer import MultiCmdContainer
import os


class Spades_v3_11_0(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_metaspades_params()

    @MultiCmdContainer.impl_set_opt_params
    def set_spades_params(self, sc=False, rna=False, plasmid=False, iontorrent=False, test=False,
                          sanger=False, pacbio=False, nanopore=False, tslr=False, disable_rr=False,
                          trusted_contigs=False, untrusted_contigs=False, only_assembler=False,
                          only_error_correction=False, careful=False, disable_gzip_output=False,
                          threads="threads", m=False, cov_cutoff=False, phred_offset=False, k=False):
        """SPAdes genome assembler v3.11.0

	Usage: /usr/local/bin/spades.py [options] -o <output_dir>

	Basic options:
	-o	<output_dir>	directory to store all the resulting files (required)
	--sc			this flag is required for MDA (single-cell) data
	--meta			this flag is required for metagenomic sample data
	--rna			this flag is required for RNA-Seq data
	--plasmid		runs plasmidSPAdes pipeline for plasmid detection
	--iontorrent		this flag is required for IonTorrent data
	--test			runs SPAdes on toy dataset
	-h/--help		prints this usage message
	-v/--version		prints version

	Input data:
	--12	<filename>	file with interlaced forward and reverse paired-end reads
	-1	<filename>	file with forward paired-end reads
	-2	<filename>	file with reverse paired-end reads
	-s	<filename>	file with unpaired reads
	--pe<#>-12	<filename>	file with interlaced reads for paired-end library number <#> (<#> = 1,2,..,9)
	--pe<#>-1	<filename>	file with forward reads for paired-end library number <#> (<#> = 1,2,..,9)
	--pe<#>-2	<filename>	file with reverse reads for paired-end library number <#> (<#> = 1,2,..,9)
	--pe<#>-s	<filename>	file with unpaired reads for paired-end library number <#> (<#> = 1,2,..,9)
	--pe<#>-<or>	orientation of reads for paired-end library number <#> (<#> = 1,2,..,9; <or> = fr, rf, ff)
	--s<#>		<filename>	file with unpaired reads for single reads library number <#> (<#> = 1,2,..,9)
	--mp<#>-12	<filename>	file with interlaced reads for mate-pair library number <#> (<#> = 1,2,..,9)
	--mp<#>-1	<filename>	file with forward reads for mate-pair library number <#> (<#> = 1,2,..,9)
	--mp<#>-2	<filename>	file with reverse reads for mate-pair library number <#> (<#> = 1,2,..,9)
	--mp<#>-s	<filename>	file with unpaired reads for mate-pair library number <#> (<#> = 1,2,..,9)
	--mp<#>-<or>	orientation of reads for mate-pair library number <#> (<#> = 1,2,..,9; <or> = fr, rf, ff)
	--hqmp<#>-12	<filename>	file with interlaced reads for high-quality mate-pair library number <#> (<#> = 1,2,..,9)
	--hqmp<#>-1	<filename>	file with forward reads for high-quality mate-pair library number <#> (<#> = 1,2,..,9)
	--hqmp<#>-2	<filename>	file with reverse reads for high-quality mate-pair library number <#> (<#> = 1,2,..,9)
	--hqmp<#>-s	<filename>	file with unpaired reads for high-quality mate-pair library number <#> (<#> = 1,2,..,9)
	--hqmp<#>-<or>	orientation of reads for high-quality mate-pair library number <#> (<#> = 1,2,..,9; <or> = fr, rf, ff)
	--nxmate<#>-1	<filename>	file with forward reads for Lucigen NxMate library number <#> (<#> = 1,2,..,9)
	--nxmate<#>-2	<filename>	file with reverse reads for Lucigen NxMate library number <#> (<#> = 1,2,..,9)
	--sanger	<filename>	file with Sanger reads
	--pacbio	<filename>	file with PacBio reads
	--nanopore	<filename>	file with Nanopore reads
	--tslr	<filename>	file with TSLR-contigs
	--trusted-contigs	<filename>	file with trusted contigs
	--untrusted-contigs	<filename>	file with untrusted contigs

	Pipeline options:
	--only-error-correction	runs only read error correction (without assembling)
	--only-assembler	runs only assembling (without read error correction)
	--careful		tries to reduce number of mismatches and short indels
	--continue		continue run from the last available check-point
	--restart-from	<cp>	restart run with updated options and from the specified check-point ('ec', 'as', 'k<int>', 'mc')
	--disable-gzip-output	forces error correction not to compress the corrected reads
	--disable-rr		disables repeat resolution stage of assembling

	Advanced options:
	--dataset	<filename>	file with dataset description in YAML format
	-t/--threads	<int>		number of threads
					[default: 16]
	-m/--memory	<int>		RAM limit for SPAdes in Gb (terminates if exceeded)
					[default: 250]
	--tmp-dir	<dirname>	directory for temporary files
					[default: <output_dir>/tmp]
	-k		<int,int,...>	comma-separated list of k-mer sizes (must be odd and
					less than 128) [default: 'auto']
	--cov-cutoff	<float>		coverage cutoff value (a positive float number, or 'auto', or 'off') [default: 'off']
	--phred-offset	<33 or 64>	PHRED quality offset in the input reads (33 or 64)
					[default: auto-detect]"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_metaspades_params(self, only_error_correction=False, only_assembler=False, irontorrent=False,
                              disable_gzip_output=False, disable_rr=False, t="threads",
                              memory="max_availiable_g", phred_offset=False, k=False):
        """SPAdes genome assembler v3.11.0 [metaSPAdes mode]

Usage: /home/biodocker/SPAdes-3.11.0-Linux/bin/metaspades.py [options] -o <output_dir>

Basic options:
-o	<output_dir>	directory to store all the resulting files (required)
--iontorrent		this flag is required for IonTorrent data
--test			runs SPAdes on toy dataset
-h/--help		prints this usage message
-v/--version		prints version

Input data:
--12	<filename>	file with interlaced forward and reverse paired-end reads
-1	<filename>	file with forward paired-end reads
-2	<filename>	file with reverse paired-end reads
-s	<filename>	file with unpaired reads
--pe<#>-12	<filename>	file with interlaced reads for paired-end library number <#> (<#> = 1,2,..,9)
--pe<#>-1	<filename>	file with forward reads for paired-end library number <#> (<#> = 1,2,..,9)
--pe<#>-2	<filename>	file with reverse reads for paired-end library number <#> (<#> = 1,2,..,9)
--pe<#>-s	<filename>	file with unpaired reads for paired-end library number <#> (<#> = 1,2,..,9)
--pe<#>-<or>	orientation of reads for paired-end library number <#> (<#> = 1,2,..,9; <or> = fr, rf, ff)
--s<#>		<filename>	file with unpaired reads for single reads library number <#> (<#> = 1,2,..,9)
--tslr	<filename>	file with TSLR-contigs
--trusted-contigs	<filename>	file with trusted contigs
--untrusted-contigs	<filename>	file with untrusted contigs

Pipeline options:
--only-error-correction	runs only read error correction (without assembling)
--only-assembler	runs only assembling (without read error correction)
--continue		continue run from the last available check-point
--restart-from	<cp>	restart run with updated options and from the specified check-point ('ec', 'as', 'k<int>', 'mc')
--disable-gzip-output	forces error correction not to compress the corrected reads
--disable-rr		disables repeat resolution stage of assembling

Advanced options:
--dataset	<filename>	file with dataset description in YAML format
-t/--threads	<int>		number of threads [default: 16]
-m/--memory	<int>		RAM limit for SPAdes in Gb (terminates if exceeded) [default: 250]
--tmp-dir	<dirname>	directory for temporary files [default: <output_dir>/tmp]
-k		<int,int,...>	comma-separated list of k-mer sizes (must be odd and less than 128) [default: 'auto']
--phred-offset	<33 or 64>	PHRED quality offset in the input reads (33 or 64) Sdefault: auto-detect]

        """
        return self

    @MultiCmdContainer.impl_run
    def run(self, paired_io, unpaired_io, subcmd="metaspades", subdir=""):

        if subcmd == "metaspades":
            inp = []
            if paired_io.io_type == "fastq-pe-gz":
                inp = ["--pe1-1", paired_io.files[0].name, "--pe1-2", paired_io.files[1].name]
            elif paired_io.io_type == "fastq-inter":
                inp = ["---pe1-12", paired_io.files[0].name]
            if unpaired_io:
                for f in unpaired_io.files:
                    inp += ["--pe1-s", f.name]
            if subdir != "":
                subdir = subdir + "/"
            out = ["-o", "/data/" + subdir]
            self.cmd = [subcmd + ".py"] + self.get_opt_params("metaspades_params") + inp + out

        if subcmd == "spades":
            inp = []
            if paired_io.io_type == "fastq-pe-gz":
                inp = ["--pe1-1", paired_io.files[0].name, "--pe1-2", paired_io.files[1].name]
            elif paired_io.io_type == "fastq-inter":
                inp = ["---pe1-12", paired_io.files[0].name]
            if unpaired_io:
                for f in unpaired_io.files:
                    inp += ["--pe1-s", f.name]
            if subdir != "":
                subdir = subdir + "/"
            out = ["-o", "/data/" + subdir]
            self.cmd = [subcmd + ".py"] + self.get_opt_params("spades_params") + inp + out

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, paired_io, unpaired_io, subcmd="metaspades", subdir=""):
        pass


