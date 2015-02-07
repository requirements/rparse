# rparse [![Build Status](https://travis-ci.org/dveselov/rparse.svg?branch=master)](https://travis-ci.org/dveselov/rparse)

Python `requirements.txt` parser.

# Installation

```bash
$ pip install rparse
```

# Usage

```python
import rparse


requirements = """
flask == 0.10.1
pip >= 6.0.0, < 6.0.7
"""

for requirement in rparse.parse(requirements):
    print(requirement.name, requirement.specs)
```

Output will be looks like this:

```python
("flask", [("==", "0.10.1")])
("pip", [(">=", "6.0.0"), ("<", "6.0.7")])
```

`rparse` also have simple command line interface that can be used like this:

```bash
$ cat requirements.txt
flask==0.10.1
raven[flask]>=1.0

$ rparse.py requirements.txt
Package: flask
Version Specifier: [('==', '0.10.1')]
Extras: None
Comment: None
----------------------------------------------------------------
Package: raven
Version Specifier: [('>=', '1.0')]
Extras: ['flask']
Comment: None
----------------------------------------------------------------
```
