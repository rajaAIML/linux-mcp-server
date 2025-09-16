# Linux MCP Server

A Model Context Protocol (MCP) server built with [fastmcp](https://github.com/modelcontextprotocol/fastmcp).  
This project allows you to run Linux commands through MCP-compatible clients (e.g., Claude Desktop, Ollmcp).  

It comes with **two versions**:
- `linux_mcp_server_whitelist.py` → safer, only allows a defined set of commands  
- `linux_mcp_server_unrestricted.py` → runs any Linux command without restriction  

---

## 🚀 Features
- MCP-compliant server
- Execute Linux commands directly via MCP
- Safe mode with command whitelist
- Unrestricted mode for advanced use

---

## 📦 Installation

This project uses [uv](https://github.com/astral-sh/uv) package manager.

```bash
# Clone the repository
git clone https://github.com/<your-username>/linux-mcp-server.git
cd linux-mcp-server

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

or

```bash
uv sync
```

---

## ▶️ Running the Server

### Whitelist Mode (safe)
```bash
uv run linux_mcp_server_whitelist.py
```

### Unrestricted Mode (advanced)
```bash
uv run linux_mcp_server_unrestricted.py
```

---

## 🔧 MCP Client Configuration

Add this to your Claude Desktop (or other MCP client) configuration:

```json
{
  "mcpServers": {
    "linux-whitelist": {
      "command": "uv",
      "args": ["run", "linux_mcp_server_whitelist.py"]
    },
    "linux-unrestricted": {
      "command": "uv",
      "args": ["run", "linux_mcp_server_unrestricted.py"]
    }
  }
}
```

---

## 📂 Project Structure

```
linux-mcp-server/
├── linux_mcp_server_whitelist.py     # MCP server with
├── linux_mcp_server_unrestricted.py  # MCP server without 
├── requirements.txt                  # Dependencies
├── .gitignore                        # Ignore venv, cache, etc.
└── README.md                         # Documentation
```

---

## ⚠️ Security Note
- The **whitelist version** is recommended for most cases, as it prevents dangerous commands from being executed.  
- The **unrestricted version** should only be used in controlled environments, as it can run any shell command on your machine.  


