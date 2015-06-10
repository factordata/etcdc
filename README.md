WIP!

# What works

- get keys
- ls key [recursive]
- get
- set
- mkdir

# What is planned

- Secure (certificates)
- delete key
- delete dir [recusive]
- TTL for files and dirs
- wait (and callback)
- Atomic creation of in-order keys
- Atomic CAS (Compare And Swap)
- Atomic CAD (Compare And Delete)
- Setting keys from files


# How to use

Just to get started. Need proper docs


```
>>> from etcdc.client import Client
>>> c = Client()
>>> c.ls()  # returns a Directory representing '/'
>>> c.ls('/some_dir', recursive=True)  # returns a Directory representing '/some_dir' with nested dirs (recursively)
>>> c.get_keys()  # return a list of keys under '/'
>>> c.get_keys('/some_dir', recursive=True)  # return a list of keys under '/some_dir' recursively
>>> c.get('/some_file')  # Returns a Node  representing '/some_file'
>>> c.set('/some_file', 'some_value')  # Set or create a value for '/some_file' and returns a Node representing the modified or created node
```

# Dev

run tests

py.test

run tests with coverage

py.test --cov etcdc --cov-report html
