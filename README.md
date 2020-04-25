# pytest-timer
Porting of [nose-timer](https://github.com/mahmoudimus/nose-timer) plugin for pytest. A timer plugin for pytest (how much time does every test take?).

[![PyPI version](https://badge.fury.io/py/pytest-timer.svg)](https://badge.fury.io/py/pytest-timer)
[![Build Status](https://travis-ci.org/skudriashev/pytest-timer.svg?branch=master)](https://travis-ci.org/skudriashev/pytest-timer)
[![codecov](https://codecov.io/gh/skudriashev/pytest-timer/branch/master/graph/badge.svg)](https://codecov.io/gh/skudriashev/pytest-timer)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Install

To install the latest release from PyPI:
```
pip install pytest-timer
```

To install `pytest-timer` with `termcolor` for colored durations:
```
pip install pytest-timer[termcolor]
```

To install `pytest-timer` with `colorama` for colored durations:
```
pip install pytest-timer[colorama]
```

Or to install the latest development version from Git:
```
pip install git+git://github.com/skudriashev/pytest-timer.git
```

Or to install the latest from source:
```
git clone https://github.com/skudriashev/pytest-timer.git
cd pytest-timer
pip install .
```

You can also make a developer install if you plan on modifying the
source frequently:
```
pip install -e .
```


## Usage

After installing `pytest-timer` plugin the following report will be added:

```
========================== pytest-timer ==========================
[success] tests/test_plugin.py::TestPlugin::test_loaded2: 0.0002s
[success] tests/test_plugin.py::TestPlugin::test_loaded: 0.0002s
```

### How do I show only the `n` slowest tests?

For example, to show only the **10** slowest tests, run pytest with the `--timer-top-n` flag:
```
pytest --with-timer --timer-top-n 10
```

### How do I turn off pretty colors?

In some cases, you may want to disable colors completely. This is done by using the `--timer-no-color` flag.
This is useful when running tests in a headless console.

### How do I filter results by colors?

It is possible to filter results by color. To do so, you can use the `--timer-filter` flag:
```
pytest --with-timer --timer-filter ok
pytest --with-timer --timer-filter warning
pytest --with-timer --timer-filter error
```

Or to apply several filters at once:
```
pytest --with-timer --timer-filter warning,error
```

## License

``pytest-timer`` is MIT Licensed library.


## Contribute

- Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
- Fork the repository on GitHub to start making your changes to the master branch (or branch off of it).
- Write a test which shows that the bug was fixed or that the feature works as expected.
- Send a pull request and bug the maintainer until it gets merged and published.
- Make sure to add yourself to the author's file in setup.py and the Contributors section below :)


## Contributors

- [@skudriashev](https://github.com/skudriashev)
