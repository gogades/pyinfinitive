import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyinfinitive",
    version="0.0.5",
    author="Michael Wood",
    author_email="mww012@gmail.com",
    description="An API wrapper for the Infinitive project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mww012/pyinfinitive.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
