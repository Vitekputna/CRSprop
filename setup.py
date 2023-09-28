import setuptools

setuptools.setup(
    name="CRSprop",
    version="0.2.0",
    url="https://github.com",
    author="DFawdwdfa",
    author_email="damien.j.martin@gmail.com",
    description="Allows conversion of Roman numerals to ints (and vice versa)",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    package_data={'': ['data/*.yaml']},
)