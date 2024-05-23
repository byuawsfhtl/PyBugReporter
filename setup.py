import os

import setuptools

from _version import __version__ as version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ""
with open("PyBugReporter/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

requirements = requirements.split("\n")

def listFolders(directory):
    folders = []
    for item in os.listdir(directory):
        itemPath = os.path.join(directory, item)
        if os.path.isdir(itemPath) and item != "__pycache__":
            folders.append(itemPath)
    otherFolders = [listFolders(itemPath) for itemPath in folders]
    for folder in otherFolders:
        folders.extend(folder)
    return folders

folderPath = "PyBugReporter"
folders = listFolders(folderPath)
folders.append("PyBugReporter")
print(folders)

setuptools.setup(
    name='PyBugReporter',
    version=version,
    author='Record Linking Lab',
    author_email='recordlinkinglab@gmail.com',
    description='A python library for catching thrown exceptions and automatically creating issues on a GitHub repo.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/byuawsfhtl/PyBugReporter.git',
    project_urls = {
        "Bug Tracker": "https://github.com/byuawsfhtl/PyBugReporter/issues"
    },
    packages=folders,
    install_requires=requirements,
)
