import bioportainer.containers.Bowtie2_v2_2_9
import bioportainer.containers.Fastqc_v0_11_15
import bioportainer.containers.Megahit_v1_1_1
import bioportainer.containers.Megahit_v1_1_2
import bioportainer.containers.Prodigal_v2_6_3
import bioportainer.containers.Recycler_latest
import bioportainer.containers.Recycler_v0_62
import bioportainer.containers.Samtools_v1_3_1
import bioportainer.containers.Trimmomatic_v0_36
import bioportainer.containers.hmmer_v3_1b2
import bioportainer.containers.spades_v3_11_0
import bioportainer.containers.Hisat_v2_1_0
import bioportainer.containers.srst2_v0_2_0
import bioportainer.containers.blast_v2_2_31
import bioportainer.containers.cd_hit_v4_6_8


class ContainerAdapter():
    def __init__(self):
        self.cd_hit_v4_6_8 = bioportainer.containers.cd_hit_v4_6_8.Cd_hit_v4_6_8(
            "cd-hit:4.6.8", None, sub_commands=["cd-hit-est"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz", "fasta-pe", "fasta-pe-gz", "fasta-se", "fasta-se-gz",
                           "fasta-inter", "fasta-inter-gz"])
        self.blast_v2_2_31 = bioportainer.containers.blast_v2_2_31.Blast_v2_2_31(
            "biocontainers/blast:2.2.31", None, sub_commands=["blastn", "blastp", "makeblastdb"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz"])

        self.fastqc_v0_11_15 = bioportainer.containers.Fastqc_v0_11_15.FastQC(
            "biocontainers/fastqc:0.11.15", "containers/dockerfiles/fastqc/0.11.15",
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz"],
            output_type="html")
        self.bowtie2_v2_2_9 = bioportainer.containers.Bowtie2_v2_2_9.Bowtie2(
            "biocontainers/bowtie2:2.2.9",
            "containers/dockerfiles/bowtie2/2.2.9",
            ["bowtie2", "bowtie2-inspect", "bowtie2-build"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz",
                           "fasta-se", "bt2"])
        self.hmmer_v3_1b2 = bioportainer.containers.hmmer_v3_1b2.Hmmer_v3_1b2(
            "customcontainers/hmmer:3.1b2", "containers/dockerfiles/hmmer_v3_1b2",
            sub_commands=["hmmpress", "hmmscan"],
            input_allowed=[""])

        self.megahit_v1_1_1 = bioportainer.containers.Megahit_v1_1_1.Megahit_v1_1_1(
            "customcontainers/megahit:1.1.1", "containers/dockerfiles/megahit_v1_1_1",
            sub_commands=["megahit", "contig2fastg"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fastq-inter",
                           "fastq-inter-gz"])

        self.megahit_v1_1_2 = bioportainer.containers.Megahit_v1_1_2.Megahit_v1_1_2(
            "customcontainers/megahit:1.1.2",
            "containers/dockerfiles/megahit_v1_1_2",
            sub_commands=["megahit", "contig2fastg"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz",
                           "fastq-inter", "fastq-inter-gz"])

        self.prodigal_v2_6_3 = bioportainer.containers.Prodigal_v2_6_3.Prodigal_v2_6_3(
            "biocontainers/prodigal:2.6.3", "containers/dockerfiles/prodigal_v2_6_3",
            input_allowed=["fasta-se", "genebank"],
            output_type=None)

        self.recycler_latest = bioportainer.containers.Recycler_latest.Recycler_latest(
            "customcontainers/recycler:latest", "containers/dockerfiles/recycler_latest",
            ["recycle", "get_simple_cycs", "make_fasta_from_fastg"],
            input_type="fastq-pe-gz")

        self.samtools_v1_3_1 = bioportainer.containers.Samtools_v1_3_1.Samtools_v1_3_1(
            "biocontainers/samtools:1.3.1", "containers/dockerfiles/Samtools_v1_3_1",
            ["view"], input_allowed=["sam", "bam", "cram"])

        self.trimmomatic_v0_36 = bioportainer.containers.Trimmomatic_v0_36.Trimmomatic_v0_36(
            "customcontainers/trimmomatic:0.36", "containers/dockerfiles/trimmomatic_v0_36",
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-pe-bz"],
            output_type="fastq-pe")

        self.spades_v3_11_0 = bioportainer.containers.spades_v3_11_0.Spades_v3_11_0(
            "customcontainers/spades:3.11.0", "containers/dockerfiles/spades_v3_11_0",
            ["metaspades"], input_allowed=["fastq-pe", "fastq_inter"])

        self.hisat_v2_1_0 = bioportainer.containers.Hisat_v2_1_0.Hisat_v2_1_0(
            "customcontainers/hisat:2.1.0",
            "containers/dockerfiles/hisat_v2_1_0",
            ["hisat2", "hisat2-inspect", "hisat2-build"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz",
                           "fasta-se", "bt2"])

        self.srst2_v0_2_0 = bioportainer.containers.srst2_v0_2_0.Srst2_v0_2_0("srst2:0.2.0",
            "containers/dockerfiles/srst2_v0_2_0", ["srst2", "getmlst"],
            input_allowed=["fastq-pe", "fastq-pe-gz", "fastq-se", "fastq-se-gz", "fasta-se"])
