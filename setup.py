#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    l_description = f.read()


with open('AUTHORS.rst', encoding='utf-8') as f:
    l_author = f.read()


try:
    setup(
        name="monitoring_project_api",
        version="0.0.1",

        url="",

        description='Monitoring project API',
        long_description=l_description,

        author=l_author,
        author_email="kamel.houchat@ynov.com",

        keywords=[
            "Monitoring", "Anomaly detection", "Nginx Log",
        ],

        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3.7",
            "Topic :: Scientific/Engineering",
        ],

        packages=find_packages(exclude=['tests*']),

        python_requires=">=3.7",
        install_requires=[
            "flask~=2.0.1",
            "python-dotenv>=0.17.1",
            "sqlalchemy~=1.4.17",
            "marshmallow>=3.12.1",
            "marshmallow-sqlalchemy>=0.26.0",
            "flask-smorest>=0.31.1",
            "requests~=2.25.1",
            "Flask-APScheduler~=1.12.2",
            "pandas==1.3.4",
        ],
    )
except:  # noqa
    print(
        "\n\nAn error occurred while building the project, "
        "please ensure you have the most updated version of setuptools, "
        "setuptools_scm and wheel with:\n"
        "   pip install -U setuptools setuptools_scm wheel\n\n"
    )
    raise
