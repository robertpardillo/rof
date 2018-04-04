
from ...superTemplate import SuperTemplate


class U(SuperTemplate):
    template = r'''
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
    class       volVectorField;
    object      U;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //    
'''

    def __init__(self, method, copy_path):
        self.copy_path = copy_path
        self.case_dir = r'0'
        super(U, self).__init__('U', method)

"""
u.set_field('boundaryField', {'inlet': {'type': 'freestream', 'freestreamValue': 'uniform (0 0 0)'},
                              'outlet': {'type': 'freestram', 'freestreamValue': 'uniform (0 0 0)'},
                              'profile': {'type': 'noSlip'},
                              'top_down': {'type': 'empty'},
                              'inlet_cyclic_1': {'type': 'noSlip'},
                              'inlet_cyclic_2': {'type': 'noSlip'},
                              'outlet_cyclic_1': {'type': 'noSlip'},
                              'outlet_cyclic_2': {'type': 'noSlip'}})
"""

