from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()
setup(
    name="nba_data_scraper",
    packages=["nba_data_scraper"],
    version="0.0.01",
    license="GNU General Public License v3.0",
    description="Python package to scrape NBA data and statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jed Ong",
    author_email="ong.jedidiah@gmail.com",
    url="https://github.com/jong481/nba_data_scraper",
    download_url="https://github.com/jong481/nba_data_scraper",
    keywords=["NBA", "basketball", "python"],
    install_requires=["requests", "pandas"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
    ],
)