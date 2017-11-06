# Bioportainer

A python package for implementing simple workflows with Biocontainers. (https://github.com/BioContainers)

Supported tools:
- Bowtie2 v2.2.9
- FastQC v0.11.15
- Hisat2 v2.1.0 (not tested)
- Hmmer v3.1b2
- Megahit v1.1.1 / v 1.1.2
- Prodigal v2.6.3
- Recycler latest
- Samtools v.1.3.1
- Spades v3.11.0 (only Metaspades)
- Trimmomatic v0.36

## Install:
    
    cd /path/to/repo/
    pip3 install .

Dependencies: 
Docker (tested with Version: 17.05.0-ce; API version:  1.29)

Python >= 3.4, xxhash, PyYaml, docker, psutil

## Basic Usage:

### 1.) Make a config file in YAML format:

    ## Optional Settings: uncomment to change from default:
    # parallel containers: 2 # maximum number of containers to set_param parallel (default: 1)
    # threads per container: 4 # max number of threads per container (default : cpus available)
    # workdir: /path/to/output/directory/ # (default: working directory)
    # tempdir: /path/to/tmp/files/ # directory for temporary files (default: working directory)
    # log: mylog.txt # name of log file written to workdir (default: no logging)
     
    # Specify the input:
    Samples:
        - id: Sample1
          type: fastq-pe-gz # input file format
          files: [/path/to/inputfile/Sample1_1.fastq.gz,
                  /path/to/inputfile/Sample1_2.fastq.gz]
        - id: Sample2
          type: fastq-pe-gz # input file format
          files: [/path/to/inputfile/Sample2_1.fastq.gz,
                  /path/to/inputfile/Sample2_2.fastq.gz]

### 2.) Write your workflow:

    from bioportainer import config, container
    input = config.load_configfile(configfile="config.yaml")
    tool1_output = container.tool1.run_parallel(input)
    tool2_output = container.tool2.run_parallel(tool1_output)

Alternatively you can run one sample after the other:
    
    from bioportainer import config, container
    input = config.load_configfile(configfile="config.yaml")
    for sample in input:
        tool1_output = container.tool1.run(input)
        tool2_output = container.tool2.run(tool1_output)
    

An example Workflow can be found in the *test/* directory
    
### 3.) Output:

You find the output generated by the containers in the specified working directory 
with the subdirectories */container_name/sample_id/.*

## Detailed Usage:

### Config file:

#### Optional settings:

parallel containers: set a maximum number of containers to spawn parallel

threads per container: set the maximum numbers of cores to be used by one container

workdir: The Output will be written to the working directory of the python script. An alternative 
Path can be specified here.

tempdir: some tools support alternative paths for temporary files. this can be specified here. 
(not tested!)

#### Specify the input:

The input is defined as a list of Samples with the attributes "id" (a unique string to identify the 
sample), "files" (a list of file paths) and the file type. Find a list of possible file types in the
 appendix.The *config.load_configfile()* method returns a *Samplelist* object.
 
 

### SampleIO and SampleList objects:

*SampleIO* and *SampleList* (a List of SampleIOs) are complex class objects which serve as adapters to 
couple the input and output between containers.

#### Methods:

##### filter_files("regex") : filter files in SampleIO object(s) by a regular expression matching the filepath in
 the sample directory.
 
##### delete_files(): remove files in the SampleIO object(s) from the filesystem

##### from_user(id_, type_, files)

Both classes have a method to manually create an instance. The *SampleList* impementation combines
 positional arguments to a *SampleList* object. Example:
    
    from bioportainer import SampleIO, SampleList
    refseq = SampleIO.SampleIO.from_user("refseq", "type", ("path/to/file",))
    refseqs = SampleList.SampleList.from_user(*[refseq] * 2) 


### container Object:

The container object holds all available containers as attributes. 

#### Methods:

##### run(SampleIO, ... , mount=(mount/path/to/file,) (subcmd="subcmd"), threads=config.container_threads)
 
 The run Method does actually more than just running the container: It checks if the container is 
 available on the docker client and builds it if not. It checks the file cache. If output files are
 not found it starts a container with the specified  command, runs it and delete it when finished. 
 The container logs are written to the logfile if 
 specified. 
 
 Parameters:
 
 - SampleIO, one or more SampleIO object specifying the input
 - mount: tuple of file paths if single files need to be mounted to the container (e.g. a reference sequence)
 - subcmd string specifying the sub command (only if a container provides more than one command)
 

 Return:
 
 SampleIO object
 
##### run_parallel(SampleList, ... , mount(,)mount=(mount/path/to/file,) (subcmd="subcmd"), threads=config.container_threads)
 
 Parameters:
 
 same as run (positional arguments are of type SampleList)
 
 threads:override the number of cpus for the container specified in configfile (optional)
 
 Return:
 SampleList object
 
 
#####  set_opt_params()
 
 chained method to override the default values for optional parameters of the run command. Provides 
 the signature with all parameters availiable in the container (except those controlling input/output).
 Container with subcommands have the method implemented with functionname set_`<subcmd>`_params
 
 
#####  set_input_type()
 
 change the input-type for a container
 
 
#####  set_output_type()
 
 select the file_type for the SampleIO object returned from the run command
 
 
#####  set_output_filter()
 
 add a regex in addition to the output_type to filter the output files
 
 
# Caching
 
 All SampleList objects are pickled and safed in the .cacheIO directory under the working directory. 
 Any before running a container checksums for the inputfiles, the command string and the output files 
 are compared to those in the corresponding IO object. Containers will only run if the output files are 
 not missing or corrupted.
 
 
# Implementing new containers

1.) fork the repo

