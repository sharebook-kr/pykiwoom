from setuptools import setup

setup(
    name            = 'pykiwoom',
    version         = '0.1.5',
    description     = 'python wrapper for Kiwoom Open API+ (Korea Stock Market)',
    url             = 'https://github.com/sharebook-kr/pykiwoom',
    author          = 'Lukas Yoo, Brayden Jo',
    author_email    = 'brayden.jo@pyquant.co.kr, jonghun.yoo@pyquant.co.kr',
    install_requires= ['pandas', 'pyqt5', 'pywin32'],
    license         = 'MIT',
    packages        = ['pykiwoom'],
    zip_safe        = False
)
