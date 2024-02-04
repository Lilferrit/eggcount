from setuptools import setup, find_packages

setup(
    name = "eggcount",
    version = "0.1",
    packages = find_packages(),
    package_data={"eggcount": ["assets/*.jpg", "assets/*.png"]}
)
