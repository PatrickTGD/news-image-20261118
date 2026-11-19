"""make.fun entry: news-image-20261118.

Copies the finished news image (entry.png, shipped in this repository)
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library
only, no network; two runs write identical bytes.
"""

import os


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
