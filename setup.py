from setuptools import setup

setup(
    name='ava',
    version='2.0.1',
    description='Discord chat bot using AIML artificial intelligence.',
    url='https://github.com/DevDungeon/ChattyCathy',
    author='DevDungeon',
    author_email='nanodano@devdungeon.com',
    license='GPL-3.0',
    packages=['ava'],
    scripts=[
        'bin/ava',
        'bin/ava.bat',
    ],
    package_data={
        'ava': [
            'std-startup.xml',
            'aiml/alice/*.aiml',
            'aiml/custom/*.aiml',
            'metadata/*.*',
            'utils/*.*',
            'bot.properties'
        ],
    },
    zip_safe=False,
    install_requires=[
        'docopt',
        'python-aiml',
        'discord.py',
        'requests'
    ]
)
