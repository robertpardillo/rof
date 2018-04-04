
from ...superTemplate import SuperTemplate


class nuTilda(SuperTemplate):
    template=r'''
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  4.1                                   |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      nuTilda;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
'''

    def __init__(self, method, copy_path):
        self.case_dir = r'0'
        self.copy_path = copy_path
        super(nuTilda, self).__init__('nuTilda', method)

"""
nuT.set_field('boundaryField', {'inlet': {'type': 'freestream', 'freestreamValue':'uniform 0.14'},
                               'outlet': {'type': 'freestreamPressure', 'freestreamValue':'uniform 0.14'},
                               'profile': {'type': 'fixedValue', 'value':'uniform 0'},
                               'top_down': {'type': 'empty'},
                               'inlet_cyclic_1': {'type': 'fixedValue', 'value':'uniform 0'},
                               'inlet_cyclic_2': {'type': 'fixedValue', 'value':'uniform 0'},
                               'outlet_cyclic_1': {'type': 'fixedValue', 'value':'uniform 0'},
                               'outlet_cyclic_2': {'type': 'fixedValue', 'value':'uniform 0'}})
"""

