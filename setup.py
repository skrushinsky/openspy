from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='openspy',
      version=version,
      description="Search planes in given range",
      long_description="""\
Query [OpenSky](https://opensky-network.org/apidoc/index.html) service
and outputs crafts in a given range (450km from Paris by default).
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='opensky',
      author='Sergey Krushinsky',
      author_email='krushinsky@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests',
          'geopy',
      ],
      tests_require=['nose>=1.0'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
