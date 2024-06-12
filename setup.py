from setuptools import setup

setup(name='surfpy',
      version='0.98.1',  # Incremented version to reflect updates
      description='Wave and weather tools written in pure python',
      url='https://github.com/jewliyahh/Tourmo-Surf-Forecast',  # Updated URL
      packages=['surfpy'],
      install_requires=['requests', 'pytz'],
      extras_require={'pygrib': ['pygrib']},
      test_suite='nose.collector',
      tests_require=['nose'],
      setup_requires=['nose>=1.0'],
      zip_safe=False)
