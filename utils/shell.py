import subprocess


class ShellError(RuntimeError):
    def __init__(self, cmd, returncode, stderr):
        super().__init__(f"Command failed ({returncode}): {' '.join(cmd)}\n{stderr}")
        self.cmd = cmd
        self.returncode = returncode
        self.stderr = stderr


def run(cmd: list[str], timeout: int = 3600) -> str:
    """Run a command, raise ShellError on non-zero exit, return stdout."""
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout
    )
    if proc.returncode != 0:
        raise ShellError(cmd, proc.returncode, proc.stderr)
    return proc.stdout