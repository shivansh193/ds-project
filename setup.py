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
        "sqlalchemy",
        "alembic",
        "psycopg2-binary",
        "ipfshttpclient",
        "requests",
        "cryptography",
        "pycryptodome",
        "RestrictedPython",
        "docker",
        "prometheus-client",
        "solana",
        "anchorpy",
    ],
    entry_points={
        "console_scripts": [
            "decom=decom.cli.main:app",
        ],
    },
)
