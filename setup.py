import setuptools

from _version import __version__ as version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("Boto4GS/requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="Boto4GS",
    version=version,
    author="Record Linking Lab",
    author_email="recordlinkinglab@gmail.com",
    description="A package to interact with the RLL AWS account in a set way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/byuawsfhtl/Boto4GS.git",
    project_urls={
        "Bug Tracker": "https://github.com/byuawsfhtl/Boto4GS/issues",
    },
    packages=["Boto4GS", "Boto4GS/src", "Boto4GS/src/models", "Boto4GS/src/models/services", "Boto4GS/src/presenters", "Boto4GS/src/views"],
    install_requires=install_requires,
)
