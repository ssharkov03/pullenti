from setuptools import setup, find_packages

setup(
    name="PullentiPython-ssharkov",
    version="0.0.7",
    author="Sergei Sharkov",
    author_email="serezhasharkov2003@gmail.com",
    description="Python implementation of PullentiPython.",
    url='https://github.com/ssharkov03/pullenti',  # Provide either the link to your github or to your website
    download_url='https://github.com/ssharkov03/pullenti/archive/refs/tags/0.0.7.tar.gz',  # I explain this later on
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8"
)


