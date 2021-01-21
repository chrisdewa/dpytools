from setuptools import setup, find_packages

VERSION = "0.0.2a"
DESCRIPTION = "Simple tools to build discord bots using discord.py"
with open('README.md', encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="dpytools",
    version=VERSION,
    author="ChrisDewa",
    author_mail="alexdewa@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(
        exclude=[".env", "env/*", ".gitignore"]
                                ),
    install_requires=["discord.py==1.6.0"],
    keywords=["discord.py", "tools", "extensions"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8"
)