from bioportainer import config, container, SampleIO, SampleList

# load the configfile
input = config.load_configfile(configfile="test_config.yaml")

# run Fastqc
fqc_io = container.fastqc_v0_11_15.run_parallel(input)


trimmed = container.trimmomatic_v0_36.set_input_type("fastq-pe-gz")\
    .set_opt_params(leading="10", trailing="10", slidingwindow="4:20", minlen="250")\
    .run_parallel(input)

trimmed_paired = trimmed.filter_files(".*P.fq.gz")  # filter paried files from trimmomatic output
trimmed_unpaired = trimmed.filter_files(".*U.fq.gz")  # filter inparied files from trimmomatic output

# create SampleIO object with reference fasta file
refseq = SampleIO.SampleIO.from_user("refseq", "fasta-se", ["CBS7435.fa"])

# build bowtie index
bt_idx = container.bowtie2_v2_2_9.run(None, refseq, None, subcmd="bowtie2-build")

# create a SampleList object of two refseqs
bt_idx = SampleList.SampleList.from_user(*[bt_idx] * 2)

bt_out = container.bowtie2_v2_2_9.set_bowtie2_params(very_fast=True, sensitive=False)\
   .set_input_type("fastq-pe-gz")\
   .run_parallel(trimmed_paired, bt_idx, trimmed_unpaired)

bt_idx.delete_files()
