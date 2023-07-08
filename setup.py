import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
      long_description = fh.read()

setuptools.setup(
      name="sparkdesk-api",
      version="1.0.2",
      author="HildaM",
      author_email="Hilda_quan@163.com",
      description="sparkdesk-api 讯飞星火大模型api",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/HildaM/sparkdesk-api",
      license='GNU General Public License v3.0',
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
)