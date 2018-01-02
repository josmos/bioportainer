import os
from bioportainer.MultiCmdContainer import MultiCmdContainer
from bioportainer.Config import config


class Kraken_v1_0(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_kraken_params()
        #self.set_kraken_build_params()
        #self.set_kraken_filter_params()
        #self.set_kraken_mpa_report_params()
        #self.set_kraken_report_params()
        #self.set_kraken_translate_params()


    @MultiCmdContainer.impl_set_opt_params
    def set_kraken_params(self,threads="threads", quick=False, min_hits=False,
                          unclassified_out=False, classified_out=False, only_classified_out=False,
                          preload=False, check_names=False):
        """Usage: kraken [options] <filename(s)>

Options:
  --db NAME               Name for Kraken DB
                          (default: none)
  --threads NUM           Number of threads (default: 1)
  --fasta-input           Input is FASTA format
  --fastq-input           Input is FASTQ format
  --gzip-compressed       Input is gzip compressed
  --bzip2-compressed      Input is bzip2 compressed
  --quick                 Quick operation (use first hit or hits)
  --min-hits NUM          In quick op., number of hits req'd for classification
                          NOTE: this is ignored if --quick is not specified
  --unclassified-out FILENAME
                          Print unclassified sequences to filename
  --classified-out FILENAME
                          Print classified sequences to filename
  --output FILENAME       Print output to filename (default: stdout); "-" will
                          suppress normal output
  --only-classified-output
                          Print no Kraken output for unclassified sequences
  --preload               Loads DB into memory before classification
  --paired                The two filenames provided are paired-end reads
  --check-names           Ensure each pair of reads have names that agree
                          with each other; ignored if --paired is not specified
  --help                  Print this message
  --version               Print version information

If none of the *-input or *-compressed flags are specified, and the
file is a regular file, automatic format detection is attempted.
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_kraken_filter_params(self, threshold=False):

        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="kraken", output_postfix="", input_type="fastq-pe", mount=None):
        self.input_type = input_type
        if subcmd == "kraken":
            self.output_type = "txt"
            out = sample_io.id + output_postfix
            self.input_allowed = ["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz"]

            if self.input_type == "fastq-pe":
                input = ["--paired", sample_io.files[0].name, sample_io.files[1].name]

            elif self.input_type == "fastq-pe-gz":
                input = ["--paired", "--gzip-compressed", sample_io.files[0].name, sample_io.files[1].name]

            elif self.input_type == ["fastq-se"]:
                input = [f.name for f in sample_io.files]

            elif self.input_type == ["fastq-se-gz"]:
                input = ["--gzip-compressed"] + [f.name for f in sample_io.files]

            else:
                raise IOError

            self.cmd = [subcmd, "--output", out] + self.get_opt_params("kraken_params") + input



    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="kraken", output_postfix="", input_type="fastq-pe", mount=None):
        pass
