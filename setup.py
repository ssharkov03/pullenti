from setuptools import setup, find_packages

setup(
    name="PullentiPython",
    version="0.1",
    author="Sergei Sharkov",
    author_email="serezhasharkov2003@gmail.com",
    description="Python implementation of PullentiPython.",
    url='https://github.com/ssharkov03/pullenti',  # Provide either the link to your github or to your website
    download_url='https://github.com/ssharkov03/pullenti/archive/refs/tags/0.1.tar.gz',  # I explain this later on
    packages=find_packages(),
    include_package_data=True,
    package_data={
            'pullenti': [
                '**/*.dat',
                '**/*.csv',
                '**/*.txt',
                '**/*.jpg',
                '**/*.png'
            ]
        },
    python_requires=">=3.8"
)


