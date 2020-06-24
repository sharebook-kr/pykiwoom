from setuptools import setup

setup(
    name            = 'pykiwoom',
    version         = '0.0.6',
    description     = 'python wrapper for Kiwoom Open API+ (Korea Stock Market)',
    url             = 'https://github.com/sharebook-kr/pykiwoom',
    author          = 'Lukas Yoo, Brayden Jo',
    author_email    = 'brayden.jo@outlook.com, jonghun.yoo@outlook.com, pystock@outlook.com',
    install_requires= ['pandas'],
    license         = 'MIT',
    packages        = ['pykiwoom'],
    zip_safe        = False
)