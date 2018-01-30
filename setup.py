from setuptools import setup

with open('README.rst') as rdm:
    README = rdm.read()

setup(
    name='qjobs',
    use_scm_version=True,

    description='Get a clean and flexible output from qstat',
    long_description=README,

    url='https://github.com/amorison/qjobs',

    author='Adrien Morison',
    author_email='adrien.morison@gmail.com',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],

    packages=['qjobs'],
    entry_points={
        'console_scripts': ['qjobs = qjobs.__main__:main']
        },
    setup_requires=['setuptools_scm'],
    install_requires=['setuptools_scm', 'loam>=0.1.1'],
)
