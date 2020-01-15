from setuptools import setup

setup(
    name='alice',
    version='2.0.1',
    description='Discord chat bot using AIML artificial intelligence.',
    url='https://github.com/DevDungeon/ChattyCathy',
    author='Giriprakash',
    author_email='giriprakash@outlook.in',
    license='GPL-3.0',
    packages=['alice'],
    scripts=[
        'bin/alice',
        'bin/alice.bat',
    ],
    package_data={
        'alice': [
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
