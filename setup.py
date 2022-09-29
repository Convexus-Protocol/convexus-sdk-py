import os
from setuptools import setup, find_packages

with open(os.path.join('.', 'VERSION')) as version_file:
    version = version_file.read().strip()

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt") as requirements:
    requires = list(requirements)

extras_requires = {
    'tests': ['pytest~=7.1.3']
}

setup(
    name='convexus',
    version=version,
    description='Convexus SDK for Python is useful for building applications on top of Convexus',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Convexus',
    author_email='convexus.protocol@gmail.com',
    url='https://github.com/Convexus-Protocol/convexus-sdk-py',
    packages=find_packages(exclude=['tests*', 'examples*']),
    install_requires=requires,
    extras_require=extras_requires,
    python_requires='~=3.10',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.10'
    ]
)
