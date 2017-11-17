from bioportainer.MultiCmdContainer import MultiCmdContainer
import os


class Hmmer_v3_1b2(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self._change_out_err_log = True

    @MultiCmdContainer.impl_set_opt_params
    def set_hmmpress_params(self, f=False):
        """hmmpress :: prepare an HMM database for faster hmmscan searches
# HMMER 3.1b2 (February 2015); http://hmmer.org/
# Copyright (C) 2015 Howard Hughes Medical Institute.
# Freely distributed under the GNU General Public License (GPLv3).
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Usage: hmmpress [-options] <hmmfile>

Options:
  -h : show brief help on version and usage
  -f : force: overwrite any previous pressed files"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_hmmscan_params(self, tblout=False, domtblout=False, pfamtblout=False, acc=False,
                           noali=False, notextw=False, textw="120", E="10.0", T=False, domE="10.0",
                           domT=False, ncE=False, incT=False, incdomE=False, incdomT=False,
                           cut_ga=False, cut_nc=False, cut_tc=False, max=False, F1="0.02", F2="1e-3",
                           F3="1e-5", nobias=False, nonull2=False, Z=False, domZ=False, seed="42",
                           qformat=False, daemon=False, cpu="threads"):
        """
        hmmscan :: search sequence(s) against a profile database
# HMMER 3.1b2 (February 2015); http://hmmer.org/
# Copyright (C) 2015 Howard Hughes Medical Institute.
# Freely distributed under the GNU General Public License (GPLv3).
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Usage: hmmscan [-options] <hmmdb> <seqfile>

Basic options:
  -h : show brief help on version and usage

Options controlling output:
  -o <f>           : direct output to file <f>, not stdout
  --tblout <f>     : save parseable table of per-sequence hits to file <f>
  --domtblout <f>  : save parseable table of per-domain hits to file <f>
  --pfamtblout <f> : save table of hits and domains to file, in Pfam format <f>
  --acc            : prefer accessions over names in output
  --noali          : don't output alignments, so output is smaller
  --notextw        : unlimit ASCII text output line width
  --textw <n>      : set max width of ASCII text output lines  [120]  (n>=120)

Options controlling reporting thresholds:
  -E <x>     : report models <= this E-value threshold in output  [10.0]  (x>0)
  -T <x>     : report models >= this score threshold in output
  --domE <x> : report domains <= this E-value threshold in output  [10.0]  (x>0)
  --domT <x> : report domains >= this score cutoff in output

Options controlling inclusion (significance) thresholds:
  --incE <x>    : consider models <= this E-value threshold as significant
  --incT <x>    : consider models >= this score threshold as significant
  --incdomE <x> : consider domains <= this E-value threshold as significant
  --incdomT <x> : consider domains >= this score threshold as significant

Options for model-specific thresholding:
  --cut_ga : use profile's GA gathering cutoffs to set all thresholding
  --cut_nc : use profile's NC noise cutoffs to set all thresholding
  --cut_tc : use profile's TC trusted cutoffs to set all thresholding

Options controlling acceleration heuristics:
  --max    : Turn all heuristic filters off (less speed, more power)
  --F1 <x> : MSV threshold: promote hits w/ P <= F1  [0.02]
  --F2 <x> : Vit threshold: promote hits w/ P <= F2  [1e-3]
  --F3 <x> : Fwd threshold: promote hits w/ P <= F3  [1e-5]
  --nobias : turn off composition bias filter

Other expert options:
  --nonull2     : turn off biased composition score corrections
  -Z <x>        : set # of comparisons done, for E-value calculation
  --domZ <x>    : set # of significant seqs, for domain E-value calculation
  --seed <n>    : set RNG seed to <n> (if 0: one-time arbitrary seed)  [42]
  --qformat <s> : assert input <seqfile> is in format <s>: no autodetection
  --daemon      : run program as a daemon
  --cpu <n>     : number of parallel CPU workers to use for multithreads
        """
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, mount=("path/to/hmmdb",), subcmd="hmmscan"):
        if subcmd == "hmmscan":
            hmmdb = os.path.split(mount[0])[1]
            seqfile = sample_io.files[0].name
            self.cmd = ["hmmscan"] + self.get_opt_params("hmmscan_params") + [hmmdb, seqfile]

        if subcmd == "hmmpress":
            self.cmd = ["hmmpress", "-h"]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="hmmalign"):
        pass

