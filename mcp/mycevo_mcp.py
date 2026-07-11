"""Checkout wrapper for the packaged MycEvo MCP server."""

from mycevo.mcp.server import *  # noqa: F403
from mycevo.mcp.server import main


if __name__ == "__main__":
    raise SystemExit(main())
