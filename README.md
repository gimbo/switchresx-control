# switchresx_control - Control utility for SwitchResX

This is a simple utility to aid remote control of [SwitchResX](https://www.madrau.com/index.html), a tool for controlling displays on macOS.

Right now it can list display sets and activate them by name; that's my main remote control use case, so I don't expect to add much more functionality — anything else I can do, I'm happy to do via the SwitchResX GUI itself.

## Installation for use

[pipx](https://github.com/pypa/pipx) is recommended:

```
pipx install <path to this folder>
```

should work.

## Installation for dev

* Create a venv
* `pip install -U pip setuptools`
* `pip install -e ".[dev]"`
* `pre-commit install --install-hooks`

### Bumping versions

Use bump2version; e.g.:

```
bumpversion patch --verbose
```
