from setuptools import setup

setup(
    name='tif2png',
    version='1.0',
    py_modules=['tif2png'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'tif2png=tif2png:main',
        ],
    },
)
