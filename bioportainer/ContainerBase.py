import distutils.dir_util
import os
import time
import uuid
from abc import ABCMeta
from functools import wraps, partial
from inspect import stack
from multiprocessing import Pool, Manager

import bioportainer.Config as Conf
import bioportainer.SampleIO as Sio
import docker
from requests.exceptions import HTTPError

import bioportainer.SampleList as Cio
from bioportainer import config


class Container(metaclass=ABCMeta):
    """
    Metaclass inherited by SingleCmcContainer and MultiCmdContainer
    """
    def __init__(self, image, image_directory, input_allowed, output_filer=None):
        """
        :param image: <registry/name:tag>
        :param image_directory: path within module
        :param input_allowed: default file format for input
        :param output_type: default file format for output
        :param output_filer: regex for filtering output files or None
        """
        self._image_on_client = False
        self._image = image
        self._image_directory = image_directory
        self._change_out_err_log = False
        self._container_dir = os.path.split(image.split("/")[-1].replace(":", "_v"))[-1]
        self._output_filter = output_filer
        self._out_dir = None
        self._input_allowed = input_allowed
        self._output_type = ""
        self._cmd = []

    def check_image(self, obj):
        if not self._image_on_client:
            print("Looking for {} image on client...".format(obj.image), end="")
            try:
                config.client.images.get(obj.image)
                print("done!")
                self._image_on_client = True

            except docker.errors.ImageNotFound:
                print("not found!\nTry pulling {} from biocontainers registry...".format(obj.image), end="")

                try:
                    config.client.images.pull(obj.image.split(":")[0], tag=obj.image.split(":")[1])
                    print("done!")
                    self._image_on_client = True

                except docker.errors.ImageNotFound:

                    print("not found!\nTry to build image from dockerfile...", end="")
                    try:

                        dockerfiledir = os.path.join(os.path.dirname(__file__), obj._image_directory)
                        Conf.config.client.images.build(path=dockerfiledir, tag=obj.image, rm=True)
                        print("done!")
                        self._image_on_client = True
                    except HTTPError:
                        print("not found!")
                        self._image_on_client = False
                    except docker.errors.BuildError:
                        print("Build failed!")
                        self._image_on_client = False

    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, val):
        self._out_dir = val

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, val):
        self._cmd = val

    @property
    def image(self):
        return self._image

    @property
    def input_allowed(self):
        return self._input_allowed

    @input_allowed.setter
    def input_allowed(self, val):
        self._input_allowed = val

    def set_input_type(self, val):
        """
        chained method for setting input_type by user
        :param val:
        :return:
        """
        self.input_type = val
        return self

    @property
    def output_type(self):
        return self._output_type

    @output_type.setter
    def output_type(self, val):
        self._output_type = val

    def set_output_type(self, val):
        """
        chained method for setting output_type by user
        :param val:
        :return:
        """
        self.output_type = val
        return self

    @property
    def container_sample_dir(self):
        return self._container_sample_dir

    @container_sample_dir.setter
    def container_sample_dir(self, val):
        self._container_sample_dir = val

    @property
    def host_dir(self):
        return self._host_dir

    @host_dir.setter
    def host_dir(self, val):
        self._host_dir = val

    @property
    def container_dir(self):
        return self._container_dir

    @container_dir.setter
    def container_dir(self, val):
        self._container_dir = val

    @property
    def output_filter(self):
        return self._output_filter

    @output_filter.setter
    def output_filter(self, regex):
        self._output_filter = regex

    def set_output_filter(self, regex):
        """
        chained method for setting output_filter by user
        :param regex:
        :return:
        """
        self.output_filter = regex
        return self

    @property
    def change_out_err_log(self):
        """
        switch stdout/stderr for container logs
        :return:
        """
        return self._change_out_err_log

    @change_out_err_log.setter
    def change_out_err_log(self, value):
        self._change_out_err_log = value

    def container_logs(self, cont):
        """

        :param cont:
        :return:
        """
        if Conf.config.logger:
            flag = True
            while flag:
                time.sleep(1)
                cont.reload()
                if cont.status == "exited":
                    if self.change_out_err_log:
                        out = cont.logs(stdout=False, stderr=True).decode()
                        err = cont.logs(stdout=True, stderr=False).decode()
                    else:
                        out = cont.logs(stdout=True, stderr=False).decode()
                        err = cont.logs(stdout=False, stderr=True).decode()
                    Conf.config.logger.info(
                        "cmd: " + " ".join(self.cmd) + "\n" + out.replace("\n", "\n\t"),
                        extra={'name_override': self.image})
                    if err != "":
                        Conf.config.logger.error(err.replace("\n", "\n\t"),
                                                 extra={'name_override': self.image})
                    cont.remove()  # delete container if finished
                    flag = False

    def make_volumes(self, sample_io, others, mountfiles):
        if not os.path.exists(self.out_dir):  # create output directory
            sample_io.with_lock(distutils.dir_util.mkpath(self.out_dir))
        v = {sample_io.host_dir: {"bind": "/data1/", "mode": "ro"},
             self.out_dir: {"bind": "/data/", "mode": "rw"}}
        fp = os.path.join(self.out_dir, "init.sh")  # entry script
        dir_nr = 1
        with open(fp, "w") as init:
            for i, arg in enumerate(others):
                dir_nr = dir_nr + i + 1
                v[arg.host_dir] = {"bind": "/data{}/".format(dir_nr), "mode": "ro"}

            if mountfiles:
                for i, filepath in enumerate(mountfiles):
                    path, file = os.path.split(filepath)
                    dir_nr = dir_nr + i + 1
                    v[path] = {"bind": "/data{}/".format(dir_nr), "mode": "ro"}

            init.write("""#!/usr/bin/env bash
for path in /data*; do
    [ -d "${{path}}" ] || continue # if not a directory, skip
    [ "${{path}}" != "/data" ] || continue # skip /data itself
    ln -s ${{path}}/* /data/
done
{}
busybox &>/dev/null
retVal=$?
if [ $retVal -eq 0 ]; then
    find /data/. -type l -exec rm {{}} +
else
    find -type l -delete
fi
""".format(" ".join(self.cmd)))

        # set permissions for entry script:
        mode = os.stat(fp).st_mode
        mode |= (mode & 0o444) >> 2  # copy R bits to X
        os.chmod(fp, mode)

        return v

    @staticmethod
    def impl_run(func):
        """
        decorator function for "run" method
        (overriding signature and adding context)
        :param func: run
        :return: wrapped func
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            cnf = Conf.config
            try:
                args_unpacked = (args[0],) + args[1]
                io_list = args[1]
            except TypeError:  # if not called from run_parallel
                args_unpacked = args
                io_list = args[1:]

            sample_io, * others = [x for x in io_list if x is not None]

            c = args[0]
            c.container_sample_dir = os.path.join(c.container_dir, sample_io.id)
            c.out_dir = os.path.join(cnf.work_dir, c.container_dir, sample_io.id)
            try:
                mountfiles = kwargs["mount"]

            except KeyError:
                mountfiles = None

            func(*args_unpacked, **kwargs)

            out = sample_io.check_cache(c.cmd, cnf.cache_dir, cnf.logger, c.image)
            if not out:
                c.check_image(c)
                v = c.make_volumes(sample_io, others, mountfiles)
                name = uuid.uuid4()
                log = cnf.client.containers.run(c.image, user=os.getuid(), detach=True, name=name,
                                                volumes=v, working_dir="/data/", entrypoint="./init.sh")
                c.container_logs(log)
                container_dict = {"id": sample_io.id, "type": c.output_type, "cmd": c.cmd}
                os.remove(os.path.join(c.out_dir, "init.sh"))
                out = Sio.SampleIO.from_container(container_dict, c.output_filter, c.out_dir,
                                                  sample_io.files)

            if stack()[1][3] == "mapstar":
                return c, out  # return "self" if called from run parallel
            else:
                return out

        return wrapper

    @staticmethod
    def impl_run_parallel(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            starting <threads> dockerfiles.runs parallel
            :param sample_list: SampleList object with input files
            :param threads: number of dockerfiles to start parallel
            :param subcmd: sub command string (None if SingleCmdContainer)
            :return: SampleList object with output files
            """
            try:
                threads = kwargs["threads"]
                del kwargs["threads"]
            except KeyError:
                threads = Conf.config.threads
            try:
                subcmd = kwargs["subcmd"]
                del kwargs["subcmd"]
            except KeyError:
                subcmd = None

            def ret_func(*args, subcmd=subcmd, **kwargs):
                c = args[0]
                s_length = [len(arg) for arg in args[1:] if arg][0]  # eventually change condtition to check types
                args = [[None] * s_length if a is None else a for a in args[1:]]
                # make iterable of nontypes for zip if argument is None
                sample_io_list = list(zip(*args))
                pool = Pool(threads)
                lock = Manager().Lock()
                c.check_image(c)
                queue = Manager().Queue()
                for sample_io in sample_io_list:
                    try:
                        [setattr(s, "lock", lock) for s in sample_io]
                        [setattr(s, "queue", queue) for s in sample_io]
                    except AttributeError:
                        pass
                if subcmd:

                    cont_list = pool.map(partial(c.run, subcmd=subcmd, **kwargs), sample_io_list)
                else:
                    cont_list = pool.map(partial(c.run, **kwargs), sample_io_list)
                new_obj = cont_list[0][0]
                c.__dict__.update(new_obj.__dict__)
                cont_io = Cio.SampleList.from_container([t[1] for t in cont_list])
                pool.close()
                pool.join()

                return cont_io

            return ret_func(*args, subcmd=subcmd, **kwargs)

        return wrapper
