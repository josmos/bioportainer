from bioportainer.SingleCmdContainer import SingleCmdContainer
from bioportainer.Config import config
import psutil
import os

class Prokka_v1_12_4(SingleCmdContainer):
    def __init__(self, image, image_directory, input_allowed, output_type):
        super().__init__(image, image_directory, input_allowed, output_type)
        self.change_out_err_log = True

    @SingleCmdContainer.impl_set_opt_params
    def set_opt_params(self, quiet=False, debug=False, force=True, addgenes=False, addmrna=False, locustag=False,
                       increment=False, gffver=False, compliant=False, centre=False, accver=False, genus=False,
                       species=False, strain=False, plasmid=False, kingdom=False, gcode=False, gram=False,
                       usegenus=False, proteins=False, hmms=False, metagenome=False, rawproduct=False, cdsrnaolap=False,
                       cpus="threads", fast=False, noanno=False, mincontiglen=False, evalue=False, rfam=False,
                       norrna=False, notrna=False, rnammer=False):
        """	  Prokka 1.12 by Torsten Seemann <torsten.seemann@gmail.com>
	Synopsis:
	  rapid bacterial genome annotation
	Usage:
	  prokka [options] <contigs.fasta>
	General:
	  --help            This help
	  --version         Print version and exit
	  --docs            Show full manual/documentation
	  --citation        Print citation for referencing Prokka
	  --quiet           No screen output (default OFF)
	  --debug           Debug mode: keep all temporary files (default OFF)
	Setup:
	  --listdb          List all configured databases
	  --setupdb         Index all installed databases
	  --cleandb         Remove all database indices
	  --depends         List all software dependencies
	Outputs:
	  --outdir [X]      Output folder [auto] (default '')
	  --force           Force overwriting existing output folder (default OFF)
	  --prefix [X]      Filename output prefix [auto] (default '')
	  --addgenes        Add 'gene' features for each 'CDS' feature (default OFF)
	  --addmrna         Add 'mRNA' features for each 'CDS' feature (default OFF)
	  --locustag [X]    Locus tag prefix [auto] (default '')
	  --increment [N]   Locus tag counter increment (default '1')
	  --gffver [N]      GFF version (default '3')
	  --compliant       Force Genbank/ENA/DDJB compliance: --addgenes --mincontiglen 200 --centre XXX (default OFF)
	  --centre [X]      Sequencing centre ID. (default '')
	  --accver [N]      Version to put in Genbank file (default '1')
	Organism details:
	  --genus [X]       Genus name (default 'Genus')
	  --species [X]     Species name (default 'species')
	  --strain [X]      Strain name (default 'strain')
	  --plasmid [X]     Plasmid name or identifier (default '')
	Annotations:
	  --kingdom [X]     Annotation mode: Archaea|Bacteria|Mitochondria|Viruses (default 'Bacteria')
	  --gcode [N]       Genetic code / Translation table (set if --kingdom is set) (default '0')
	  --gram [X]        Gram: -/neg +/pos (default '')
	  --usegenus        Use genus-specific BLAST databases (needs --genus) (default OFF)
	  --proteins [X]    FASTA or GBK file to use as 1st priority (default '')
	  --hmms [X]        Trusted HMM to first annotate from (default '')
	  --metagenome      Improve gene predictions for highly fragmented genomes (default OFF)
	  --rawproduct      Do not clean up /product annotation (default OFF)
	  --cdsrnaolap      Allow [tr]RNA to overlap CDS (default OFF)
	Computation:
	  --cpus [N]        Number of CPUs to use [0=all] (default '8')
	  --fast            Fast mode - only use basic BLASTP databases (default OFF)
	  --noanno          For CDS just set /product="unannotated protein" (default OFF)
	  --mincontiglen [N] Minimum contig size [NCBI needs 200] (default '1')
	  --evalue [n.n]    Similarity e-value cut-off (default '1e-06')
	  --rfam            Enable searching for ncRNAs with Infernal+Rfam (SLOW!) (default '0')
	  --norrna          Don't run rRNA search (default OFF)
	  --notrna          Don't run tRNA search (default OFF)
	  --rnammer         Prefer RNAmmer over Barrnap for rRNA prediction (default OFF)
"""
        return self

    @SingleCmdContainer.impl_run
    def run(self, sample_io, outdir="", prefix=""):
        self.cmd = ["prokka"] + self.get_opt_params() + [sample_io.files[0].name]

    @SingleCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io):
        pass