from setuptools import find_packages, setup
from typing import List
from backend.logger.logger import CustomLogger

logger = CustomLogger().get_logger()

def get_requirements() -> List[str]:
    """
    This function will return list of requirements
    """
    requirement_list: List[str] = []

    try:
        # Open and read the requirements.txt file
        with open('requirements.lock.txt', 'r') as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                # Strip whitespace and newline characters
                requirement = line.strip()
                # Ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        logger.error("requirements.lock.txt file not found.")  # replaced print with logger

    return requirement_list

print(get_requirements())

setup(
    name="DEEP-WEB-SEARCH-MULTI-AGENT",
    version="0.0.1",
    author="Deep Web Search",
    author_email="deepwebsearch@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)

# pip install -e .