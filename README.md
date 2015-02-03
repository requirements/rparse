# rparse

Python `requirements.txt` parser.

# Usage

```python
import rparse


requirements = """
flask == 0.10.1
pip >= 6.0.0, < 6.0.7
"""

for requirement in rparse.parse(requirements):
    print(requirement.pretty())
```

Output will be looks like this:

```
start
  package
    name    flask
    vspec
      comparison    ==
      version   0.10.1

start
  package
    name    pip
    vspec
      comparison    >=
      version   6.0.0
      comparison    <
      version   6.0.7
```
