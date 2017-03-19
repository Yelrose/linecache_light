import cPickle as pkl
from collections import Iterable
import os


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
    def __init__(self, filename, cache_suffix='.cache'):
        self.filename = filename
        if os.path.exists(self.filename + cache_suffix):
            self.st_mtime,  self.line_seek = pkl.load(open(self.filename + cache_suffix, 'rb'))
            self.num_lines = len(self.line_seek)
            if self.st_mtime != os.stat(self.filename).st_mtime:
                print('The cache file is out-of-date')
                self.build_seek_index(cache_suffix)
        else:
            self.build_seek_index(cache_suffix)

    def build_seek_index(self, cache_suffix):
        print("Caching lines informaiton to %s" % (self.filename + cache_suffix))
        statinfo = os.stat(self.filename)
        self.st_mtime = statinfo.st_mtime
        with open(self.filename, 'rb') as f:
            self.line_seek = []
            while True:
                seek_pos = f.tell()
                line = f.readline()
                if not line: break
                self.line_seek.append(seek_pos)
            pkl.dump((self.st_mtime, self.line_seek), open(self.filename + cache_suffix, 'wb'))
            self.num_lines = len(self.line_seek)


    def __getitem__(self, line_no):
        if isinstance(line_no, slice):
            return [self[ii] for ii in xrange(*line_no.indices(len(self)))]
        elif isinstance(line_no, Iterable):
            return [self[ii] for ii in line_no]
        else:
            if line_no >= self.num_lines:
                raise IndexError("Out of index: line_no:%s  num_lines: %s" % (line_no, self.num_lines))
            fhandle = open(self.filename, 'rb')
            fhandle.seek(self.line_seek[line_no])
            line = fhandle.readline()
            return line

    def __len__(self):
        return self.num_lines

