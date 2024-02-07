from setuptools import setup, find_packages

setup(
    name = "larvaecount",
    version = "0.1",
    packages = find_packages(),
    package_data = {
        "larvaecount": [
            "assets/*.jpg",
            "assets/*.png",
            "assets/*.css",
            "docs/*.md"
        ]
    }
)
