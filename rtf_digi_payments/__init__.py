"""Top-level shim package to expose `src/rtf_digi_payments` as `rtf_digi_payments`.

This allows importing `rtf_digi_payments.*` during local development without
installing the package (it forwards to `src.rtf_digi_payments`).
"""
from importlib import import_module
from types import ModuleType

_src_pkg = None
try:
    _src_pkg = import_module('src.rtf_digi_payments')
except Exception:
    _src_pkg = None

if _src_pkg:
    # Expose attributes from the src package module
    for _name in dir(_src_pkg):
        if _name.startswith('_'):
            continue
        globals()[_name] = getattr(_src_pkg, _name)

    # Make submodule imports work (so `from rtf_digi_payments import models` works)
    __path__ = getattr(_src_pkg, '__path__', __path__)
