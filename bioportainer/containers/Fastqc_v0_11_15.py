from bioportainer.SingleCmdContainer import SingleCmdContainer


class FastQC(SingleCmdContainer):
    def __init__(self, image, image_directory, input_allowed, output_type):
        super().__init__(image, image_directory, input_allowed, output_type)
        self.change_out_err_log = True

    @SingleCmdContainer.impl_set_opt_params
    def set_opt_params(self,
                       cassava=False,
                       nano=False,
                       nofilter=False,
                       noextract=False,
                       nogroup=False,
                       t="threads",
                       contaminants=False,
                       adapters=False,
                       limits=False,
                       kmers=False,
                       quiet=True,
                       dir=False):
        return self

    @SingleCmdContainer.impl_run
    def run(self, sample_io):
        self.cmd = ["fastqc", "-o", "/data"] + self.get_opt_params() + \
                   [f.name for f in sample_io.files]

    @SingleCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io):
        pass
