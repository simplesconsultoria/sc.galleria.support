# -*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

version = '0.5'

setup(name='sc.galleria',
      version=version,
      description="Simple gallery for plone based in http://galleria.io",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='python simples_consultoria plone galleria gallery',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['sc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
