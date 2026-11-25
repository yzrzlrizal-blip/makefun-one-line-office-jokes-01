"""One-line office joke entry for make.fun.

Writes a single original one-line joke about office life to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Pure standard library only.
"""

import os
import sys

JOKE = 'I put "per my last email" in my will so my family knows I tried.'

MAX_CHARS = 199


def validate(line):
    """Check the joke meets the competition gate."""
    if not isinstance(line, str):
        raise ValueError("joke must be text")
    if not line.strip():
        raise ValueError("joke must not be only whitespace")
    if len(line) != len(line.strip()):
        raise ValueError("joke must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("joke must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError("joke is %d chars, over the %d limit" % (len(line), MAX_CHARS))
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("joke must not contain control characters")
    return line


def main():
    line = validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    data = line.encode("utf-8")
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, target)
    with open(target, "rb") as fh:
        written = fh.read()
    if written != data:
        raise SystemExit("verification failed: entry.txt does not match")
    print("wrote %d chars (%d bytes) to %s" % (len(line), len(data), target))
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
