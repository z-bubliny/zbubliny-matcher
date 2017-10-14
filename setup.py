from setuptools import setup, find_packages
import itertools

options = dict(
    name='zbubliny_matcher',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    description='Matchers for zbubliny',
    # long_description=__doc__.strip(),
    # author='Jan Pipek',
    # author_email='jan.pipek@gmail.com',
    # url='https://github.com/janpipek/physt',
    # package_data={"physt" : ["examples/*.csv"]},
    install_requires = ['googletrans', 'gensim', 'pyemd', 'click'],
    #extras_require = {
    #    'all' : ['dask', 'matplotlib', 'bokeh', 'folium']
    #},
    entry_points = {
        'console_scripts' : [
            'zbubliny = zbubliny_matcher.cli_interface:run'
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

# extras = options['extras_require']
# extras['full'] = list(set(itertools.chain.from_iterable(extras.values())))
setup(**options)