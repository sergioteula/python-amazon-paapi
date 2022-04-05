import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-amazon-paapi',
    version='4.2.2',
    author='Sergio Abad',
    author_email='sergio.abad@bytelix.com',
    description='Amazon Product Advertising API 5.0 wrapper for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/sergioteula/python-amazon-paapi',
    packages=setuptools.find_packages(),
    install_requires=['certifi',
                      'six',
                      'python_dateutil',
                      'setuptools',
                      'urllib3'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
