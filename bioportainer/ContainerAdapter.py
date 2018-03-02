import bioportainer.containers.bowtie2_v2_2_9
import bioportainer.containers.fastqc_v0_11_15
import bioportainer.containers.Megahit_v1_1_1
import bioportainer.containers.Megahit_v1_1_2
import bioportainer.containers.Prodigal_v2_6_3
import bioportainer.containers.Recycler_latest
import bioportainer.containers.Recycler_v0_62
import bioportainer.containers.Samtools_v1_3_1
import bioportainer.containers.Trimmomatic_v0_36
import bioportainer.containers.hmmer_v3_1b2
import bioportainer.containers.spades_v3_11_0
import bioportainer.containers.hisat_v2_1_0
import bioportainer.containers.srst2_v0_2_0
import bioportainer.containers.blast_v2_2_31
import bioportainer.containers.cd_hit_v4_6_8
import bioportainer.containers.bwa_v0_7_15
import bioportainer.containers.tabix_v0_2_5
import bioportainer.containers.bcf_tools_v1_3_1
import bioportainer.containers.kraken_v1_0
import bioportainer.containers.art_2016_06_05
import bioportainer.containers.picard_v2_3_9
import bioportainer.containers.quast_v4_6_1
import bioportainer.containers.circlator_v1_5_2
import bioportainer.containers.prokka_v1_12_4

