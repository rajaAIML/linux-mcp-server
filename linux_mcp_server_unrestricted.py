"""
Linux MCP Server (Unrestricted)
--------------------------------

This module implements a FastMCP-based server that allows unrestricted execution of Linux shell
commands via a registered tool. It provides an interface to run any command without a whitelist, 
making it useful for debugging, system inspection, and automation tasks. However, due to its 
unrestricted nature, it should only be used in controlled environments.

Modules:
    subprocess: Used to execute shell commands securely with output and error capturing.
    fastmcp: Provides the FastMCP framework for building MCP-compatible servers.
"""

import subprocess
from fastmcp import FastMCP, tools

# Initialize FastMCP application instance
app = FastMCP("Linux MCP Server (Unrestricted)")


@app.tool()
def run_command(command: str, timeout: int = 15) -> str:
    """
    Execute a Linux shell command without a whitelist restriction.

    This function runs any given Linux shell command in a subprocess with support
    for pipes, redirects, and background operators. Both standard output and 
    error streams are captured and returned along with the command's exit code.

    Args:
        command (str): 
            The shell command to execute. 
            Examples:
                - "ls -la /"
                - "df -h"
                - "ps aux | grep python"
        timeout (int, optional): 
            Maximum execution time for the command in seconds. 
            Defaults to 15 seconds.

    Returns:
        str: 
            A formatted string containing:
            - Command STDOUT (if any)
            - Command STDERR (if any)
            - The return code of the executed command

            Example output:
            ```
            STDOUT:
            file1.txt
            file2.txt

            STDERR:
            ls: cannot access 'missing.txt': No such file or directory

            RETURN CODE: 2
            ```

    Raises:
        Exception: If an unexpected error occurs during execution.
        subprocess.TimeoutExpired: If the command exceeds the specified timeout.

    Notes:
        - Since shell=True is enabled, this function supports advanced shell 
          features (pipes, redirects, etc.).
        - For security reasons, do not expose this tool to untrusted users or 
          production environments without additional safeguards.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,                   # Allows pipes, redirects, and shell features
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )

        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        output += f"RETURN CODE: {result.returncode}"

        return output.strip()

    except subprocess.TimeoutExpired:
        return f"ERROR: Command timed out after {timeout} seconds."
    except Exception as e:
        return f"ERROR: {e}"


if __name__ == "__main__":
    # Run the MCP server
    app.run()
