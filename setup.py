from distutils.core import setup
setup(
  name = 'packson',
  packages = ['packson'],
  version = '0.2.1',
  license='MIT',
  description = 'Easily bind JSON to user defined class instances.',
  author = 'Eric Falkenberg',
  author_email = 'ericsfalkenberg@gmail.com',
  url = 'https://github.com/EricFalkenberg/packson',
  download_url = 'https://github.com/EricFalkenberg/packson/archive/v0.2.1.tar.gz',
  keywords = ['json', 'data', 'bind', 'decorator', 'types'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)