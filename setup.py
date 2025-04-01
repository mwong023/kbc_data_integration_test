from setuptools import setup, find_packages

setup(
    name="kbc_automated_tests",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "loguru",
        "requests",
    ],
) 