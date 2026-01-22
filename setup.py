"""
Setup script for DiveIn
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="divein",
    version="1.0.1",
    author="Akhilesh S",
    author_email="akhileshs222000@gmail.com",
    description="A simple, secure, and modern SSH connection manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Akhilesh2220/divein",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[
        "typer",
        "rich",
        "cryptography",
        "pexpect",
    ],
    entry_points={
        "console_scripts": [
            "divein=divein.__main__:main",
        ],
    },
)