class ContainerAdapter():
    def __init__(self):
        self.bcf_tools_v1_3_1 = bioportainer.containers.bcf_tools_v1_3_1.Bcf_tools_v1_3_1(
            "biocontainers/bcftools:1.3.1", None, sub_commands=["annotate", "call"],
            input_allowed=["vcf", "vcf-gz" "bcf"])

        self.tabix_v0_2_5 = bioportainer.containers.tabix_v0_2_5.Tabix_v0_2_5(
            "quay.io/biocontainers/tabix:0.2.5--0", None,
            input_allowed=["gff", "bed", "sam", "vcf", "psltbl"], output_type="")

        self.bwa_v0_7_15 = bioportainer.containers.bwa_v0_7_15.Bwa_v0_7_15(
            "biocontainers/bwa:0.7.15", None, sub_commands=["mem", "index"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz", "fasta-pe", "fasta-pe-gz", "fasta-se", "fasta-se-gz",
                           "fasta-inter", "fasta-inter-gz"])

        self.cd_hit_v4_6_8 = bioportainer.containers.cd_hit_v4_6_8.Cd_hit_v4_6_8(
            "quay.io/biocontainers/cd-hit:4.6.8", None, sub_commands=["cd-hit-est"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz", "fasta-pe", "fasta-pe-gz", "fasta-se", "fasta-se-gz",
                           "fasta-inter", "fasta-inter-gz"])
        self.blast_v2_2_31 = bioportainer.containers.blast_v2_2_31.Blast_v2_2_31(
            "biocontainers/blast:2.2.31", None, sub_commands=["blastn", "blastp", "makeblastdb"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz"])

        self.fastqc_v0_11_15 = bioportainer.containers.fastqc_v0_11_15.FastQC(
            "biocontainers/fastqc:0.11.15", None,
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz"], output_type="html")

        self.bowtie2_v2_2_9 = bioportainer.containers.bowtie2_v2_2_9.Bowtie2(
            "biocontainers/bowtie2:2.2.9", None,
            ["bowtie2", "bowtie2-inspect", "bowtie2-build"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz",
                           "fasta-se", "bt2"])
        self.hmmer_v3_1b2 = bioportainer.containers.hmmer_v3_1b2.Hmmer_v3_1b2(
            "quay.io/biocontainers/hmmer:3.1b2--3", None,
            sub_commands=["hmmpress", "hmmscan"], input_allowed=[""])

        self.megahit_v1_1_1 = bioportainer.containers.Megahit_v1_1_1.Megahit_v1_1_1(
            "quay.io/biocontainers/megahit:1.1.1--py36_0", None,
            sub_commands=["megahit", "contig2fastg"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz"])

        self.megahit_v1_1_2 = bioportainer.containers.Megahit_v1_1_2.Megahit_v1_1_2(
            "quay.io/biocontainers/megahit:1.1.2--py36_0", None,
            sub_commands=["megahit", "contig2fastg"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz",
                           "fastq-inter", "fastq-inter-gz"])

        self.prodigal_v2_6_3 = bioportainer.containers.Prodigal_v2_6_3.Prodigal_v2_6_3(
            "quay.io/biocontainers/prodigal:2.6.3--0", None,
            input_allowed=["fasta-se", "genebank"],
            output_type=None)

        self.recycler_latest = bioportainer.containers.Recycler_latest.Recycler_latest(
            "customcontainers/recycler:latest", "containers/dockerfiles/recycler_latest",
            ["recycle", "get_simple_cycs", "make_fasta_from_fastg"],
            input_type="fastq-pe-gz")

        # self.recycler_v0_62 = bioportainer.containers.Recycler_latest.Recycler_latest(
        #     "quay.io/biocontainers/recycler:0.6.2--py27_0", None,
        #     ["recycle", "get_simple_cycs", "make_fasta_from_fastg"], input_type="fastq-pe-gz")
        # not working because of missing -o parameter (fixted in next version)

        self.samtools_v1_3_1 = bioportainer.containers.Samtools_v1_3_1.Samtools_v1_3_1(
            "biocontainers/samtools:1.3.1", None,
            ["view"], input_allowed=["sam", "bam", "cram"])

        self.trimmomatic_v0_36 = bioportainer.containers.Trimmomatic_v0_36.Trimmomatic_v0_36(
            "quay.io/biocontainers/trimmomatic:0.36--5", None,
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-pe-bz"],
            output_type="fastq-pe")

        self.spades_v3_11_0 = bioportainer.containers.spades_v3_11_0.Spades_v3_11_0(
            "quay.io/biocontainers/spades:3.11.0--py36_zlib1.2.8_1", None,
            ["metaspades"], input_allowed=["fastq-pe", "fastq_inter"])

        self.hisat_v2_1_0 = bioportainer.containers.hisat_v2_1_0.Hisat_v2_1_0(
            "quay.io/biocontainers/hisat2:2.0.4--py35_0", None,
            ["hisat2", "hisat2-inspect", "hisat2-build"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz",
                           "fasta-se", "bt2"])

        self.srst2_v0_2_0 = bioportainer.containers.srst2_v0_2_0.Srst2_v0_2_0("srst2:0.2.0",
            "containers/dockerfiles/srst2_v0_2_0", ["srst2", "getmlst"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fasta-se"])

        self.kraken_v1_0 = bioportainer.containers.kraken_v1_0.Kraken_v1_0(
            "quay.io/biocontainers/kraken:1.0--pl5.22.0_0", None, ["kraken"], input_allowed=["fastq-pe", "fastq-pe-gz",
            "fastq-se", "fastq-se-gz", "fasta-se-gz", "fasta-se", "fasta_pe", "fasta_pe_gz"])

        self.art_2016_06_05 = bioportainer.containers.art_2016_06_05.Art_2016_06_05(
            "quay.io/biocontainers/art:2016.06.05--gsl1.16_0", None, ["art_illumina"],
            input_allowed = ["fastq-pe"])

        self.picard_v2_3_0 = bioportainer.containers.picard_v2_3_9.Picard_v2_3_0(
            "quay.io/biocontainers/picard:2.9.2--py35_1", None, ["CollectInsertSizeMetrics"], input_allowed=["bam"])

        self.quast_v4_6_1 = bioportainer.containers.quast_v4_6_1.Quast_v4_6_1(
            "quay.io/biocontainers/quast:4.6.1--py27_boost1.64_0", None, ["quast", "metaquast"],
            input_allowed=["fasta_se"])

        self.circlator_v1_5_2 = bioportainer.containers.circlator_v1_5_2.Circlator_v1_5_2(
            "customcontainers/circlator:1.5.5", "containers/dockerfiles/circlator_v1_5_5", ["minimus2"], input_allowed=["fasta_se"])

        self.prokka_v1_12_4 = bioportainer.containers.prokka_v1_12_4.Prokka_v1_12_4(
            "quay.io/biocontainers/prokka:1.12--4", None,  input_allowed=["fasta_se"], output_type="gff")

