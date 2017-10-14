from setuptools import setup, find_packages

options = dict(
    name='zbubliny_matcher',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    description='Matchers for zbubliny',
    install_requires = ['googletrans', 'gensim', 'pyemd', 'click', 'nltk'],
    entry_points = {
        'console_scripts' : [
            'zbubliny = zbubliny_matcher.cli_interface:run',
            'zbubliny-multi = zbubliny_matcher.cli_interface:run_multi'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)

setup(**options)