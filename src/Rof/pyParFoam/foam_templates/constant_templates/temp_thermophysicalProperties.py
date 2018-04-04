
from ...superTemplate import SuperTemplate


class thermophysicalProperties(SuperTemplate):
    template=r"""
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
    class       dictionary;
    location    "constant";
    object      thermophysicalProperties;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
"""

    def __init__(self, method, copy_path):
        self.copy_path = copy_path
        self.case_dir = r'constant'
        super(thermophysicalProperties, self).__init__('thermophysicalProperties',  method)

