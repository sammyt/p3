from distutils.core import setup

setup(
    name='p3',
    version='0.1.0-dev',
    packages=['p3'],
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'cssselect >= 0.7.1'
        'lxml >= 3.1.0'
    ]
)