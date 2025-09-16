"""
Linux MCP Server (Whitelist)
----------------------------

This module implements a FastMCP server that executes only whitelisted Linux commands.
It enforces a strict whitelist, argument validation, and safe execution without a shell,
providing a safer way to expose limited system command functionality.

Modules:
    shlex       -- Safely split command strings into argument lists
    shutil      -- Locate system executables in PATH
    subprocess  -- Execute external commands with controlled input/output
    re          -- Regular expressions for argument validation
    typing      -- Type hints for cleaner function definitions
    fastmcp     -- Framework for MCP-compatible servers
"""

import shlex
import shutil
import subprocess
import re
from typing import List
from fastmcp import FastMCP

# Initialize FastMCP application instance
app = FastMCP("Linux MCP Server (whitelist)")

# --- Whitelist of allowed commands (base command names only) ---
# Add or remove commands here as needed.
# Avoid dangerous commands like rm, mv, shutdown, dd, etc.
ALLOWED_COMMANDS = {
    "ls", "cat", "head", "tail", "less", "grep", "egrep", "fgrep", "wc",
    "df", "du", "ps", "top", "uname", "whoami", "id", "uptime", "free",
    "ip", "ifconfig", "ss", "netstat", "journalctl", "systemctl",
    "mount", "umount", "stat", "find", "sed", "awk", "cut", "sort",
    "uniq", "tr", "env", "date", "hostname", "readlink", "file",
    "which", "bash",
}

# --- Validation rules ---
SHELL_META_PATTERN = re.compile(r"[;&|<>$`\\]")  # Disallowed metacharacters
MAX_ARGS = 30                                    # Limit number of args
DEFAULT_TIMEOUT = 10                             # Default command timeout (seconds)


def is_allowed_base(cmd: str) -> bool:
    """
    Check if the base command name is allowed.

    Args:
        cmd (str): Base command name (e.g., 'ls').

    Returns:
        bool: True if the command is in the whitelist, False otherwise.
    """
    return cmd in ALLOWED_COMMANDS


def is_safe_arg(arg: str) -> bool:
    """
    Validate that a command argument is safe.

    Args:
        arg (str): Command argument to validate.

    Returns:
        bool: False if the argument contains unsafe patterns, True otherwise.
    """
    if SHELL_META_PATTERN.search(arg):
        return False
    if re.search(r"\b-exec\b|\b--exec\b", arg):
        return False
    if ".." in arg:
        return False
    if len(arg) > 1024:
        return False
    return True


def split_command(command_text: str) -> List[str]:
    """
    Safely split a command string into a list of arguments.

    Args:
        command_text (str): The command string.

    Returns:
        List[str]: Tokenized command and arguments.
    """
    return shlex.split(command_text)


@app.tool
def run_command(command: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    Run a whitelisted Linux command.

    Args:
        command (str): Full command string, e.g., "ls -la /var/log".
        timeout (int, optional): Seconds before the command is terminated. Defaults to DEFAULT_TIMEOUT.

    Returns:
        str: Command execution result including:
             - STDOUT (if any)
             - STDERR (if any)
             - RETURN CODE
             - Whitelist validation feedback
    """
    try:
        argv = split_command(command)
        if not argv:
            return "ERROR: No command provided."

        base = argv[0]
        base_name = base.split("/")[-1]

        # Validate base command
        if not is_allowed_base(base_name):
            return f"ERROR: Command '{base_name}' is not allowed by server whitelist."

        # Ensure the binary exists
        resolved = shutil.which(base_name)
        if resolved is None:
            return f"ERROR: Command '{base_name}' not found on server PATH."

        # Validate arguments
        args = argv[1:]
        if len(args) > MAX_ARGS:
            return f"ERROR: Too many arguments (limit {MAX_ARGS})."

        for a in args:
            if not is_safe_arg(a):
                return f"ERROR: Unsafe argument detected: {a!s}"

        # Final argv with resolved binary
        final_argv = [resolved] + args

        # Run safely without shell
        proc = subprocess.run(
            final_argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )

        out_lines = []
        if proc.stdout:
            out_lines.append("STDOUT:\n" + proc.stdout.rstrip())
        if proc.stderr:
            out_lines.append("STDERR:\n" + proc.stderr.rstrip())
        out_lines.append(f"RETURN CODE: {proc.returncode}")

        return "\n\n".join(out_lines)

    except subprocess.TimeoutExpired:
        return f"ERROR: Command timed out after {timeout} seconds."
    except Exception as e:
        return f"ERROR: Exception while running command: {e}"


if __name__ == "__main__":
    # Start the MCP server
    app.run()
