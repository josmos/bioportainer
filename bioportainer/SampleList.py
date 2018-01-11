import bioportainer.SampleIO as Sio
from multiprocessing import Pool
from functools import partial


class SampleList(list):
    """
    List of SampleIO objects
    """
    def __init__(self, samples):
        list.__init__(self)
        [self.append(s) for s in samples]

    @classmethod
    def from_container(cls, samples):
        """
        Init from container.parallel_run output
        :param samples: list of SampleIO instances
        :return: SampleList object
        """
        return cls(samples)

    @classmethod
    def from_configfile(cls, configfile):
        """
        Init from configfile
        :param configfile: yaml dict from configfile
        :return: SampleList object
        """
        samples = [Sio.SampleIO.from_configfile(s) for s in configfile.get("Samples")]
        return cls(samples)

    @classmethod
    def from_user(cls, id_, type_, files, n):
        s = Sio.SampleIO.from_user(id_, type_, files)
        samples = [s] * n
        return cls(samples)

    def filter_files(self, regex):
        new = [s.filter_files(regex) for s in Sio.copy.copy(self)]
        return self.from_container(new)

    def delete_files(self):
        """
        Delete all files from SampleIO objects in list
        :return:
        """
        try:
            [s.delete_files() for s in self]
        except FileNotFoundError:
            pass

    def move(self, directory_name):
        new = [s.move(directory_name) for s in Sio.copy.copy(self)]
        return new

    def parallel_apply(self, function, *args, **kwargs):
        filelist = []
        for sample in self:
            out = sample.apply(partial(function, *args, **kwargs))
            filelist.append(out)
        return self.from_container(filelist)

ContainerIO = SampleList

