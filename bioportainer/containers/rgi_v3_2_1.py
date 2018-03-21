import os

from bioportainer.MultiCmdContainer import MultiCmdContainer


class Rgi_v3_2_1(MultiCmdContainer):
        def __init__(self, image, image_directory, sub_commands, input_allowed):
            super().__init__(image, image_directory, sub_commands, input_allowed)
            self.set_main_params()
            self.set_tab_params()
            self.set_parser_params()
            self.set_database_params()

        @MultiCmdContainer.impl_set_opt_params
        def set_main_params(self, t=False, a=False, n="threads", clean=False, d=False, local=False):
            """usage: rgi main [-h] -i INPUT_SEQUENCE -o OUTPUT_FILE
	                [-t {read,contig,protein,wgs}] [-a {DIAMOND,BLAST}]
	                [-n THREADS] [--include_loose] [--local] [--clean] [--debug]
	                [--low_quality] [-d {wgs,plasmid,chromosome,NA}] [-v]

	Resistance Gene Identifier - 4.0.2 - Main

	optional arguments:
	  -h, --help            show this help message and exit
	  -i INPUT_SEQUENCE, --input_sequence INPUT_SEQUENCE
	                        input file must be in either FASTA (contig and
	                        protein), FASTQ(read) or gzip format! e.g
	                        myFile.fasta, myFasta.fasta.gz
	  -o OUTPUT_FILE, --output_file OUTPUT_FILE
	                        output folder and base filename
	  -t {read,contig,protein,wgs}, --input_type {read,contig,protein,wgs}
	                        specify data input type (default = contig)
	  -a {DIAMOND,BLAST}, --alignment_tool {DIAMOND,BLAST}
	                        specify alignment tool (default = BLAST)
	  -n THREADS, --num_threads THREADS
	                        number of threads (CPUs) to use in the BLAST search
	                        (default=32)
	  --include_loose       include loose hits in addition to strict and perfect
	                        hits
	  --local               use local database (default: uses database in
	                        executable directory)
	  --clean               removes temporary files
	  --debug               debug mode
	  --low_quality         use for short contigs to predict partial genes
	  -d {wgs,plasmid,chromosome,NA}, --data {wgs,plasmid,chromosome,NA}
	                        specify a data-type (default = NA)
	  -v, --version         prints software version number"""
            return self

        @MultiCmdContainer.impl_set_opt_params
        def set_tab_params(self):
            """usage: rgi tab [-h] -i AFILE

	Resistance Gene Identifier - 4.0.2 - Tab-delimited

	optional arguments:
	  -h, --help            show this help message and exit
	  -i AFILE, --afile AFILE
	                        must be a rgi json result file
"""
            return self

        @MultiCmdContainer.impl_set_opt_params
        def set_parser_params(self, t=False):
            """usage: rgi parser [-h] -i INPUT [-o OUTPUT] [--include_loose] [-t TYPE]

	Creates categorical .json files RGI wheel visualization. An input .json file
	containing the RGI results must be input.

	optional arguments:
	  -h, --help            show this help message and exit
	  -i INPUT, --input INPUT
	                        RGI results in a .json file
	  -o OUTPUT, --output OUTPUT
	                        Name/identifier for the output categorical .json files
	  --include_loose       Include loose hits in addition to strict and perfect
	                        hits
	  -t TYPE, --type TYPE  type of input sequence: contig, protein or read
"""
            return self

        @MultiCmdContainer.impl_set_opt_params
        def set_database_params(self):
            """usage: rgi database [-h] [-v] [--local]

	Resistance Gene Identifier - 4.0.2 - Database

	optional arguments:
	  -h, --help     show this help message and exit
	  -v, --version  prints data version number
	  --local        use local database (default: uses database in executable
	                 directory)"""
            return self

        @MultiCmdContainer.impl_run
        def run(self, sample_io, subcmd="main", output_postfix=""):
            if subcmd == "main":
                inp = sample_io.files[0].name
                out = sample_io.id + "_rgi" + output_postfix

                self.cmd = ["rgi", subcmd, "-i", inp, "-o", out] + self.get_opt_params("main_params")

            if subcmd == "tab":
                out = sample_io.id + output_postfix + "_rgi.txt"

                self.cmd = ["rgi", subcmd, "-h"] #+ self.get_opt_params("main_params") + \
                         #  ["--", self.index_prefix] + input + ["-S", out]
            if subcmd == "parser":
                out = sample_io.id + output_postfix + "_rgi.txt"

                self.cmd = ["rgi", subcmd, "-h"] #+ self.get_opt_params("main_params") + \
                         #  ["--", self.index_prefix] + input + ["-S", out]
            if subcmd == "database":
                self.cmd = ["rgi", subcmd]

            if subcmd == "load":
                self.cmd = ["rgi", subcmd, "--afile", "/data/localDB/card.json", "--local"]

        @MultiCmdContainer.impl_run_parallel
        def run_parallel(self, sample_io, subcmd="main", output_postfix=""):
            pass
