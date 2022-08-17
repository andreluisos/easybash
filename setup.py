"""
setuptools' settings.
"""

from setuptools import setup, find_packages

setup(
    name='basher',
    version='1.0.0',
    author='André Luís',
    author_email='andreluisos@me.com',
    description='A Python shell command helper using the subprocess Popen.',
    packages=find_packages(),
    license="GPLv3",
    keywords=['Bash', 'sh', 'shell', 'Linux'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
)
