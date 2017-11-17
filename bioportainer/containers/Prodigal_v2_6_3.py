import os

from bioportainer.SingleCmdContainer import SingleCmdContainer


class Prodigal_v2_6_3(SingleCmdContainer):
    def __init__(self, image, image_directory, input_allowed, output_type):
        super().__init__(image, image_directory, input_allowed, output_type)
        self.change_out_err_log = True

    def get_opt_params(self):
        """
        return optional parameter dictionary as parameter-string-list
        :return: list of strings
        """
        l = []
        for k, v in self.opt_params.items():
            if k not in ["a", "d", "s"]: # remove opt ouput files
                if type(v) == bool and v is True:
                    l += ["--" + k.replace("_", "-")]
                elif type(v) == bool and v is False:
                    continue
                elif len(k) == 1:
                    l += ["-" + k, v]
                else:
                    k = k.replace("_", "-")
                    l += ["--" + k, v]

        return l

    @SingleCmdContainer.impl_set_opt_params
    def set_opt_params(self, a=False, c=False, d=False, f="gbk", g="11", n=False,
                       p="single", q=False, s=False, t=False, m=False):
        return self

    @SingleCmdContainer.impl_run
    def run(self, sample_io):
        fbn = os.path.splitext(sample_io.files[0].name)[0]
        opt_out_files = []
        out_file = fbn + ".gbk"
        if self.opt_params["a"]:
            opt_out_files += ["-a", fbn + ".prot.fa"]
        if self.opt_params["d"]:
            opt_out_files += ["-d", fbn + ".nucl.fa"]
        if self.opt_params["s"]:
            opt_out_files += ["-s", fbn + ".starts"]
        if self.opt_params["f"] == "gff":
            out_file = fbn + ".gff"
        elif self.opt_params["f"] == "sqn":
            out_file = fbn + ".sqn"
        elif self.opt_params["f"] == "sco":
            out_file = fbn + ".sco"

        self.cmd = ["prodigal", "-i", sample_io.files[0].name, "-o", out_file] + opt_out_files + self.get_opt_params()

    @SingleCmdContainer.impl_run_parallel
    def run_parallel(self, sample_io):
        pass


