# linecache_light
A python package that can fast random access any lines in a large file without high memory cost.

## Usage

It's avaiable to install linecache_light throught pip.

```
	pip install linecache_light
```

The basic usage is followed:

```
	from linecache_light import LinceCache
	linecache = LineCache('large_file.txt', cache_suffix='.cache')
	# This will create a cache file with suffix in your file location
	# Noticing it may cost a long time to cache the file since the LineCache will scan through the document.
	# If the cache file has already existed, it will reload the cache file in a much short time without scan through the document again.
	
	# Check the total number of lines
	print len(linecache)
	
	# Access the lines by line index
	print linecache[5]
	
	# Access the lines by slice
	print linecache[3:5]
	print linecache[-1]
	
	# Access the lines by a iterable list of index
	print linecache[[3,2,1,5]]
```


