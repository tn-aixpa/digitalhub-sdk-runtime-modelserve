"""
Setup file for the SDK package.
"""
from setuptools import setup, find_packages

install_requires = [
    "boto3==1.28.2",
    "pydantic==2.0.2",
    "pandas==2.0.3",
]

setup(
    name="sdk",
    version="",
    author="",
    author_email="",
    description="",
    install_requires=install_requires,
    extras_require={},
    packages=find_packages(),
)
