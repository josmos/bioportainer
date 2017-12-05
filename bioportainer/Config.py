import os
import docker
import yaml
import bioportainer.SampleList as Cio
import bioportainer.Logger as Logger


class Config:
    """
    Singleton class for global shared vars
    """
    __instance = None

    def __new__(cls):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(Config, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        Config.__instance.client = docker.from_env()
        Config.__instance.threads = 1  # max number of parallel running containers
        Config.__instance.container_threads = str(os.cpu_count())  # max cpus for each container
        Config.__instance.work_dir = None  # working directory
        Config.__instance.tmp_dir = None  # temp host_dir (can be passed as arg to some tools)
        Config.__instance.logger = None  # workflow logger
        Config.__instance.samples = None  # SampleList object

    @classmethod
    def load_configfile(cls, configfile):
        """
        Update Config instance attributes form config file
        :param configfile:
        :return:
        """
        def check_path(directory):
            if not os.path.isdir(directory):
                raise NotADirectoryError
            else:
                return directory

        def make_dir(dir):
            if not os.path.isdir(dir):
                os.makedirs(dir)
            return dir

        if configfile:
            try:
                configfile = yaml.load(open(configfile).read())
            except TypeError:
                configfile = yaml.load(configfile.read())

            cls.__instance.samples = Cio.SampleList.from_configfile(configfile)

            if "parallel containers" in configfile:
               cls.__instance.threads = int(configfile["parallel containers"])

            if "threads per container" in configfile:
                cls.__instance.container_threads = configfile["threads per container"]

            if "workdir" in configfile:
                cls.__instance.work_dir = check_path(configfile["workdir"])
                cls.__instance.cache_dir = make_dir(os.path.join(cls.__instance.work_dir, ".cacheIO"))  # Path for saving pickle objects
            else:
                cls.__instance.work_dir = os.getcwd()
                cls.__instance.cache_dir = make_dir(os.path.join(cls.__instance.work_dir, ".cacheIO"))

            if "tempdir" in configfile:
                cls.__instance.tmp_dir = check_path(configfile["tempdir"])
            else:
                cls.__instance.tmp_dir = cls.__instance.work_dir

            if "log" in configfile:
                log_file = os.path.join(cls.__instance.work_dir, configfile["log"])
                cls.__instance.logger = Logger.setup_logger("logger", log_file)

        return cls.__instance.samples

config = Config()
