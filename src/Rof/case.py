
import os
import xml.etree.ElementTree as ET
import re

import platform
from .simulation import Simulation

commands = __import__('miscellaneous',globals(), locals(), ['os_commands'], level=1)
commands = commands.__dict__['os_commands'].__dict__[platform.system()]


class Case(object):
    """
        Class to build case files.
        This class build all the files except which related to mesh.

        ATTENTION: AFTER CALLING "build_files" OR "simulation" ANY CHANGE CAN NOT BE DONE TO THIS FILES.

        Way to change this files:
            case_object.file_nameOfFile.setField('field_to_change', values)

            Examples:
                -Changing U boundary conditions:
                    case.file_U.set_field('boundaryField',{'inlet': {'type': 'fixedValue',value': 'uniform (20 20 0)'},
                                                             'outlet': {'type': 'zeroGradient'},
                                                             'cyclic_in_1': {'type': 'cyclic'},
                                                             'cyclic_in_2': {'type': 'cyclic'},
                                                             'cyclic_out_1': {'type': 'cyclic'},
                                                             'cyclic_out_2': {'type': 'cyclic'}})

                -Changing p initial internal value:
                    case.file_p.set_field('internalField', 'uniform 23456')

                -Changing controlDict:
                    case.file_controlDict.set_field('endTime', '10000')

                -Changing turbulenceProperties:
                    case.file_turbulenceProperties.set_field('simulationType', 'laminar')

    """
    def __init__(self,path,method):
        """

        Allowed methods:
            - icoFoam
            - rhoCentralFoam
            - rhoSimpleFoam
            - simpleFoam
            - sonicFoam

        :param path: path to case
        :type: str
        :param method: standard method
        :type: str
        """
        self.case_dir = path
        self.method = method
        if os.path.exists(self.case_dir):
            pass
        else:
            os.system(r'{} {}'.format(commands['mkdir'], self.case_dir))
            os.system(r'{} {}'.format(commands['mkdir'], os.path.join(self.case_dir,'0')))
            os.system(r'{} {}'.format(commands['mkdir'], os.path.join(self.case_dir,'constant')))
            os.system(r'{} {}'.format(commands['mkdir'], os.path.join(self.case_dir,'system')))

        from .definitions import PYPARFOAM_DIR
        xml_path = os.path.join(PYPARFOAM_DIR ,'pyParFoam','methods_xml','{}.xml'.format(method))
        root1 = ET.parse(xml_path).getroot()
        copy_path = self.case_dir
        for i in root1:
            res = re.findall('_(.*)', i.tag)[0]
            copy_path_0 = os.path.join(copy_path, '{}'.format(res))
            for j in i:
                folder = __import__('pyParFoam.foam_templates.{}_templates.temp_{}'.format(res, j.tag, j.tag), globals(), locals(), ['{}'.format(j.tag)], level=1)
                template_class = folder.__dict__['{}'.format(j.tag)]
                file = template_class(method, os.path.join(copy_path_0,'{}'.format(j.tag)))
                self.__setattr__('file_{}'.format(j.tag), file)

    def build_files(self):
        """
            Build all the files.

             ATTENTION: AFTER CALLING ANY CHANGE CAN NOT BE DONE TO THIS FILES.

        """
        for i in self.__dict__:
            if len(re.findall('file_.*', i))==0:
                pass
            else:
                self.__getattribute__(i).build_file()
                self.__getattribute__(i).create()

    def interacting(self, iterations):
        """

        Converts the simulation into an interactive simulation. Allowing parse results, analyse and stop or continue.

        :param iterations: time steps to stop the simulation and write results
        :return:
        """
        self.file_controlDict.set_field('startFrom', 'latestTime')
        self.file_controlDict.set_field('stopAt', 'nextWrite')
        self.file_controlDict.set_field('writeControl','timeStep')
        self.file_controlDict.set_field('writeInterval','{}'.format(iterations))

    def simulation(self, alias=None):
        """
            Get the Simulation object.

            ATTENTION: BEFORE CALLING ANY CHANGE CAN NOT BE DONE TO THIS FILES.
        :param alias: Alias to allow commands of OpenFOAM
        :type alias: str
        :return: Simulation object
        :rtype: :class:`Rof.simulation.Simulation`
        """
        self.build_files()
        if not alias:alias=""
        return Simulation(self, alias)

    def add_file(self, local_path,name, string=""):
        """
        Add a file to the case.

        Allowed files through template:
            +------------+----------------------------+
            | local_path |          name              |
            +------------+----------------------------+
            |     0      |          alphat            |
            |            |          epsilon           |
            |            |            k               |
            |            |           nut              |
            |            |           nuTilda          |
            |            |            p               |
            |            |            T               |
            |            |            U               |
            +------------+----------------------------+
            |  constant  |  thermophysicalProperties  |
            |            |     transportProperties    |
            |            |   turbulenceProperties.py  |
            +------------+----------------------------+
            |  system    |      controlDict           |
            |            |      fvSchemes             |
            |            |      fvSolutions           |
            |            |      topoSetDict           |
            +------------+----------------------------+

        If the string is filled, a new file without template will be built.

        Example:
            - add_file('0', 'alphat') --> a file with the template pyParFoam.foam_templates.0_templates.temp_alphat is built

            -add_file('system', 'test_file', 'string of new file') --> 'test_file' will be created in folder 'system' with
                                                                        'string of new file'


        :param local_path: path inside case structure
        :type local_path: str
        :param name: file's name
        :type name: str
        :param string: new file string
        :type string: str
        """
        if string=="":
            folder = __import__('pyParFoam.foam_templates.{}_templates.temp_{}'.format(local_path, name), globals(),
                                locals(), ['{}'.format(name)], level=1)
            template_class = folder.__dict__['{}'.format(name)]
            copy_path_0 = os.path.join(self.case_dir, '{}'.format(local_path))
            file = template_class(self.method, os.path.join(copy_path_0, '{}'.format(name)))
            self.__setattr__('file_{}'.format(name), file)
        else:
            folder = __import__('pyParFoam.superTemplate'.format(local_path, name), globals(),
                                locals(), ['SuperTemplate'], level=1)
            superTemplate = folder.__dict__['SuperTemplate']
            copy_path_0 = os.path.join(self.case_dir, '{}'.format(local_path))
            file = superTemplate(name, self.method)
            file.template=string
            file.copy_path = copy_path_0
            self.__setattr__('file_{}'.format(name), file)
