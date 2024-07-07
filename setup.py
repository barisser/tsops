from setuptools import setup, find_packages

setup(
    name='tsops',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "pandas"
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    author='Andrew Barisser',
    description='Timeseries Operations',
    url='https://github.com/barisser/tsops/tree/master',
    python_requires='>=3.6',
)
