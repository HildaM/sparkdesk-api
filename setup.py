from distutils.core import setup

from setuptools import find_namespace_packages

setup(
      name='sparkdesk-api',
      version='1.0.0',
      description='sparkdesk-api 讯飞星火大模型api',
      author='HildaM',
      author_email='Hilda_quan@163.com',
      url='https://github.com/HildaM/sparkdesk-api',
      license='GNU General Public License v3.0',
      packages=find_namespace_packages('src'),
      package_dir={'': 'src'},
      install_requires=[
          'httpx[socks]'
      ]
)
