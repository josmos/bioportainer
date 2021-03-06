import copy
import operator
import os
from pathlib import Path
import shutil
import pickle
import re
import xxhash
import bioportainer.Config
from inspect import stack


class SampleFile:
    def __init__(self, path, host_dir, id):
        path = path if path.startswith("/") else os.path.abspath(path)
        self._id = id
        self._name = self.set_name(path, host_dir)
        self._file_path = path
        self._checksum = self.calc_checksum()

    @staticmethod
    def set_name(path, host_dir):
        return path[len(host_dir) + 1:]

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def file_path(self):
        return self._file_path

    @property
    def checksum(self):
        return self._checksum

    def calc_checksum(self):
        bs = 65536
        xx = xxhash.xxh64(seed=1)
        with open(self.file_path, 'rb') as kali_file:
            file_buffer = kali_file.read(bs)
            while len(file_buffer) > 0:
                xx.update(file_buffer)
                file_buffer = kali_file.read(bs)
        return xx.hexdigest()

    def check_checksum(self):
        return True if self.calc_checksum() == self.checksum else False

    def __hash__(self):
        return self.checksum

    def __eq__(self, other):
        return self.checksum == other.checksum


class SampleIO:
    def __init__(self, input_dict, hostdir, input_files=None):
        """
        :param input_dict: input dictionary returned from container.run
        or parsed from config yaml file.
        """
        self._id = input_dict["id"]
        self._io_type = input_dict["type"]
        self._host_dir = hostdir
        self._files = sorted([SampleFile(p, self._host_dir, self.id) for p in input_dict["files"]],
                             key=operator.attrgetter('name'))
        self._input_files = input_files
        if input_files:  # files of pre-step for comparison with pickled objects
            self._input_files = input_files
            self._cmd = input_dict["cmd"]
            self.init_hash = self.create_hash(self._cmd, self._input_files)

    @property
    def cmd(self):
        return self._cmd

    @property
    def input_files(self):
        return self._input_files

    def calc_hash(self, cmd, files):
        try:
            copy_cmd = copy.copy(cmd)
            copy_cmd.sort()
            string = self._id + "".join(copy_cmd + [s.calc_checksum() for s in files])
            cmd_hash = xxhash.xxh64(string, seed=1).hexdigest()
            return cmd_hash

        except TypeError:
            raise TypeError

    def create_hash(self, cmd, files):
        cmd_hash = self.calc_hash(cmd, files)
        fn = os.path.join(bioportainer.Config.config.cache_dir, cmd_hash)
        with open(fn, "wb") as f:
            pickle.dump(self, f)
        return cmd_hash

    def check_cache(self, cmd, cache_dir, logger, logger_name_override):
        cmd_hash = self.calc_hash(cmd, self._files)
        for path, dirs, files in os.walk(cache_dir):
            for f in files:
                if cmd_hash == f:
                    with open(os.path.join(path, f), "rb") as of:
                        obj = pickle.load(of)
                    check = True
                    for of in obj.files:
                        if not os.path.isfile(of.file_path):
                            check = False
                            break
                        if not of.check_checksum():
                            check = False
                            break

                    if check:
                        if logger:
                            logger.info("cmd: {}\nOutput files found, skip run for sample {} -- "
                                        "hash value: {}\n".format(" ".join(cmd), self.id, cmd_hash),
                                        extra={'name_override': logger_name_override})
                        return obj
                # else None

    @property
    def lock(self):
        return self._lock

    @lock.setter
    def lock(self, val):
        self._lock = val

    def with_lock(self, func):
        def wrapper(*args, **kwargs):
            if self.lock:
                with self.lock:
                    func()
            else:
                func(*args, **kwargs)
        return wrapper

    @property
    def id(self):
        return self._id

    @property
    def io_type(self):
        return self._io_type

    @property
    def files(self):
        return self._files

    @property
    def host_dir(self):
        return self._host_dir

    def __repr__(self):
        return "Sample_{}".format(self.id)

    def __str__(self):
        return ";".join({str(name) + ":" + str(attr) for name, attr in self.__dict__.items()
                         if not name.startswith("__")
                         and not callable(attr)
                         and not type(attr) is staticmethod})

    def __call__(self):
        return self

    def filter_files(self, regex):
        new = copy.deepcopy(self)
        [new.files.remove(f) for f in self.files if not re.match(regex, f.name)]
        try:
            new.cmd_hash = new.create_hash(new.cmd, new.files)
        except AttributeError:
            new.cmd_hash = new.create_hash(["None"], new.files)
        fn = os.path.join(bioportainer.Config.config.cache_dir, new.cmd_hash)
        with open(fn, "wb") as f:
            pickle.dump(new, f)

        return new

    @classmethod
    def from_container(cls, d, output_filter, out_dir, input_files):
        """
        intitilaize from container output
        :param d:
        :param output_filter:
        :param out_dir:
        :return: SampleIO instance
        """
        def add(p, f, outfiles):
            if not output_filter:
                outfiles.append(p)
            elif output_filter:
                if re.match(output_filter, f):
                    outfiles.append(p)

        out_files = []

        extensions = cls.get_extensions(d["type"])
        for path, dirs, files in os.walk(out_dir):
            for f in files:
                p = os.path.join(path, f)
                if extensions:
                    for ext in extensions:
                        if f.endswith(ext):
                           add(p, f, out_files)
                else:
                    add(p, f, out_files)
        d.update({"files": out_files})

        return cls(d, hostdir=out_dir, input_files=input_files)

    @classmethod
    def from_configfile(cls, yaml_dict):
        """
        Initialize from config file
        :param yaml_dict:
        :return: SampleIO instance
        """
        return cls(yaml_dict, hostdir=os.path.split(os.path.abspath(yaml_dict["files"][0]))[0])

    @classmethod
    def from_user(cls, id_, type_, files):
        """
        Init method for user input
        :param id_: Sample id
        :param type_: Sample type
        :param files: list of input files
        :return: SampleIO instance
        """
        files = [os.path.abspath(f) for f in files]
        d = {"id": id_, "type": type_, "files": files}

        return cls(d, hostdir=os.path.split(files[0])[0])

    @classmethod
    def from_func(cls, id_, type_, files):
        """
        Init method for user input
        :param id_: Sample id
        :param type_: Sample type
        :param files: list of input files
        :return: SampleIO instance
        """
        d = {"id": id_, "type": type_, "files": files}

        return cls(d, hostdir=os.path.split(files[0])[0])

    @staticmethod
    def get_extensions(file_type):
        """
        Returns valid extensions for each input type
        :param file_type:
        :return:
        """
        if file_type in ["fasta-pe", "fasta-se", "fasta-inter"]:
            return [".fa", ".fasta"]

        elif file_type in ["fasta-pe-gz", "fasta-se-gz", "fasta-inter-gz"]:
            return [".fa.gz", ".fasta.gz"]

        elif file_type in ["fasta-pe-bz", "fasta-se-bz", "fasta-inter-bz"]:
            return [".fa.bz2", ".fasta.bz2"]

        elif file_type in ["fastq-pe", "fastq-se", "fastq-inter"]:
            return [".fq", ".fastq"]

        elif file_type in ["fastq-pe-gz", "fastq-se-gz", "fastq-inter-gz"]:
            return [".fq.gz", ".fastq.gz"]

        elif file_type in ["fastq-pe-bz", "fastq-se-bz", "fastq-inter-bz"]:
            return [".fq.bz2", ".fastq.bz2"]

        elif file_type == "html":
            return [".html"]

        elif file_type == "bt2":
            return [".bt2"]

        elif file_type == "sam":
            return [".sam"]

        elif file_type == "bam":
            return [".bam"]

        elif file_type == "bai":
            return [".bam.bai"]

        elif file_type == "fastg":
            return [".fastg"]

        elif file_type == "gbk":
            return [".gbk", ".genebank"]

        elif file_type == "gff":
            return [".gff"]

        elif file_type == "sqn":
            return [".sqn"]

        elif file_type == "sco":
            return [".sco"]

        elif file_type == "txt":
            return [".txt", ".tab", ".tsv"]

        elif file_type == "out":
            return [".out"]

        elif file_type == "psltbl":
            return [".psltbl"]

        elif file_type == "bed":
            return [".bed"]

        elif file_type == "bcf":
            return [".bcf"]

        elif file_type == "bcf-bz":
            return [".bcf.bz"]
        elif file_type == "vcf":
            return [".vcf"]

        elif file_type == "vcf-gz":
            return [".vcf.gz"]

        elif file_type == "cram":
            return [".cram"]

        elif file_type == "mpi":
            return [".mpi"]

        elif file_type == "xml":
            return [".xml"]

        elif file_type == "svg":
            return [".svg"]

        elif file_type == "png":
            return [".png"]

        elif file_type == "jpg":
            return [".jpg"]

        else:
            return None

    def delete_files(self):
        """
        Deletes all files in SampleIO object
        :return:
        """
        import bioportainer.Config as Conf
        [os.remove(f.file_path) for f in self.files]
        subdir = os.path.join(os.path.split(os.path.split(self.host_dir)[0])[-1], self.id)
        [Conf.config.logger.info("File deleted: {}".format(f.name), extra={'name_override': subdir})
         for f in self.files]

    def move(self, directory_name):
        new_dir = list(Path(self.host_dir).parts)
        new_dir[-2] = directory_name
        new_dir = os.path.join(*new_dir)
        shutil.move(self.host_dir, new_dir)

        import bioportainer.Config as Conf
        for file in self.files:
            p_list = list(Path(file.file_path).parts)
            p_list[-3] = directory_name
            Conf.config.logger.info("File {} moved from {} to {} ".format(file.name, self.host_dir, new_dir),
                                    extra={'name_override': self.id})
        self._host_dir = new_dir

    def apply(self, function, *args, **kwargs):
        if stack()[1][3] == "parallel_apply":
            out = function(*args, **kwargs)
        else:
            out = function(self, *args, **kwargs)
        try:
            return self.from_func(self.id, self.io_type, out)
        except (AttributeError, FileNotFoundError):
            return out
