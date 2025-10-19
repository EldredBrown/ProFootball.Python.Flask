import setuptools

setuptools.setup(
    name='pro_football_app',
    version='1.0.0',
    description='Program to support my pro football stats hobby.',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'}
)
