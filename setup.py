from setuptools import setup, find_packages

setup(
    name="decom",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "rich",
        "typer",
        "fastapi",
        "uvicorn",
        "pydantic",
        "requests",
        "cryptography",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "decom=cli.main:app",
        ],
    },
)
