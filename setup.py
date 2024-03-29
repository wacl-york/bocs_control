from setuptools import setup

setup(
    name="bocs",
    version="1.0.0",
    description="Control code for BOCS instrument",
    keywords="BOCS, air quality, low cost sensors",
    author="Stuart Lacy",
    author_email="stuart.lacy@york.ac.uk",
    url="https://github.com/wacl-york/bocs_control",
    license="Apache",
    packages=["bocs_control"],
    install_requires=["pyserial",],
    python_requires=">=3.4, <4",
    entry_points={
        "console_scripts": [
            "bocs_control = bocs_control.control:main",
            "bocs_archive = bocs_control.archive:main",
        ]
    },
)
