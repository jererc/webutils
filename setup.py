from setuptools import setup, find_packages

setup(
    name='webutils',
    version='2024.12.09.065843',
    author='jererc',
    author_email='jererc@gmail.com',
    url='https://github.com/jererc/webutils',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.10',
    install_requires=[
        'dateutils',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'playwright',
    ],
    extras_require={
        'dev': ['flake8', 'pytest'],
    },
    include_package_data=True,
)