2.) Implement a container class in bioportainer/containers 
(derive from SingleCmdContainer or MultiCmdContainer) Provide complete method signatures for set_opt_params()
run() and run_parallel() using the corresponding impl_<func> decorator.

2.) If no Biocontainer exists: create a Dockerfile under bioportainer/containers/dockerfiles/<container_name> 
follow the Biocontainer implementation guidelines.

3.) Add the container as attribute to the ContainerAdapter class

4.) Test it

5.) Send a Merge Request
 
# Appendix

## File types:

| File Type      	| Description              	| possible extensions  	|
|----------------	|--------------------------	|----------------------	|
| fasta-se       	| Fasta single end         	| .fa ; .fasta         	|
| fasta-pe       	| Fasta paired end         	| .fa ; .fasta         	|
| fasta-inter    	| Fasta interleaved        	| .fa ; .fasta         	|
| fasta-pe-gz    	| Fasta single end gzipped 	| .fa.gz ;  .fasta.gz  	|
| fasta-se-gz    	| Fasta paired end gzipped 	| .fa.gz ; .fasta.gz   	|
| fasta-se-gz    	| Fasta inteleaved gzipped 	| .fa.gz ; .fasta.gz   	|
| fasta-se-bz    	| Fasta single end bzipped 	| .fa.bz2 ; .fasta.bz2 	|
| fasta-pe-bz    	| Fasta paired end bzipped 	| .fa.bz2 ; .fasta.bz2 	|
| fasta-inter-bz 	| Fasta inteleaved bzipped 	| .fa.bz2 ; .fasta.bz2 	|
| fastq-se       	| Fastq single end         	| .fq ; .fastq         	|
| fastq-pe       	| Fastq paired end         	| .fq ; .fastq         	|
| fastq-inter    	| Fastq interleaved        	| .fq ; .fastq         	|
| fastq-pe-gz    	| Fastq single end gzipped 	| .fq.gz ; .fastq.gz   	|
| fastq-se-gz    	| Fastq paired end gzipped 	| .fq.gz ; .fastq.gz   	|
| fastq-se-gz    	| Fastq inteleaved gzipped 	| .fq.gz ; .fastq.gz   	|
| fastq-se-bz    	| Fastq single end bzipped 	| .fq.bz2 ; .fastq.bz2 	|
| fastq-pe-bz    	| Fastq paired end bzipped 	| .fq.bz2 ; .fastq.bz2 	|
| fastq-inter-bz 	| Fastq inteleaved bzipped 	| .fq.bz2 ; .fastq.bz2 	|
| sam            	| sam format               	| .sam                 	|
| bam            	| bam format               	| .bam                 	|
| bai            	| bam index                	| .bam.bai             	|
| fastg          	| fasta graph              	| .fastg               	|
| gbk            	| Genebank format          	| .gbk ; .genebank     	|
| gff            	| gff format               	| .gff                 	|
| sqn            	| ncbi sqn format          	| .sqn                 	|
| bt2            	| Bowtie index             	| .bt2                 	|
| html           	| html                     	| .html                	|