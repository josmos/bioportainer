import bioportainer


input = bioportainer.config.load_configfile("config.yaml")

fastqc_out = bioportainer.container.fastqc_v0_11_15.run_parallel(input)

trimmed = bioportainer.container.fastqc_v0_11_15.run_parallel()



