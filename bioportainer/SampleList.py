import bioportainer.SampleIO as Sio


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

    def filter_files(self, regex):
        new = [s.filter_files(regex) for s in Sio.copy.copy(self)]
        return new

    def delete_files(self):
        """
        Delete all files from SampleIO objects in list
        :return:
        """
        [s.delete_files() for s in self]

ContainerIO = SampleList
