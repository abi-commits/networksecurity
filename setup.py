from setuptools import find_packages, setup
from typing import List

def get_requirements() ->List[str]:
    """
    This function returns a list of requirements from the requirements.txt file.
    """
    requirement_list: List[str] = []

    try:
       with open('requirements.txt', 'r') as file:
           lines = file.readlines()
           for line in lines:
               requirement = line.strip()
               if requirement and requirement != '-e .':
                   requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    
setup(
    name="networksecurity",
    version="0.1.0",
    author="Abinesh",
    author_email="abinesh3200@gmail.com",
    description="A production-ready MLOps pipeline for network security",
    packages=find_packages(),
    install_requires=get_requirements(),)