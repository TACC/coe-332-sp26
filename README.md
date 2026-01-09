# COE 332: Software Engineering and Design, Spring 20256

[![Documentation Status](https://readthedocs.org/projects/coe-332-sp26/badge/?version=latest)](https://coe-332-sp26.readthedocs.io/en/latest/?badge=latest)


This repo contains the lecture materials for the UT Austin course COE 332, Spring 2026.

https://coe-332-sp26.readthedocs.io/

# Building Locally

We are using Nix for the local build. Note that the requirements.txt file is included only for the ReadTheDocs build.

To run the doc engine locally, first enter the Nix development environment

```
$ nix develop -i 
```

We recommend the `-i` so that environment variables set in the outside shell don't interfere. 
In particular, this can prevent issues with locale errors, etc.

From within the Nix development environment:

```
make livehtml
```
will start the server on localhost. 