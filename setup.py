import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    ]

testing_requires = [
    "pytest"
]

setup(name='pyramid-tiny-utility',
      version='0.0',
      description='the training wheel for developping with pyramid',
      long_description=README + '\n\n' +  CHANGES,
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      extras_require={"testing": testing_requires}
      )

