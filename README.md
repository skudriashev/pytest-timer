# pytest-timer
Porting of [nose-timer](https://github.com/mahmoudimus/nose-timer) plugin for pytest. A timer plugin for pytest (how much time does every test take?).

[![Build Status](https://travis-ci.org/skudriashev/pytest-timer.svg?branch=master)](https://travis-ci.org/skudriashev/pytest-timer)

## Install

To install the latest release from PyPI:
```
pip install pytest-timer
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
nosetests --with-timer --timer-top-n 10
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
