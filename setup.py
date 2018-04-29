from setuptools import setup


setup(
    name='musicsync',
    version='0.4.2',
    description='Sync songs between music streaming services',
    long_description_content_type='text/markdown',
    long_description="from musicsync import spotify_gpm_copy  spotify_gpm_copy([\"Discover Weekly\"])",
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
