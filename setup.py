from setuptools import setup, find_packages

setup(
    name='webopen',
    version='1.0.0',
    author='Bhuvaneshwar_Marri',
    author_email='bhuvaneshwarmarri@gmail.com',
    description='A package helps to open browser via CLI and used to store and manage your passwords.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BhuvaneshwarMarri/webopen',
    project_urls={
        'Homepage': 'https://github.com/BhuvaneshwarMarri/webopen',
        'Issues': 'https://github.com/BhuvaneshwarMarri/webopen/issues'
    },
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["add", "search","delete"],
    python_requires=">=3.8",
    install_requires=[
        "argparse",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'webopen = webopen.main:main',
        ],
    },
)
