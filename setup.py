"""
setuptools' settings.
"""

from pathlib import Path
from setuptools import setup, find_packages


setup(
    name='easybash',
    version='1.0.0',
    author='André Luís',
    author_email='andreluisos@me.com',
    description='A Python shell command helper using the subprocess Popen.',
    long_description=Path(__file__).parent.joinpath(
        'README.md').read_text(encoding='UTF-8'),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('img', 'tests')),
    license="GPLv3",
    keywords=['bash', 'sh', 'shell', 'linux'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
    project_urls={
        'Source': 'https://github.com/andreluisos/easybash',
        'Documentation': 'https://github.com/andreluisos/easybash',
        'Issues': 'https://github.com/andreluisos/easybash/issues',
    }
)
