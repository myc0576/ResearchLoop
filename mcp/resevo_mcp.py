"""Checkout compatibility wrapper for the packaged Resevo MCP server."""

from resevo.mcp_server import *  # noqa: F403
from resevo.mcp_server import main


if __name__ == "__main__":
    raise SystemExit(main())
