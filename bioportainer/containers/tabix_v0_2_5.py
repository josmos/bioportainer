from bioportainer.SingleCmdContainer import SingleCmdContainer


class Tabix_v0_2_5(SingleCmdContainer):
    def __init__(self, image, image_directory, input_allowed, output_type):
        super().__init__(image, image_directory, input_allowed, output_type)

    @SingleCmdContainer.impl_set_opt_params
    def set_opt_params(self, p=False, s=False, b=False, e=False, S=False, c=False, r=False,
                       B=False, _0=False,  h=False, l=False, f=False, ):
        """Program: tabix (TAB-delimited file InderXer)
Version: 0.2.5 (r964)

Usage:   tabix <in.tab.bgz> [region1 [region2 [...]]]

Options: -p STR     preset: gff, bed, sam, vcf, psltbl [gff]
         -s INT     sequence name column [1]
         -b INT     start column [4]
         -e INT     end column; can be identical to '-b' [5]
         -S INT     skip first INT lines [0]
         -c CHAR    symbol for comment/meta lines [#]
         -r FILE    replace the header with the content of FILE [null]
         -B         region1 is a BED file (entire file will be read)
         -0         zero-based coordinate
         -h         print the header lines
         -l         list chromosome names
         -f         force to overwrite the index

"""
        return self

    @SingleCmdContainer.impl_run
    def run(self, sample_io):
        self.cmd = ["tabix"] + self.get_opt_params() + [f.name for f in sample_io.files]

    @SingleCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io):
        pass
