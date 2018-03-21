from bioportainer.MultiCmdContainer import MultiCmdContainer
import os


class Hmmer2go_v0_17_5(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_fetchmap_params()
        self.set_getorf_params()
        self.set_map2gaf_params()
        self.set_mapterms_params()
        self.set_pfamsearch_params()
        self.set_run_params()

    @MultiCmdContainer.impl_set_opt_params
    def set_fetchmap_params(self):
        """Usage: hmmer2go <command> [-m] [long options...]
	-m --man    Get the manual entry for a command

hmmer2go fetchmap [-o] [long options...]
	-o STR --outfile STR    A file to place the Pfam2GO mappings
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_getorf_params(self, a=False, l=False, t=False, nm=False):
        """Usage: hmmer2go <command> [-m] [long options...]
	-m --man    Get the manual entry for a command

hmmer2go getorf [-ailostv] [long options...]
	-i STR --infile STR       The fasta files to be translated
	-o STR --outfile STR      A file to place the translated sequences
	-l INT --orflen INT       The minimum length for which to report an
	                          ORF
	-a --all                  Annotate all the ORFs, not just the longest
	                          one
	-t INT --translate INT    Determines what to report for each ORF
	-s --sameframe            Report all ORFs in the same (sense) frame
	--nm --nomet              Do not report only those ORFs starting with
	                          Methionine
	-v --verbose              Print results to the terminal
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_map2gaf_params(self,s="species", g=False):
        """Usage: hmmer2go <command> [-m] [long options...]
	-m --man    Get the manual entry for a command

hmmer2go map2gaf [-gios] [long options...]
	-i STR --infile STR     Tab-delimited file containing gene -> GO term
	                        mappings (GO terms should be separated by
	                        commas).
	-o STR --outfile STR    File name for the association file.
	-s STR --species STR    The species name to be used in the
	                        association file.
	-g STR --gofile STR     GO.terms_alt_ids file containing the one
	                        letter code for each term.
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_mapterms_params(self, map=True):
        """Usage: hmmer2go <command> [-m] [long options...]
	-m --man    Get the manual entry for a command

hmmer2go mapterms [-iop] [long options...]
	-i STR --infile STR     The HMMscan output in table format (generated
	                        with '--tblout' option from HMMscan).
	-o STR --outfile STR    The file to hold the GO term/description
	                        mapping results.
	-p STR --pfam2go STR    The PFAMID->GO mapping file provided by the
	                        Gene Ontology.
	--map                   Produce of tab-delimted file of query
	                        sequence IDs and GO terms.
"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_pfamsearch_params(self,n=False, d=False):
        """Usage: hmmer2go <command> [-m] [long options...]
	-m --man    Get the manual entry for a command

hmmer2go pfamsearch [-dnot] [long options...]
	-t STR --terms STR      The term(s) to search against Pfam entries
	-o STR --outfile STR    The name of a file to write search results
	-d --createdb           A database of HMMs for the search terms
	                        should be created
	-n STR --dirname STR    The name of the directory to create for
	                        storing HMMs from the Pfam search results"""
        return self

    @MultiCmdContainer.impl_set_opt_params
    def set_run_params(self, n="threads"):
        """Usage: hmmer2go <command> [-m] [long options...]
	-m --man    Get the manual entry for a command

hmmer2go run [-dinop] [long options...]
	-p STR --program STR     The program to run for domain identification
	                         (NOT IMPLEMENTED: Defaults to hmmscan)
	-i STR --infile STR      The fasta file of translated amino acid
	                         sequences
	-n INT --cpus INT        The number of CPUs to use for the search
	-d STR --database STR    The database to search against (typically
	                         Pfam-A.hmm)
	-o STR --outfile STR     The report file to store matches against the
	                         database"""
        return self

    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="mapterms", mount=("path/to/hmmdb", "path/to/gomapings")):
        if subcmd == "getorf":
            inp = sample_io.files[0].name
            out = os.path.splitext(inp)[0] + ".faa"
            self.set_output_filter(".*.faa")
            self.cmd = ["hmmer2go", "run", "-i", inp, "-o", out] + self.get_opt_params("getorf_params")

        if subcmd == "run":
            inp = sample_io.files[0].name
            db = os.path.split(mount[0])[1]
            self.set_output_filter(".*out")
            self.cmd = ["hmmer2go", "run", "-d", db] + self.get_opt_params("run_params") + ["-i", inp]

        if subcmd == "fetchmap":
            self.cmd = ["hmmer2go", "fetchmap", "-o", "pfam2go"]

        if subcmd == "mapterms":
            if mount[1]:
                map = ["-p", os.path.split(mount[1])[1]]
            else:
                map = []
            tab = sample_io.files[0].name
            out = os.path.splitext(tab)[0] + "_GO.tsv"
            self.set_output_filter(".*.tsv")
            self.cmd = ["hmmer2go", "mapterms", ] + self.get_opt_params("mapterms_params") + ["-i", tab, "-o", out] + map

        if subcmd == "map2gaf":
            inp = sample_io.files[0].name
            out = os.path.splitext(inp)[0] + "_GO.gaf"
            self.set_output_filter(".*.gaf")
            self.cmd = ["hmmer2go", "map2gaf", "-i", inp, "-o", out] + self.get_opt_params("map2gaf_params")

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="mapterms", mount=("path/to/hmmdb",)):
        pass

