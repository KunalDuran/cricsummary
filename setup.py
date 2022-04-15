from setuptools import setup

with open('Readme.md') as file:
    readme = file.read()


setup(
    name="cricsummary",
    version="2.0.0",
    description="Perform Analysis, Create summary table and charts from cricsheet data",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/KunalDuran/cricsummary",
    author="Kunal Duran",
    author_email="kunalduran13@gmail.com",
    license="MIT",
    python_requires = '>=3.5',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["cricsummary"],
    include_package_data=True,
    install_requires=["numpy", "pandas", "matplotlib", "seaborn"],
)
