# YouOweMe

## Install

1. Check if you have Python version 3 installed. Read official [documentation](https://www.python.org/downloads/).
2. Install Poetry version 1.1 or higher. Read official [documentation](https://python-poetry.org/docs/).

## Install project dependencies

To install project dependencies, run the following command:

```bash
$ poetry install
```
Then run the following command, so that all subsequent commands may run in the virtual environment:

```bash
$ poetry shell
```

#### SCC

To install the SCC tool, follow the steps described [here](https://github.com/boyter/scc), which is the official documentation

## Run project

To run the project, run the following command:

```bash
$ ./you_owe_me.sh [directoy_path_to_analyze]
```

### Run test suite

Inside proetry shell, run the following command:

```bash
$ task test
```

or

```bash
$ poetry run task test
```

### Run lint

Inside poetry shell, run the following command:

```bash
$ task lint
```

or

```bash
$ poetry run task lint
```

### Initialize test submodule
Inside the project, run the following commands:

```bash
$ git submodule init
$ git submodule update
```

