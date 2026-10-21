"""문제 10에서 사용하는 바이너리 데이터로그를 생성한다.

실행:
    python3 input10_make.py

Record layout (little-endian, 20 bytes):
    4바이트 serial
    1바이트 site
    1바이트 test_id
    1바이트 status      (0=PASS, 1=FAIL)
    1바이트 reserved
    4바이트 float value
    4바이트 timestamp
    4바이트 checksum    (앞 16바이트 합 mod 2**32)

The file intentionally contains corrupt records so the parser has to
validate checksum, status, value and site instead of trusting the header.
"""

import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "input10.bin"

HEADER = struct.Struct("<4sHHII")
BODY = struct.Struct("<IBBBBfI")
CHECKSUM = struct.Struct("<I")


def make_record(serial, site, test_id, status, value, timestamp, bad_checksum=False):
    body = BODY.pack(serial, site, test_id, status, 0, value, timestamp)
    checksum = sum(body) & 0xFFFFFFFF
    if bad_checksum:
        checksum = (checksum + 1) & 0xFFFFFFFF
    return body + CHECKSUM.pack(checksum)


def main() -> int:
    records = [
        # serial, site, test, status, value, timestamp, corrupt?
        (1001, 1, 1, 0, 1.25, 1000, False),
        (1002, 2, 1, 1, -0.5, 1001, False),
        (1003, 3, 2, 0, 12.0, 1002, True),   # checksum mismatch
        (1004, 4, 2, 2, 3.3, 1003, False),   # invalid status
        (1005, 5, 3, 0, float("nan"), 1004, False),  # invalid value
        (1006, 6, 3, 1, 0.0, 1005, False),
        (1007, 9, 1, 0, 1.0, 1006, False),   # site out of range
        (1008, 1, 1, 0, 2.5, 1007, False),
    ]

    blob = bytearray(HEADER.pack(b"TEST", 1, HEADER.size, len(records), 0))
    for serial, site, test_id, status, value, timestamp, bad in records:
        blob.extend(make_record(serial, site, test_id, status, value, timestamp, bad))

    OUTPUT.write_bytes(blob)
    print(f"Wrote {OUTPUT} ({len(blob)} bytes, {len(records)} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
