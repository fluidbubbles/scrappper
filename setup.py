from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.readlines()

setup(
    name='scrapper',
    version='0.0.1',
    author="Danial Mubarik",
    author_email="rusdanyal@gmail.com",
    license='Open',
    description="Web scrapper",
    packages=find_packages(),
    package_data={'static': ['*.png'],
                  'templates': ['*.html']
                  },
    python_requires=">=3.10",
    install_requires=requirements
)
