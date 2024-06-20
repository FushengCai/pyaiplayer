from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

# Function to read the requirements from the requirements.txt file
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

setup(
    name="pyaiplayer",
    description="A tool to let human play game against AI model",
    version="0.1.3",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    long_description=description,
    long_description_content_type="text/markdown"
)
