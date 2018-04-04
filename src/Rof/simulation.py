
import os
import re
import subprocess
from collections import deque

from .PyParseVTK import VTK_File


class Simulation(object):
    """
        Class to control simulation and postprocessing

    """
    def __init__(self, case_object, alias):
        self.case_object = case_object
        self.alias = alias
        self.run_container = dict()
        self._limit_write = 0

    @property
    def limit_write(self):
        return self._limit_write

    @limit_write.setter
    def limit_write(self, value):
        self._limit_write = value

    def _execute(self, command):
        """
            Execute commands. Uses an alias to get aliases used by OpenFOAM.
        :param command: command to execute
        :return: string. Standard output of command execution
        """
        p = subprocess.Popen("/bin/bash -i -c '{} && {}'".format(self.alias, command), stdout=subprocess.PIPE, shell=True)
        out = p.stdout.read().decode()

        return out

    def _write_log(self, out,command):
        """
        Write a log
        :param out: console output
        :param command: command
        :return:
        """
        f = open(os.path.join(self.case_object.case_dir,r"{}.log".format(command)), 'w')
        f.write(out)
        f.close()

    def block_mesh(self, string=None, path=None):
        """
            Create blockMeshDict from string or from file at another path.Then execute OpenFOAM command "blockMesh"
        :param string: string with blockMeshDict format
        :param path: path to a blockMesh file
        """
        if string:
            copy_path = os.path.join(self.case_object.case_dir, r'system', r'blockMeshDict')
            f = open(copy_path, 'w')
            f.write(string)
            f.close()
        elif path:
            copy_path = os.path.join(self.case_object.case_dir, r'system', r'blockMeshDict')
            os.system('cp {} {}'.format(path, copy_path))

        out = self._execute('blockMesh -case {}'.format(self.case_object.case_dir))
        self._write_log(out, 'blockMesh')

    def check_mesh(self):
        """
            Command of OpenFOAM "checkMesh"
        :return: True or False. True: Mesh OK.
                                False: Mesh failed.
        :rtype: bool
        """
        out = self._execute('checkMesh -case {}'.format(self.case_object.case_dir))
        self._write_log(out, "checkMesh")
        if len(re.findall(".*Mesh OK.*", out))>0:
            print('Mesh OK')
            return True
        else:
            print('Mesh failed, see {}/checkMesh.log for more information'.format(self.case_object.case_dir))
            return False

    def paraFoam(self, args=("",)):
        """
            Command of OpenFOAM "paraFoam"
        :param args: list or tuple. Contains arguments like command line options.
                     Example:  args=("-block",) ----------> paraFoam -block .......
        """
        args_string = ''
        for i in args:
            args_string+=i
        out = self._execute('paraFoam {} -case {}'.format(args_string, self.case_object.case_dir))
        self._write_log(out, 'paraFoam')

    def run(self, func=lambda x, y: False, args=None):
        """
            Run simulation.
                -If case.interacting() was called, the simulation stops and writes the results for each
                iterations (passed to case.interacting), and then execute :param func.

                -If case.interacting() was not called, the simulation stops at time indicated by controlDict. If want
                execute a function at the end of simulation this function MUST return True.

        :param func: function to execute at the end of each simulation. If returns True simulation stops.
                     Two arguments are passed to this function. -First:  a container to save variables between simulations
                                                                -Second: args passed to Simulation.run()
        :param args: whatever wants
        :return: 
        """
        is_right = False
        self.run_container = dict()
        time_deque = deque()
        while not is_right:
            out = self._execute('{} -case {}'.format(self.case_object.method,self.case_object.case_dir))
            self._write_log(out, '{}'.format(self.case_object.method))
            if self.limit_write:
                for i in list(os.walk(self.case_object.case_dir))[0][1]:
                    result = re.findall('([0-9].*\..*)', i)

                    if len(result)>0 and result[0] not in time_deque:
                        if len(time_deque) >= self.limit_write:
                            remove_item = time_deque.popleft()
                            os.system('rm -r {}/{}'.format(self.case_object.case_dir, remove_item))
                        self.run_container['current_time'] = i
                        time_deque.append(i)
                        break
            is_right = func(self.run_container, args)
        print('Simulation end')

    def foamToVTK(self, args=("-ascii",)):
        """
            Command of OpenFOAM "foamToVTK"
        :param args: list or tuple. Contains arguments like command line options.
                    Example:    args=("-ascii",) ----------------> foamToVTK -ascii .....
                                args=("-ascii","-latestTime") ---> foamToVTK -ascii -latestTime ......
        :return:
        """
        args_string = ''
        for i in args:
            args_string+=i+' '
        out = self._execute('foamToVTK {} -case {}'.format(args_string, self.case_object.case_dir))
        self._write_log(out, 'foamToVTK')

    def _get_last_VTK(self):
        """
            Get last iteration number of vtk files indexing.
        :return:
        """
        current = 0
        for i in list(os.walk(os.path.join(self.case_object.case_dir, 'VTK')))[1][2]:
            iteration = re.findall('.*_(.*).vtk', i)[0]
            if int(iteration) >= current:
                current = int(iteration)

        return current

    def get_last_results(self, patch):
        """

            Get a parsed results from vtk files.

            Before calling this method, MUST call foamToVTK to create vtk files

        :param patch: patch's name
        :return: VTK_File object
        """
        last_time = self._get_last_VTK()
        path_file = os.path.join(self.case_object.case_dir,'VTK', patch, "{}_{}.vtk".format(patch, last_time))
        return VTK_File(path_file)

    def not_implemented_command(self, command, args=('',)):
        command_string = command + " -case {}".format(self.case_object.case_dir)
        for i in args:
            command += " "+i
        self._write_log(self._execute(command_string), command)
