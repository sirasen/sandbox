from setuptools import setup, find_packages

setup(
    name="mlops-lab",
    version="0.0.1",
    description="Simple test",
    install_requires = [ "click"],
    entry_points="""
    [console_scripts]
    test=test.main:main
    """,
    author="Davy Toch",
    packages=find_packages()
)