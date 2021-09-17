# YouOweMe

## Install

1. Check if you have Python version 3 installed. Read official [documentation](https://www.python.org/downloads/).
2. Install Poetry version 1.1 or higher. Read official [documentation](https://python-poetry.org/docs/).

## Dependencies

**SCC**: To install SCC package, run the following command 
* Linux
```
$ sudo snap install sc
```
   * Windows (using [chocolatey](https://chocolatey.org/))
````
$ choco install scc
````
## Run project

To install the project dependencies, run the following command:

```bash
$ poetry install
```

Then run the following command, so that all subsequent commands may run in the virtual environment:

```bash
$ poetry shell
```
