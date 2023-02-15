from setuptools import setup, find_packages

setup(
    name="PullentiPython",
    version="0.0.1",
    author="Sergei Sharkov",
    author_email="serezhasharkov2003@gmail.com",
    url='https://github.com/ssharkov03/PullentiPython',  # Provide either the link to your github or to your website
    download_url='https://github.com/ssharkov03/PullentiPython/archive/refs/tags/0.0.2.tar.gz',  # I explain this later on
    description="Python implementation of PullentiPython.",
    package_dir={"": "pullenti"},
    packages=find_packages(where="pullenti"),
    python_requires=">=3.8"
)
