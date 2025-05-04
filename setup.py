from setuptools import setup, find_packages

setup(
    name="morning_brief",
    version="0.1",
    packages=find_packages(),
)

# this script is basically to add the src directory to the python path so that we can get environment variables without appending the path to the script.

