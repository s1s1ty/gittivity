"""Run "python setup.py install" to install gittivity."""

from setuptools import setup

try:
    with open('README.md') as f:
        long_description = f.read()

except Exception:
    long_description = """
    `gittivity` is a simple, elegant Python package to show git
    activity terminal notificaion.

    More information at: https://github.com/s1s1ty/gittivity/.
"""


setup(name="gittivity",
      packages=['gittivity'],
      version='0.0.1',
      description="Git activity terminal notifier",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Topic :: Utilities',
          'Topic :: Terminals',
          'Programming Language :: Python :: 3',
      ],
      author='Shaonty Dutta',
      author_email='shaonty.dutta@gmail.com',
      license='MIT',
      url="https://github.com/s1s1ty/gittivity/",
      keywords=['Utilities', 'Terminal', 'Notifier'],
      include_package_data=True,
      zip_safe=False,
      setup_requires=['setuptools>=38.6.0'],
      install_requires=["requests", "pyjsonq", "pync"],
      entry_points={
        'console_scripts': ['gittivity=gittivity'],
      }
      )
