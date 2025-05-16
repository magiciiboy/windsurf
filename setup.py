from setuptools import setup, find_packages

setup(
    name="python-standards-checker",
    version="0.1.0",
    description="CLI tool to check Python standards in GitLab repositories",
    author="",
    author_email="",
    url="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "python-gitlab>=3.0.0",
        "python-dotenv>=1.0.0",
        "pytoml>=0.1.21",
        "requests>=2.31.0",
        "pytest>=7.4.0",
        "packaging>=23.0"
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "python-standards-checker=python_standards_checker:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
