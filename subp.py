import io
import subprocess
from pathlib import Path
import sys

source = "a\r\nabc\r\n"

argv = ["python", Path(__file__).parent / "subp_c.py"]

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf8", newline="\n")

process = subprocess.Popen(
    argv,
    encoding="utf-8",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE,
)
stdout, stderr = process.communicate(input=source)

print(stdout, stderr)
