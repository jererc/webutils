from setuptools import setup, find_packages

setup(
    name='webutils',
    version='2025.08.10.115157',
    author='jererc',
    author_email='jererc@gmail.com',
    url='https://github.com/jererc/webutils',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.10',
    install_requires=[
        'playwright',
    ],
    extras_require={
        'dev': ['flake8', 'pytest'],
    },
    include_package_data=True,
)
