from setuptools import setup, find_packages

setup(
    name='webutils',
    version='0.1.0',
    author='jererc',
    author_email='jererc@gmail.com',
    url='https://github.com/jererc/webutils',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.10',
    install_requires=[
        'selenium',
    ],
    extras_require={
        'dev': ['pytest', 'flake8'],
    },
    include_package_data=True,
)
