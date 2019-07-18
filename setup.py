from setuptools import setup, find_packages

setup(
	name='codonPython',
	version='0.1',
	license='BSD',
	packages=['codonPython',],
	install_required=[
		'numpy',
		're',
		'pandas',
		'random',
		'sqlalchemy'
	],
	author='NHS Digital DIS Team',
	author_email='paul.ellingham@nhs.net',
	url='https://digital.nhs.uk/data-and-information',
	description='This is a first attempt at how our package will work.'
)
