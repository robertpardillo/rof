
import os
import re
import xml.etree.ElementTree as ET
from collections import namedtuple

import platform
commands = __import__('miscellaneous.os_commands',globals(), locals(), level=2)
commands = commands.__dict__['os_commands'].__dict__[platform.system()]


class SuperTemplate(object):

    def __init__(self, name, method):
        self.name = name
        self.method = method
        self.abs_path = os.path.join(os.path.abspath(''),'{}'.format(self.name))
        try:self.default_values()
        except:pass

    def create(self):
        """

            Attention, implementation ruled by the way that it works, (virtual box, linux or windows)

        :return:
        """
        #TODO

        ending = '// ************************************************************************* //\n'
        self.template += ending
        abs_path = os.path.join(os.path.abspath(''), r'{}'.format(self.name))
        f = open(abs_path, 'w')
        f.write(self.template)
        f.close()

        os.system(r'{} {} {}'.format(commands['cp'],abs_path, self.copy_path))
        os.system(r'{} {}'.format(commands['rm'], abs_path))

    def build_file(self):
        # First default

        __dict__0 = self.__dict__.copy()
        for i in __dict__0:
            result = re.findall('f_(.*)', i)
            if len(result) > 0:

                index_0 = __dict__0[i]
                if index_0[1]:
                    continue
                elif not index_0[1]:
                    self.template += '{}'.format(result[0])
                # Perhaps fail with some templates ###############################################################
                if isinstance(index_0[0], dict):
                    if isinstance(index_0[0], dict):
                        sep_i = '{'
                        sep_f = '}'
                    self.template += '\n{}\n'.format(sep_i)
                    for j in index_0[0]:
                        if isinstance(index_0[0][j], dict):
                            self.template += '\t{}\n'.format(j)
                            self.template += '\t{\n'
                            for k in index_0[0][j]:
                                self.template += '\t\t{}\t{};\n'.format(k, index_0[0][j][k])
                            self.template += '\t}\n'
                        else:
                            self.template += '\t{}\t{};\n'.format(j, index_0[0][j])
                    self.template += '{}\n'.format(sep_f)
                    index_0[1]=True
                    self.__setattr__(i, index_0)
                elif isinstance(index_0[0], list):
                    self.template += '(\n'
                    for i in index_0[0]:
                        self.template += '\t{\n'
                        for j in i:
                            if isinstance(i[j], dict):
                                self.template += '\t{}\n'.format(j)
                                self.template += '\t{\n'
                                for k in i[j]:
                                    self.template += '\t\t{}\t{};\n'.format(k, i[j][k])
                                self.template += '\t}\n'
                            else:
                                self.template += '\t{}\t{};\n'.format(j, i[j])
                        self.template += '\t}\n'
                    self.template += ')\n'
                else:
                    self.template += '\t{};\n'.format(index_0[0])
                    index_0[1] = True
                    self.__setattr__(i, index_0)

    def set_field(self, name, value):
        #value = self.format_field(value, False)
        value = [value, False]
        self.__setattr__('f_{}'.format(name), value)

    def default_values(self):
        from ..definitions import PYPARFOAM_DIR
        methods_path = os.path.join(PYPARFOAM_DIR, 'pyParFoam', 'methods_xml', '{}.xml'.format(self.method))
        root = ET.parse(methods_path).getroot()
        root2 = root.find('_'+self.case_dir).find(self.name)
        if not root2:
            return 0
        for i in root2:
            if i.get('dict'):
                field_name = i.tag
                field_dict = dict()
                for j in i:
                    if j.get('dict'):
                        sub_field_dict = dict()
                        for k in j:
                            if k.get('real'):
                                tag = k.get('real')
                            else:
                                tag = k.tag
                            sub_field_dict[tag] = k.text
                        if j.get('real'):
                            tag = j.get('real')
                        else:
                            tag = j.tag
                        field_dict[tag] = sub_field_dict
                    else:
                        if j.get('real'):
                            tag = j.get('real')
                        else:
                            tag = j.tag
                        field_dict[tag] = j.text
                self.set_field(field_name, field_dict)
            else:
                self.set_field(i.tag, i.text)







