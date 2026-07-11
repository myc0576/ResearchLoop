"""Deprecated CLI module; use :mod:`mycevo.cli`."""

from mycevo.compat import resevo_main as main


if __name__ == "__main__":
    raise SystemExit(main())
