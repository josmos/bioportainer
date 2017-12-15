from bioportainer.SingleCmdContainer import SingleCmdContainer

from bioportainer.Config import config


class Trimmomatic_v0_36(SingleCmdContainer):
    def __init__(self, image, image_directory, input_allowed, output_type):
        super().__init__(image, image_directory, input_allowed, output_type)
        self.set_opt_params()
        self.change_out_err_log = True

    def set_opt_params(self,
                       threads="threads", phred64=False, phred33=True, trimlog=False,
                       quiet=False, validatepairs=False, illuminaclip_custom=None,
                       illuminaclip_NexteraPE=False, illuminaclip_TruSeq2PE=False,
                       illuminaclip_TruSeq2SE=False, illuminaclip_TruSeq3PE2=False,
                       illuminaclip_TruSeq3PE=False, illuminaclip_TruSeq3SE=False,
                       slidingwindow=None, maxinfo=None, leading=None, trailing=None, crop=None,
                       headcrop=None, minlen=None, avgqual=None, topphred33=None, topphred64=None):
        trim_params = []
        paramlist = []
        if threads == "threads":
            threads = str(config.container_threads)
        paramlist += ["-threads", threads]
        if phred33:
            paramlist += ["-phred33"]
        if phred64:
            paramlist += ["-phred64"]
        if trimlog:
            paramlist += ["-trimlog", trimlog]
        if quiet:
            paramlist += ["-quiet"]
        if validatepairs:
            paramlist += ["-validatePairs"]
        if illuminaclip_custom:
            trim_params += ["ILLUMINACLIP:" + illuminaclip_custom]
        if illuminaclip_NexteraPE:
            trim_params += ["ILLUMINACLIP:/usr/local/share/trimmomatic/adapters/NexteraPE-PE.fa:" + illuminaclip_NexteraPE]
        if illuminaclip_TruSeq2SE:
            trim_params += ["ILLUMINACLIP:/usr/local/share/trimmomatic/adapters/TruSeq2-SE.fa:" + illuminaclip_TruSeq2SE]
        if illuminaclip_TruSeq2PE:
            trim_params += ["ILLUMINACLIP:/usr/local/share/trimmomatic/adapters/TruSeq2-PE.fa:" + illuminaclip_TruSeq2PE]
        if illuminaclip_TruSeq3PE:
            trim_params += ["ILLUMINACLIP:/usr/local/share/trimmomatic/adapters/TruSeq3-PE.fa:" + illuminaclip_TruSeq3PE]
        if illuminaclip_TruSeq3PE2:
            trim_params += ["ILLUMINACLIP:/usr/local/share/trimmomatic/adapters/TruSeq3-PE-2.fa:" + illuminaclip_TruSeq3PE2]
        if illuminaclip_TruSeq3SE:
            trim_params += ["ILLUMINACLIP:/usr/local/share/trimmomatic/adapters/TruSeq3-SE.fa:" + illuminaclip_TruSeq3SE]
        if slidingwindow:
            trim_params += ["SLIDINGWINDOW:" + slidingwindow]
        if maxinfo:
            trim_params += ["MAXINFO:" + maxinfo]
        if leading:
            trim_params += ["LEADING:" + leading]
        if trailing:
            trim_params += ["TRAILING:" + trailing]
        if crop:
            trim_params += ["CROP:" + crop]
        if headcrop:
            trim_params += ["HEADCROP:" + headcrop]
        if minlen:
            trim_params += ["MINLEN:" + minlen]
        if avgqual:
            trim_params += ["AVGQUAL:" + avgqual]
        if topphred33:
            trim_params += ["TOPHRED33:" + topphred33]
        if topphred64:
            trim_params += ["TOPHRED64:" + topphred64]

        self.opt_params = paramlist
        self.trim_params = trim_params

        return self

    @SingleCmdContainer.impl_run
    def run(self, sample_io, mount=None):
        """
        Usage:
	       PE [-version] [-threads <threads>] [-phred33|-phred64] [-trimlog <trimLogFile>] [-quiet] [-validatePairs] [-basein <inputBase> | <inputFile1> <inputFile2>] [-baseout <outputBase> | <outputFile1P> <outputFile1U> <outputFile2P> <outputFile2U>] <trimmer1>...
	    or:
	       SE [-version] [-threads <threads>] [-phred33|-phred64] [-trimlog <trimLogFile>] [-quiet] <inputFile> <outputFile> <trimmer1>...
	    or:
	     version
        :param sample_io:
        :return:
       """
        if sample_io.io_type == "fastq-pe" or "fastq-pe-gz" or "fastq-pe-bz":
            self.output_type = self.input_type
            baseout = ""
            for c1, c2 in zip(sample_io.files[0].name, sample_io.files[1].name):
                if c1 == c2:
                    baseout += c2
                else:
                    if baseout[-1] == "_":
                        baseout = baseout[:-1]
                    break
            if self.output_type == "fastq-pe":
                baseout += ".fq"
            elif self.output_type == "fastq-pe-gz":
                baseout += ".fq.gz"
            elif self.output_type == "fastq-pe-bz":
                baseout += ".fq.bz2"
            baseout = ["-baseout", baseout]
            mode = ["PE"]
            input = [sample_io.files[0].name, sample_io.files[1].name]
        elif sample_io.io_type == ("fastq-se"or "fastq-se-gz" or "fastq-se-bz"):
            baseout = ["-baseout", sample_io.files[0].name]
            mode = ["SE"]
            input = [sample_io.files[0].name]

        else:
            raise IOError

        self.cmd = ["trimmomatic"] + mode + self.opt_params + input + baseout + self.trim_params

    @SingleCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, mount=None):
        pass

