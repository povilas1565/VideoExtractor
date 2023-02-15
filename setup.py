from setuptools import setup
import subprocess

def readme():
    """Read the long description from the README.md file."""
    with open('README.md') as f:
        return f.read()

def version():
    """Try to use git to construct a version, or fail."""
    try:
        return version_git()
    except subprocess.CalledProcessError:
        return None

def version_git():
    """Use git to construct a version string."""

    # get tags
    tags = subprocess.check_output(['git', 'tag', '--sort=version:rename', '--merged'], universal_newlines=True).splitlines()

    if not tags:
        # no tagged version
        version = '1.0'
        tagsha = None
    else:
        # use last tagged version
        version = tags[-1].strip()
        tagsha = subprocess.check_output(['git', 'rev-list', '-n', '1', version], universal_newlines=True).strip()
        if version.startswith('v'):
            version = version[1:]

    # append +{hash}, if head doesn't match tag
    headsha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], universal_newlines=True).strip()
    if tagsha != headsha:
        version += '+' + headsha[:8]

    # append +dirty or .dirty, if working tree has modified tracked files
    if subprocess.check_output(['git', 'status', '-s', '-uno']).strip():
        if '+' in version:
            version += '.'
        else:
            version += '+'
        version += 'dirty'

    return version

setup(
    name='VideoExtractor',
    version=version(),
    url='https://github.com/povilas1565/VideoExtrCTOR',
    # author, author_email
    description='extract parts of videos based on subtitle searches',
    long_description=readme(),
    long_description_content_type='text/markdown',
    # keywords, license, classifiers

    py_modules=['subsearch'],
    install_requires=[
        'attrs>=22.2.0',
        'Click>=8.1.3',
        'pysubs2>=1.0.0',
        'requests>=2.0.0',
        'Whoosh>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'subsearch = subsearch:cli',
        ],
    },
)
