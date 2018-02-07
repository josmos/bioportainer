from bioportainer import config, container, SampleIO, SampleList
import os
# load the configfile
input = config.load_configfile(configfile="test_config.yaml")

# run Fastqc
fqc_io = container.fastqc_v0_11_15.run_parallel(input)


trimmed = container.trimmomatic_v0_36.set_input_type("fastq-pe-gz")\
    .set_opt_params(leading="10", trailing="10", slidingwindow="4:20", minlen="250")\
    .run_parallel(input)
#
trimmed_paired = trimmed.filter_files(".*P.fq.gz")  # filter paried files from trimmomatic output
trimmed_unpaired = trimmed.filter_files(".*U.fq.gz")  # filter inparied files from trimmomatic output

spadesio = container.spades_v3_11_0.run_parallel(trimmed_paired,trimmed_unpaired, subcmd="spades")

# mh_io = container.megahit_v1_1_2\
#     .set_megahit_params(k_step="12", k_min="27", k_max="99", min_count="2", min_contig_len="500", kmin_1pass=True)\
#     .set_output_filter(None).run_parallel(trimmed_paired, threads=1)
#
# final = mh_io.filter_files("final.contigs.fa")
# subgraph = mh_io.filter_files(".*/k99.contigs.fa")
#
# refseq = SampleList.SampleList.from_user("refseq", "fasta-se", ["CBS7435.fa"], 2)
#
# ref_idx = container.bwa_v0_7_15.run_parallel(None, refseq, subcmd="index")
#
# bwa_sam = container.bwa_v0_7_15.run_parallel(trimmed_paired, ref_idx)
# build bowtie index
#bt_idx = container.bowtie2_v2_2_9.run(None, refseq, None, subcmd="bowtie2-build")

# create a SampleList object of two refseqs
#bt_idx = SampleList.SampleList.from_user(*[bt_idx] * 2)

#bt_out = container.bowtie2_v2_2_9.set_bowtie2_params(very_fast=True, sensitive=False)\
#   .set_input_type("fastq-pe-gz")\
#   .run_parallel(trimmed_paired, bt_idx, trimmed_unpaired)

#bt_idx.delete_files()

#blast_db_fa = "/home/josmos/pycharmprojects/bioportainer/test/blast_db/NCBI_plasmid_db.fna"

#blast_db = container.blast_v2_2_31.set_makeblastdb_params(parse_seqids=True).run(refseq, mount=(blast_db_fa,), subcmd="makeblastdb")

#blast_out = container.blast_v2_2_31\
#    .set_blastn_params(outfmt="'6 qseqid sacc stitle pident length mismatch gapopen qstart qend sstart send evalue bitscore'") \
#    .run(refseq, subcmd="blastn", mount=(blast_db_fa,))
