from pathlib import Path
from setuptools import setup, find_packages

current_directory = Path(__file__).parent
setup(
    name="restconf-service",
    version="1.0",
    packages=find_packages(str(current_directory)),
    install_requires=[
        "fastapi==0.116.1",
        "uvicorn==0.35.0",
        "pydantic-settings==2.10.1",
        "yangson==1.6.3",
    ],
    entry_points={
        "console_scripts": [
            "restconf-service-run=restconf_service.__main__:main",
        ],
    },
)
