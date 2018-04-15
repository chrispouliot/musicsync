from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='musicsync',
    version='0.3',
    description='Sync songs between music streaming services',
    long_description=readme(),
    url='https://github.com/moxuz/musicsync',
    author='Chris Pouliot',
    author_email='me@chrispouliot.codes',
    license='MIT',
    test_suite='musicsync.tests',
    packages=['musicsync'],
    install_requires=[
        "appdirs",
        "beautifulsoup4",
        "certifi",
        "chardet",
        "decorator",
        "future",
        "gmusicapi",
        "gpsoauth",
        "httplib2",
        "idna",
        "lxml",
        "MechanicalSoup",
        "mock",
        "mutagen",
        "oauth2client",
        "pbr",
        "proboscis",
        "protobuf",
        "pyasn1",
        "pyasn1-modules",
        "pycryptodomex",
        "python-dateutil",
        "requests",
        "rsa",
        "six",
        "urllib3",
        "validictory",
    ],
    zip_safe=False
)
