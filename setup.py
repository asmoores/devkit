"""A setuptools based setup module


"""

from setuptools import setup, setuptools

setup(
    name='devkit',
    version='0.0.1',
    description='Project lifecycle tool for polyglot micro-services based development projects.',
    url='https://github.com/asmoores/devkit',
    author='Andrew Moores',
    install_requires=['pyyaml', 'gitpython', 'tabulate', 'pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    entry_points={
        'console_scripts': [
            'devkit=devkit.devkit_cli:main',
        ],
    },
    keywords='dev build tool',
    packages=setuptools.find_packages(),

)
