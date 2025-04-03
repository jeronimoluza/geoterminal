from setuptools import setup, find_packages

setup(
    name="geoterminal",
    version="0.1.0",
    description="Geoterminal is a command-line tool designed to simplify common GIS (Geographic Information System) tasks that you may encounter in your daily work.",
    author="Jerónimo Luza",
    author_email="jero.luza@gmail.com",
    url="https://github.com/jeronimoluza/geoterminal",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "geopandas>=0.9.0",
        "pandas>=1.2.0",
        "pyarrow>=6.0.0",
        "shapely>=1.7.0",
        "h3==4.1.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ]
    },
    entry_points={
        "console_scripts": [
            "geoterminal=src.cli:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
