from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Simple tools to build discord bots using discord.py"
LONG_DESCRIPTION = "General purpose, simple tools meant to aid in common tasks when building a discord bot."

setup(
    name="dpytools",
    version=VERSION,
    author="ChrisDewa",
    author_mail="alexdewa@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    find_packages=find_packages(),
    install_requires=["discord.py"],

    keywords=["discord.py", "tools", "extensions"],
    classifiers={
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Python Discord Bot Developers",
        "Programming Language :: Python :: 3",
    }

)