
import re


class VTK_File(object):
    """
        Utility for parse VTK files
    """
    def __init__(self, file):
        self.name = file
        self._parse()

    def _parse(self):
        self._fix_lines = [1, 4]


        self._buffer = -1
        self._buffer_field = -1

        f = open(self.name, 'r')

        fields = dict()
        broke_fields = ['ASCII', 'DATASET', 'POINTS', 'POLYGONS', 'CELL_DATA', 'POINT_DATA']

        current_field = fields
        field_data = []

        while True:
            if self._buffer == 130:
                pass
            text = self._read_line(f)
            field = self._is_a_field(text)
            if self._buffer == self._fix_lines[0]:
                self.patch = text
            elif field[0]:
                field_name = field[1][0]

                try:
                    if len(field_data) > 0:
                        field_dict['DATA'] = field_data
                except:
                    pass
                field_dict = dict()
                if field_name in broke_fields:
                    current_field = fields
                    current_field[field_name] = field_dict
                    field_dict['PARAMETERS'] = field[1][1:]
                    current_field = field_dict
                elif not field[2]:
                    super_dict[field_name] = field_dict
                    field_dict['PARAMETERS'] = field[1][1:]
                elif field[2]:
                    super_dict = current_field
                    current_field[field_name] = field_dict
                    field_dict['PARAMETERS'] = field[1][1:]
                    current_field = field_dict
                field_data = list()
            elif not field[0]:
                field_data += text.replace('\n', '').split(' ')
            if text == '':
                field_dict['DATA'] = field_data
                self.fields = fields
                f.close()
                break

    def _read_line(self, f):
        self._buffer += 1
        return f.readline()

    def _is_a_field(self, text):
        if len(re.findall('^([A-Z]*[a-z]*)', text)[0]) > 0:
            params = re.findall('(.*)[ (.*)]*', text)[0].split(' ')
            _super = False
            if self._buffer_field + 1 == self._buffer:
                _super = True
            self._buffer_field = self._buffer
            return [True, params, _super]

        return [False, None, None]

    def GetCellData(self, *field):
        """
            Get field data from cells
        :param field: list of fields (U,p,T ...)
        :return: list
        """
        if len(field)>0:
            _fields = self.fields['CELL_DATA']['FIELD'][field[0]]
            vector_len = _fields['PARAMETERS'][0]
            data_len = _fields['PARAMETERS'][1]
            data = list()
            for i in range(int(data_len)):
                data.append([])
                for j in range(int(vector_len)):
                    data[-1].append(_fields['DATA'][i*int(vector_len)+j])
            return data
        else:
            return self.fields['CELL_DATA']['FIELD']

    def GetPointData(self, *field):
        """
            Get field data from points
        :param field: list of fields (U,p,T ...)
        :return: list
        """
        if len(field)>0:
            _fields = self.fields['CELL_DATA']['FIELD'][field[0]]
            vector_len = _fields['PARAMETERS'][0]
            data_len = _fields['PARAMETERS'][1]
            data = list()
            for i in range(int(data_len)):
                data.append([])
                for j in range(int(vector_len)):
                    data[-1].append(_fields['DATA'][i * int(vector_len) + j])
            return data
        else:
            return self.fields['POINT_DATA']['FIELD']

    def GetPoints(self):
        """
            Get points coord.
        :return: list
        """
        _fields = self.fields['POINTS']
        vector_len = 3
        data_len = _fields['PARAMETERS'][0]
        data = list()
        for i in range(int(data_len)):
            data.append([])
            for j in range(int(vector_len)):
                data[-1].append(_fields['DATA'][i * int(vector_len) + j])
        return data

    def GetPolygons(self):
        """
            Get polygons.
        :return: list
        """
        _fields = self.fields['POLYGONS']
        vector_len = _fields['PARAMETERS'][0]
        data_len = _fields['PARAMETERS'][1]
        data = list()
        rest = int(int(data_len)/int(vector_len))
        for i in range(rest):
            data.append([])
            for j in range(int(vector_len)):
                data[-1].append(_fields['DATA'][i * int(vector_len) + j])
        return data

