import pickle as pkl
from collections import Iterable
import os
import logging
import io
import numpy as np

try:
    xrange
except NameError:  # python3
    xrange = range

logger = logging.getLogger('LineCache')

class LineCache(object):
    '''
    LineCache caches the line position of a file in the memory. Everytime it access a line, it will seek to the related postion and readline().
    Noticing that it may cost some time when you first cache lines of a file.

    Usage:
        from linecache_ligth import LineCache

        linecache = LineCache('a.txt', cache_suffix='.cache')
        num_lines = len(linecache)
        line_0 = linecache[0]
        line_100 = linecache[100]

    '''
    def __init__(self, filename, cache_suffix='.cache.npy', encoding="utf-8"):
        self.filename = filename
        self.encoding = encoding
        if os.path.exists(self.filename + cache_suffix):
            self.line_seek = np.load(self.filename + cache_suffix, mmap_mode="r")
            self.num_lines = len(self.line_seek)
        else:
            self._build_seek_index(cache_suffix)


    def _build_seek_index(self, cache_suffix):
        logger.info("Caching lines informaiton to %s" % (self.filename + cache_suffix))
        with io.open(self.filename, 'r', encoding=self.encoding, errors="ignore") as f:
            self.line_seek = []
            while True:
                seek_pos = f.tell()
                line = f.readline()
                if not line:
                    break
                self.line_seek.append(seek_pos)
            self.line_seek = np.array(self.line_seek)
            np.save(self.filename + cache_suffix, self.line_seek)
            # Reload
            self.line_seek = np.load(self.filename + cache_suffix, mmap_mode="r")
            self.num_lines = len(self.line_seek)


    def __getitem__(self, line_no):
        if isinstance(line_no, slice):
            return [self[ii] for ii in xrange(*line_no.indices(len(self)))]
        elif isinstance(line_no, Iterable):
            return [self[ii] for ii in line_no]
        else:
            if line_no >= self.num_lines:
                raise IndexError("Out of index: line_no:%s  num_lines: %s" % (line_no, self.num_lines))
            with io.open(self.filename, 'r', encoding=self.encoding, errors="ignore") as fhandle:
                fhandle.seek(self.line_seek[line_no])
                line = fhandle.readline()
            return line

    def __len__(self):
        return self.num_lines

