from ...superTemplate import SuperTemplate


class topoSetDict(SuperTemplate):
    template=r"""*--------------------------------*- C++ -*----------------------------------*\
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
    object      topoSetDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
    """

    def __init__(self, method, copy_path):
        self.copy_path = copy_path
        self.case_dir = r'system'
        super(topoSetDict, self).__init__('topoSetDict', method)
