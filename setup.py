import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvidesk",
    version="0.0.1",
    author="Vinicius Lanzarini",
    author_email="vinicius.lanzarini@movidesk.com",
    description="Movidesk API client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vilanz/pyvidesk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)