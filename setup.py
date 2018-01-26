from setuptools import setup

with open('README.rst') as rdm:
    README = rdm.read()

setup(
    name='qjobs',
    use_scm_version=True,

    description='Get a clean and flexible output from qstat!',
    long_description=README,

    url='https://github.com/amorison/qjobs',

    author='Adrien Morison',
    author_email='adrien.morison@gmail.com',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],

    packages=['qjobs'],
    entry_points={
        'console_scripts': ['qjobs = qjobs.main:main_wrapper']
        },
    setup_requires=['setuptools_scm'],
    install_requires=['setuptools_scm'],
)
