from setuptools import setup, find_packages

install_requires = ["boto3==1.22.8", "pydantic==1.10.7", "mlrun==1.3.0"]

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
