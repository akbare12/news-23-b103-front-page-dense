#!/usr/bin/env python3
"""news-23 b103 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.realpath(__file__))
SRC = os.path.join(HERE, "entry.png")
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.realpath(os.path.abspath(out_dir))
    repo_abs = os.path.realpath(HERE)
    if out_dir_abs == repo_abs or out_dir_abs.startswith(repo_abs + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if not os.path.isfile(SRC):
        fail(f"source not found: {SRC}")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        fail(f"source too small: {len(data)} bytes")
    if len(data) > MAX_BYTES:
        fail(f"source over 1 MiB: {len(data)} bytes")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    # first chunk must be IHDR, 13 bytes: 1024x1024, bit depth 8, colour type 2/6
    if len(data) < 33:
        fail("file too short for IHDR")
    ln, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or ln != 13:
        fail("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        fail(f"wrong size: {w}x{h}, expected 1024x1024")
    if depth != 8 or ctype_b not in (2, 6):
        fail(f"unsupported PNG: bit depth {depth}, colour type {ctype_b}")
    if comp != 0 or filt != 0 or inter != 0:
        fail("unsupported PNG: compression/filter/interlace must be 0")
    ihdr_crc_stored, = struct.unpack(">I", data[29:33])
    ihdr_crc_calc = zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF
    if ihdr_crc_calc != ihdr_crc_stored:
        fail("CRC mismatch in IHDR")
    # walk chunks: CRC each, IDAT payload non-empty, IEND last with no trailing data
    pos, idat_total, seen_iend = 8, 0, False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        clen, cname = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 12 + clen
        if end > len(data):
            fail(f"truncated chunk {cname!r}")
        crc_stored, = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])
        crc_calc = zlib.crc32(cname + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            fail(f"CRC mismatch in chunk {cname!r}")
        if cname == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if cname == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if end != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total == 0:
        fail("no IDAT chunk found")
    if idat_total < 1000:
        fail(f"IDAT payload too small: {idat_total} bytes")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.realpath(dst) == os.path.realpath(SRC):
        fail("refusing to overwrite the source image")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("output differs from source after write")
    print(f"wrote {dst} ({len(data)} bytes)")
    print(f"sha256 {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
