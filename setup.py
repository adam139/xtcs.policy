from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='xtcs.policy',
      version=version,
      description="a site policy for xtcs web site",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='python plone',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['xtcs'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'mysqlclient==1.4.6',
          'Products.CMFPlone',
          'z3c.jbot',
          'plone.app.dexterity',          
          'MySQL-python',
          'SQLAlchemy',          
#           'xtcs.theme',
          'z3c.caching',
          'collective.autopermission',
          'sqlalchemy.dbapi',
                                                                     
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing',]
      },         
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
