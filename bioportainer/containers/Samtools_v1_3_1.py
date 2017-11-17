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
            if k == "_1":
                k = "1"
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
    def set_view_params(self, threads="threads", b=False, _1=False, C=False,
                        u=False, h=False, H=False,c=False,U=False, t=False, T=False, r=False, q="0",
                        l=False, m="0", f="0", F="0", x=False, B=False, s="0", REGIONS=()):
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_sort_params(self, l="9", m="768M", n=False, O=False, threads="threads"):
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_index_params(self, b=True, c=False, m=False):
        return self


    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="view"):
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

        if subcmd == "sort":
            out = os.path.splitext(sample_io.files[0].name)[0] + "_sorted." + self.output_type
            self.output_filter = ".*_sorted." + self.output_type
            self.cmd = ["samtools", subcmd] + self.get_opt_params("sort_params") + \
                       ["-o", out, sample_io.files[0].name]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="view"):
        pass


