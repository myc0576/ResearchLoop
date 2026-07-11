"""Deprecated MCP filename wrapper; use ``mycevo.mcp.server``."""

from __future__ import annotations

import sys

from mycevo_mcp import main


if __name__ == "__main__":
    print("warning: 'research_harness_mcp.py' is deprecated; use 'mycevo mcp serve'.", file=sys.stderr)
    raise SystemExit(main())
