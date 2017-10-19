from bioportainer.MultiCmdContainer import MultiCmdContainer


class Recycler_latest(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_type):
        super().__init__(image, image_directory, sub_commands, input_type)

    @MultiCmdContainer.impl_set_opt_params
    def set_recycle_params(self, length="1000", m="0.5", iso="False"):
        """gets simple (single contig) cycles from plasmid metagenomes, leaves rest of
graph as is; outputs these to two separate files

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input (SPAdes 3.50+) FASTG to process
  -m MIN_LENGTH, --min_length MIN_LENGTH
                        Minimum cycle length to keep (shorter cycles put in
                        new graph file; default = 1000)

        :param length:
        :param m:
        :param iso:
        :return:
        """
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_get_simple_cycs_params(self, m="1000"):
        """gets simple (single contig) cycles from plasmid metagenomes, leaves rest of
graph as is; outputs these to two separate files

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input (SPAdes 3.50+) FASTG to process
  -m MIN_LENGTH, --min_length MIN_LENGTH
                        Minimum cycle length to keep (shorter cycles put in
                        new graph file; default = 1000)

        :param m:
        :return:
        """
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_make_fasta_from_fastg_params(self):
        """recycle extracts cycles likely to be plasmids from metagenome and genome
assembly graphs

optional arguments:
  -h, --help            show this help message and exit
  -g GRAPH, --graph GRAPH
                        (spades 3.50+) FASTG file to process [recommended:
                        before_rr.fastg]
"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, graph_io, bam_io, subcmd="recycle", k=""):
        """

        :param graph_io: sample_io object with fastg file
        :param bam_io: sample_io object with mapped bam file
        :param subcmd: "recycle" or "get_simple_cycs" or "make_fasta_from_fastg"
        :param k: max_kmer size from assembly graph (required for recycle subcommand)
        :return:
        """
        graph = ["-g", graph_io.files[0].name]
        if subcmd == "recycle":
            k = ["-k", k]
            bam = ["-b", bam_io.files[0].name]
            self.cmd = [subcmd + ".py", "-o", self.out_dir] + graph + k + bam + self.get_opt_params("recycle_params") + ["-o", "/data/"]
            self.output_type = "fasta-se"

        elif subcmd == "get_simple_cycs":
            self.cmd = [subcmd + ".py"]

        elif subcmd == "make_fasta_from_fastg":
            self.cmd = [subcmd + ".py"] + graph

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, graph_io, bam_io, subcmd="recycle", k=""):
        """
        :param graph_io: sample_io object with fastg file
        :param bam_io: sample_io object with mapped bam file
        :param subcmd: "recycle" or "get_simple_cycs" or "make_fasta_from_fastg"
        :param k: max_kmer size from assembly graph (required for recycle subcommand)
        :return:
        """
        pass


