from setuptools import setup, find_packages

options = dict(
    name='zbubliny_matcher',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    description='Matchers for zbubliny',
    install_requires = ['googletrans', 'gensim', 'pyemd', 'click', 'nltk', 'psycopg2', 'awscli'],
    entry_points = {
        'console_scripts' : [
            'zbubliny = zbubliny_matcher.cli_interface:run',
            'zbubliny-multi = zbubliny_matcher.cli_interface:run_multi',
            'zbubliny-db-search = zbubliny_matcher.database_scanner:run_scanner',
            'zbubliny-server = zbubliny_matcher.search_server:run_server',
            'zbubliny-fb-bot = zbubliny_matcher.bot:run_server'
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