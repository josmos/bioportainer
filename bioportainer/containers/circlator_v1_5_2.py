from bioportainer.MultiCmdContainer import MultiCmdContainer
import os


class Circlator_v1_5_2(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_minimus2_params()

    @MultiCmdContainer.impl_set_opt_params
    def set_minimus2_params(self, no_pre_merge=False):
        """usage: circlator minimus2 [options] <assembly.fasta> <output prefix>

Runs minimus2 circularisation pipeline, see
https://github.com/PacificBiosciences/Bioinformatics-
Training/wiki/Circularizing-and-trimming ... this script is a modified version
of that protocol. It first runs minimus2 on the input contigs (unless
--no_pre_merge is used). Then it tries to circularise each contig one at a
time, by breaking it in the middle and using the two pieces as input to
minimus2. If minimus2 outputs one contig, then that new one is assumed to be
circularised and is kept, otherwise the original contig is kept.

positional arguments:
  assembly.fasta  Name of original assembly
  output prefix   Prefix of output files

optional arguments:
  -h, --help      show this help message and exit
  --no_pre_merge  Do not do initial minimus2 run before trying to circularise
                  each contig"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample, subcmd="minimus2"):

        if subcmd == "minimus2":
            inp = [sample.files[0].name]
            out = [sample.id + "_circular_contigs"]
            self.cmd = [subcmd] + self.get_opt_params("metaspades_params") + inp + out

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample, subcmd="minimus2"):
        pass


