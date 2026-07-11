"""Deprecated compatibility import for the old ResearchLoop CLI."""

from mycevo.compat import researchloop_main as main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
