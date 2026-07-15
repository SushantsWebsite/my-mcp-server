import os
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.fastmcp import FastMCP

AUTH_TOKEN = os.environ.get("MCP_AUTH_TOKEN", "")

class StaticTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        if not AUTH_TOKEN:
            return None  # no token configured = reject everything, fail closed
        if token == AUTH_TOKEN:
            return AccessToken(token=token, client_id="my-server-client", scopes=["mcp"])
        return None

mcp = FastMCP(
    "my-server",
    host="0.0.0.0",
    port=8080,

)
@mcp.tool()
def echo(text: str) -> str:
    """Echo back the input text."""
    return f"You said: {text}"

@mcp.tool()
def list_dir(path: str = ".") -> str:
    """List files in a directory."""
    return "\n".join(os.listdir(path))

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
