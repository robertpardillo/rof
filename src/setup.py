from distutils.core import setup

setup(
    name='rof',
    version='0.1',
    packages=['Rof', 'Rof.pyParFoam', 'Rof.pyParFoam.foam_templates', 'Rof.pyParFoam.foam_templates.0_templates',
              'Rof.pyParFoam.foam_templates.system_templates', 'Rof.pyParFoam.foam_templates.constant_templates',
              'Rof.miscellaneous'],
    url='https://github.com/robertpardillo/rof',
    license='MIT',
    author='Roberto',
    author_email='robertpardillo93@gmail.com',
    description='Api to control OpenFOAM'
)
