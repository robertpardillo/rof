
from ...superTemplate import SuperTemplate


class p(SuperTemplate):
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
    class       volScalarField;
    object      p;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
'''

    def __init__(self, method, copy_path):
        self.case_dir = r'0'
        self.copy_path = copy_path
        super(p, self).__init__('p', method)

"""
ps.set_field('boundaryField', {'inlet': {'type': 'freestreamPressure'},
                               'outlet': {'type': 'freestreamPressure'},
                               'profile': {'type': 'zeroGradient'},
                               'top_down': {'type': 'empty'},
                               'inlet_cyclic_1': {'type': 'zeroGradient'},
                               'inlet_cyclic_2': {'type': 'zeroGradient'},
                               'outlet_cyclic_1': {'type': 'zeroGradient'},
                               'outlet_cyclic_2': {'type': 'zeroGradient'}})
"""
