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
        'dateutils',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'selenium',
    ],
    extras_require={
        'dev': ['pytest', 'flake8'],
    },
    include_package_data=True,
)
