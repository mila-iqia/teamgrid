from setuptools import setup

setup(
    name='teamgrid',
    version='0.0.1',
    keywords='memory, environment, agent, rl, openaigym, openai-gym, gym',
    packages=['teamgrid', 'teamgrid.envs'],
    install_requires=[
        'gym>=0.9.6',
        'numpy>=1.15.0',
        'pyqt5>=5.10.1'
    ]
)
