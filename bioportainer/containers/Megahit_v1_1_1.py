import os

from bioportainer.MultiCmdContainer import MultiCmdContainer


class Megahit_v1_1_1(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self._change_out_err_log = True
        self.output_filter = "final.contigs.fa"

    @MultiCmdContainer.impl_set_opt_params
    def set_megahit_params(self,
                       t="threads",
                       min_count=False,
                       k_list=False,
                       k_min=False,
                       k_max=False,
                       k_step=False,
                       no_mercy=False,
                       bubble_level=False,
                       merge_level=False,
                       prune_level=False,
                       low_local_ratio=False,
                       max_tip_len=False,
                       no_local=False,
                       kmin_1pass=False,
                       presets=False,
                       m="0.9",
                       mem_flag="1",
                       min_contig_len=False,
                       keep_tmp_files=False):
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_contig2fastg_params(self):
        """
        Usage: contig2fastg <kmer_size> <k_{kmer_size}.contigs.fa>
        :return:
        """
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="megahit"):
        if subcmd == "megahit":
            self.output_type = "fasta-se"
            if sample_io.io_type == "fastq-pe" or "fastq-pe-gz":
                input = ["-1", sample_io.files[0].name, "-2", sample_io.files[1].name]
            elif sample_io.io_type == "fastq-se"or "fastq-se-gz":
                input = ["-r", sample_io.files[0].name]
            elif sample_io.io_type == "fastq-inter" or "fastq-inter-gz":
                input = ["-12", sample_io.files[0].name]
            else:
                raise IOError

            self.cmd = ["megahit", "-o", "./", "-f"] + self.get_opt_params("megahit_params") + input

        if subcmd == "contig2fastg":
            self.input_allowed = ["fasta-se"]
            self.output_type = "fastg"
            file = sample_io.files[0].name
            k = [s for s in file if s.isdigit()][0]
            self.cmd = ["megahit_toolkit", "contig2fastg", k, file, ">", os.path.splitext(file)[0] + ".fastg"]

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="megahit"):
        pass
