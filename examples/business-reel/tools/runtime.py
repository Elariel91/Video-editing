"""Locate locally installed Craft tools without machine-specific paths."""
import os
import pathlib
import shutil


def resolve_cli(variable, executable):
    configured = os.environ.get(variable)
    if configured:
        path = pathlib.Path(configured).expanduser()
        if path.is_file():
            return str(path)
        raise SystemExit(f'{variable} does not point to a file: {path}')
    found = shutil.which(executable)
    if found:
        return found
    raise SystemExit(f'Install {executable} on PATH or set {variable} to its executable path.')
