import bioportainer.ContainerBase as Cont
import psutil
from bioportainer.Config import config
from inspect import signature


class MultiCmdContainer(Cont.Container):
    """
    Abstract Base Class for dockerfiles with sub commands
    """
    def __init__(self, image, image_directory, sub_commands, input_allowed):
        super().__init__(image, image_directory, input_allowed)
        self.subcommands = sub_commands
        self.assert_subcmd_impl()

    def assert_subcmd_impl(self):
        """
        checks if all sub command methods are implemented at init
        :return:
        """
        for scmd in self.subcommands:
            method = "set_" + scmd.replace("-", "_") + "_params"
            if method not in dir(self):
                raise NotImplementedError("{} not implemented".format(method))
            else:
                method_to_call = getattr(self, method)
                method_to_call()

    def get_opt_params(self, param_attr):
        """
        return optional parameter dictionary as parameter-string-list
        :param param_attr: string: "get_<sub command>_params"
        :return: list of strings
        """
        p = getattr(self, param_attr)
        l = []
        for k, v in p.items():
            if v == "threads":
                v = str(config.container_threads)
            if v == "max_availiable_g":
                v = "{:.0f}".format(
                int((psutil.virtual_memory().available / 1024 ** 3) / config.threads))
            if v == "max_availiable_m":
                v = "{:.0f}".format(
                int((psutil.virtual_memory().available / 1024 ** 2) / config.threads))
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
        decorator function for set_<sub command>_params methods
        :param func: "set_<sub command>_params"
        :return: wrapped function
        """
        @Cont.wraps(func)
        def wrapper(*args, **kwargs):
            def return_func(*args, **kwargs):
                sig = signature(func).parameters.values()
                sub_cmd = func.__name__[4:].replace("-", "_")
                c = args[0]
                kwags = {p.name: p.default for p in sig if p.default is not p.empty}
                for k, v in kwargs.items():
                    kwags[k] = v
                setattr(c, sub_cmd, kwags)
                func(*args, **kwargs)

                return c

            return return_func(*args, **kwargs)

        return wrapper

