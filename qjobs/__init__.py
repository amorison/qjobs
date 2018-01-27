"""The qjobs tool is an attempt at getting a clean qstat output.

See the documentation at https://qjobs.readthedocs.io
"""

from setuptools_scm import get_version
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_version(root='..', relative_to=__file__)
except LookupError:
    __version__ = get_distribution('qjobs').version
except (DistributionNotFound, ValueError):
    __version__ = 'unknown'
