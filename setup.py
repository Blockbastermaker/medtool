from setuptools import setup

"""
Description of how to make a python package

https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

"""

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
      name='medtool',
      version='1.0',
      long_description=readme(),
      description='A collection of tools for medical data analysis' ,
      url='https://github.com/zhenglz/medtool',
      author='zhenglz',
      author_email='zhenglz@outlook.com',
      license='GPL-3.0',
      packages=['medtool'],
      install_requires=[
          'numpy',
          'pandas',
          'mpi4py',
          'scikit-learn',
          'matplotlib',
      ],
      include_package_data=True,
      zip_safe=False,
      )