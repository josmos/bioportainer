from abc import abstractmethod

import bioportainer.ContainerBase as Cont
from inspect import signature
import bioportainer.Config


class SingleCmdContainer(Cont.Container):
    """
    Abstract Base Class for Tools with single command
    """
    def __init__(self, image, image_directory, input_type, output_type):
        super().__init__(image, image_directory, input_type)
        self._output_type = output_type
        self.opt_params = {}
        #self.set_opt_params()

    def get_opt_params(self):
        """
        return optional parameter dictionary as parameter-string-list
        :return: list of strings
        """
        l = []
        for k, v in self.opt_params.items():
            if v == "threads":
                v = str(bioportainer.Config.config.container_threads)
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

    @staticmethod
    def impl_set_opt_params(func):
        """
        decorator function for set_opt_params method in child class
        :param func: set_opt_params
        :return:
        """
        @Cont.wraps(func)
        def wrapper(*args, **kwargs):
            def return_func(*args, **kwargs):
                sig = signature(func).parameters.values()
                c = args[0]
                kwags = {p.name: p.default for p in sig if p.default is not p.empty}
                for k, v in kwargs.items():
                    kwags[k] = v
                setattr(c, "opt_params", kwags)
                func(*args, **kwargs)

                return c

            return return_func(*args, **kwargs)

        return wrapper

    @abstractmethod
    def set_opt_params(self):
        raise NotImplementedError("Must be overridden in child class")

    @abstractmethod
    def run(self, sample_io):
        raise NotImplementedError("Must be overridden in child class")

    @abstractmethod
    def run_parallel(self, *args):
        raise NotImplementedError("Must be overridden in child class")