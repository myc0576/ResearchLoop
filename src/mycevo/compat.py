"""Deprecated command wrappers for pre-MycEvo product names."""

from __future__ import annotations

import sys

from .cli import main as _main


def _compat_main(old_name: str, argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    print(f"warning: '{old_name}' is deprecated; use 'mycevo' instead.", file=sys.stderr)
    return _main(args)


def resevo_main(argv: list[str] | None = None) -> int:
    return _compat_main("resevo", argv)


def researchloop_main(argv: list[str] | None = None) -> int:
    return _compat_main("researchloop", argv)


main = researchloop_main


if __name__ == "__main__":
    raise SystemExit(main())
