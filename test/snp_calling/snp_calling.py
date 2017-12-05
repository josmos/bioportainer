from bioportainer import container, config, SampleList
import subprocess
import os
from io import StringIO


def download(fp):
    subprocess.call("curl ftp://" + fp + " > " + os.path.split(fp)[1], shell=True)

def head(fn, n):
    subprocess.call("zcat " + fn + " | head -n " + n + " | gzip > " + fn + ".tmp &&"
                    " mv " + fn + ".tmp " + fn, shell=True)
n = str(100000)
f1 = "ftp.sra.ebi.ac.uk/vol1/fastq/SRR507/SRR507778/SRR507778_1.fastq.gz"
f2 = "ftp.sra.ebi.ac.uk/vol1/fastq/SRR507/SRR507778/SRR507778_2.fastq.gz"
ref ="ftp.ensembl.org/pub/current_fasta/saccharomyces_cerevisiae/dna/" \
     "Saccharomyces_cerevisiae.R64-1-1.dna_sm.toplevel.fa.gz"

[download(f) for f in [f1, f2, ref] if not os.path.isfile(f[2])]
[head(os.path.split(f)[1], n) for f in [f1, f2]]
subprocess.call("gunzip -c " + os.path.split(ref)[1] + " > " + os.path.split(ref)[1][:-3], shell=True)
cf = StringIO("""log: snp_test.log
Samples:
    - id: SRR507778
      type: fastq-pe-gz
      files: [{},{}]""".format(os.path.split(f1)[1], os.path.split(f2)[1]))

fastq = config.load_configfile(cf)
ref = SampleList.SampleList.from_user("ref", "fasta-se", [ref[:-3]], len(fastq))

sam_idx = container.samtools_v1_3_1.run_parallel(ref, subcmd="faidx")
bwa_idx = container.bwa_v0_7_15.run_parallel(None, ref, subcmd="index")
bwa_out = container.bwa_v0_7_15\
    .set_mem_params(R="'@RG\tID:foo\tSM:bar\tLB:library1'")\
    .run_parallel(fastq, bwa_idx, subcmd="mem")
bam = container.samtools_v1_3_1.set_output_type("bam")\
    .set_sort_params(O="bam", l="0")\
    .run_parallel(bwa_out, subcmd="sort")
ref_dir = ref[0].files[0].file_path
cram = container.samtools_v1_3_1.set_output_type("cram")\
    .set_view_params(T=ref[0].files[0].name, C=True)\
    .run_parallel(bam, mount=(ref_dir,))
vcf = container.samtools_v1_3_1\
    .set_mpileup_params(u=True, g=True, f=ref[0].files[0].name)\
    .run_parallel(bam, subcmd="mpileup", mount=(ref_dir,))
vcf_bz = container.bcf_tools_v1_3_1\
    .set_call_params(v=True, m=True, O="z")\
    .run_parallel(vcf, subcmd="call")
vcf_idx = container.tabix_v0_2_5.run_parallel(vcf_bz)
stats = container.bcf_tools_v1_3_1\
    .set_stats_params(F=ref[0].files[0].name, s="-")\
    .run_parallel(vcf_bz, subcmd="stats")
#  plots = container.bcf_tools_v1_3_1.run_parallel(stats, subcmd="plot_vcfstats")
vcf_filetered = container.bcf_tools_v1_3_1\
    .set_filter_params(O="v", s="LOWQUAL", i="%QUAL>10")\
    .run_parallel(vcf_bz, subcmd="filter", output_postfix="_filtered")
