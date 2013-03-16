from setuptools import setup

setup(
    name='p3',
    version='0.1.2',
    author='Sam Williams',
    author_email='samueltwilliams@gmail.com',
    packages=['p3'],
    license='MIT',
    description='a minimal d3 for python',
    classifiers=[
        'Programming Language :: Python :: 2'
    ],
    install_requires=[
        'cssselect >= 0.7.1',
        'lxml >= 3.1.0'
    ],
    setup_requires=['nose'],
    tests_require=['sure==1.1.7', 'coverage'],
)