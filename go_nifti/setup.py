from setuptools import setup

setup(
    name='GoNifti',
    version='0.1',
    packages=['go_nifti/src'],
    install_requires=[
        'click',
        'dicom2nifti',
        'tqdm',
    ],
    entry_points='''
        [console_scripts]
        gonifti=src.GoNifti:main
    ''',
)
