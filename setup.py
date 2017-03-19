from os import path
from setuptools import setup

long_description='''
    LineCache caches the line position of a file in the memory. Everytime it access a line, it will seek to the related postion and readline().
    Noticing that it may cost some time when you first cache lines of a file.

    Usage:

        from linecache_light import LineCache

        linecache = LineCache('a.txt', cache_suffix='.cache')

        num_lines = len(linecache)

        line_0 = linecache[0]

        line_100 = linecache[100]

        line_indexing= linecache[[2,3,4,5]]

        line_indexing = linecache[-1]
'''

setup(
    name='linecache-light',
    packages=['linecache_light'],
    version = '0.1.3',
    description='A python package that can fast random access any lines in a large file without high memory cost.',
    author='Ching Kit Wong',
    author_email='270018958@qq.com',
    url='https://github.com/Yelrose/linecache_light',
    keywords=['linecache', 'random access'],
    long_description=long_description,
    license='MIT'
)
