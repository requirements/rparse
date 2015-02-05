# rparse [![Build 
Status](https://travis-ci.org/dveselov/rparse.svg?branch=master)](https://travis-ci.org/dveselov/rparse)

Python `requirements.txt` parser.

# Usage

```python
import rparse


requirements = """
flask == 0.10.1
pip >= 6.0.0, < 6.0.7
"""

for requirement in rparse.parse(requirements):
    print(requirement)
```

Output will be looks like this:

```python
("flask", [("==", "0.10.1")])
("pip", [(">=", "6.0.0"), ("<", "6.0.7")])
```
