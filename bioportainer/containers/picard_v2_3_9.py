import os
from bioportainer.MultiCmdContainer import MultiCmdContainer
from bioportainer.Config import config


class Picard_v2_3_0(MultiCmdContainer):
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, sub_commands, input_allowed)
        self.set_CollectInsertSizeMetrics_params()

    def get_opt_params(self, param_attr):
        """
        return optional parameter dictionary as parameter-string-list
        :param param_attr: string: "get_<sub command>_params"
        :return: list of strings
        """
        p = getattr(self, param_attr)
        l = []
        for k, v in p.items():
            if v == "threads":
                v = str(config.container_threads)
            elif type(v) == bool and v is False:
                continue
            else:
                l += [k + "=" + v]

    @MultiCmdContainer.impl_set_opt_params
    def set_CollectInsertSizeMetrics_params(self, M="0.5", HISTOGRAM_FILE="insert_size_histogram.pdf",
                                            DEVIATIONS=False, HISTOGRAM_WIDTH=False, MINIMUM_PCT=False,
                                            METRIC_ACCUMULATION_LEVEL=False, INCLUDE_DUPLICATES=False,
                                            ASSUME_SORTED=False, STOP_AFTER=False):
        """USAGE: CollectInsertSizeMetrics [options]

Documentation: http://broadinstitute.github.io/picard/command-line-overview.html#CollectInsertSizeMetrics

This tool provides useful metrics for validating library construction including the insert size distribution and read orientation of paired-end libraries.

The expected proportions of these metrics vary depending on the type of library preparation used, resulting from technical differences between pair-end libraries and mate-pair libraries. For a brief primer on paired-end sequencing and mate-pair reads, see the GATK Dictionary (http://gatkforums.broadinstitute.org/discussion/6327/paired-end-mate-pair)

The CollectInsertSizeMetrics tool outputs the percentages of read pairs in each of the three orientations (FR, RF, and TANDEM) as a histogram. In addition, the insert size distribution is output as both a histogram (.insert_size_Histogram.pdf) and as a data table (.insert_size_metrics.txt).
Usage example:

java -jar picard.jar CollectInsertSizeMetrics \
      I=input.bam \
      O=insert_size_metrics.txt \
      H=insert_size_histogram.pdf \
      M=0.5
Note: If processing a small file, set the minimum percentage option (M) to 0.5, otherwise an error may occur.

Please see the InsertSizeMetrics documentation (https://broadinstitute.github.io/picard/picard-metric-definitions.html#InsertSizeMetrics) for further explanations of each metric.
Collect metrics about the insert size distribution of a paired-end library.
Version: 2.3.0(9a00c87b7ffdb01cfb5a0d6e76556146196babb8_1463071327)


Options:

--help
-h                            Displays options specific to this tool.

--stdhelp
-H                            Displays options specific to this tool AND options common to all Picard command line
                              tools.

--version                     Displays program version.

HISTOGRAM_FILE=File
H=File                        File to write insert size Histogram chart to.  Required.

DEVIATIONS=Double             Generate mean, sd and plots by trimming the data down to MEDIAN +
                              DEVIATIONS*MEDIAN_ABSOLUTE_DEVIATION. This is done because insert size data typically
                              includes enough anomalous values from chimeras and other artifacts to make the mean and
                              sd grossly misleading regarding the real distribution.  Default value: 10.0. This option
                              can be set to 'null' to clear the default value.

HISTOGRAM_WIDTH=Integer
W=Integer                     Explicitly sets the Histogram width, overriding automatic truncation of Histogram tail.
                              Also, when calculating mean and standard deviation, only bins <= Histogram_WIDTH will be
                              included.  Default value: null.

MINIMUM_PCT=Float
M=Float                       When generating the Histogram, discard any data categories (out of FR, TANDEM, RF) that
                              have fewer than this percentage of overall reads. (Range: 0 to 1).  Default value: 0.05.
                              This option can be set to 'null' to clear the default value.

METRIC_ACCUMULATION_LEVEL=MetricAccumulationLevel
LEVEL=MetricAccumulationLevel The level(s) at which to accumulate metrics.    Default value: [ALL_READS]. This option
                              can be set to 'null' to clear the default value. Possible values: {ALL_READS, SAMPLE,
                              LIBRARY, READ_GROUP} This option may be specified 0 or more times. This option can be set
                              to 'null' to clear the default list.

INCLUDE_DUPLICATES=Boolean    If true, also include reads marked as duplicates in the insert size histogram.  Default
                              value: false. This option can be set to 'null' to clear the default value. Possible
                              values: {true, false}

INPUT=File
I=File                        Input SAM or BAM file.  Required.

OUTPUT=File
O=File                        File to write the output to.  Required.

ASSUME_SORTED=Boolean
AS=Boolean                    If true (default), then the sort order in the header file will be ignored.  Default
                              value: true. This option can be set to 'null' to clear the default value. Possible
                              values: {true, false}

STOP_AFTER=Long               Stop after processing N reads, mainly for debugging.  Default value: 0. This option can
                              be set to 'null' to clear the default value."""
        return self


    @MultiCmdContainer.impl_run
    def run(self, sample_io, subcmd="CollectInsertSizeMetrics", out_prefix="", mount=None):
        if subcmd == "CollectInsertSizeMetrics":
            self.cmd = ["picard", subcmd, "I=" + sample_io.files[0].name, "O=" + sample_io.id + out_prefix + "_metrics.txt"] + self.get_opt_params("CollectInsertSizeMetrics_params")

    @MultiCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io, subcmd="CollectInsertSizeMetrics", out_name="", mount=None):
        pass



