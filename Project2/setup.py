from setuptools import setup, find_packages

setup(
    name="movielog",
    version="1.0.0",
    author="Nolan",
    description="A movie tracking application using TMDb API",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'certifi>=2025.1.31',
        'charset-normalizer>=3.4.1',
        'idna>=3.10',
        'pillow>=11.1.0',
        'requests>=2.32.3',
        'urllib3>=2.3.0',
        'tk>=0.1.0',
    ],
    entry_points={
        'gui_scripts': [
            'movielog=Movielog:main',
        ],
    },
    python_requires=">=3.12",
)
