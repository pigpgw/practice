"""문제 15. 바이너리 데이터로그 파서 (난이도 중상)


## 핵심

**바이트 단위로 고정 구조를 읽는 것**입니다. `struct`, little-endian, checksum 검증.

장비 로그가 CSV가 아니라 바이너리로 내려올 때가 있다. 구조를 알아야 읽을 수 있고,
앞부분이 잘렸는지, 값이 깨졌는지도 같이 판단해야 한다.

`input15.bin`은 little-endian 바이너리다. 텍스트가 아니라 바이트 단위로 읽어야 한다.

```text
Header 16 bytes (little-endian):
  4바이트 magic b"TEST", 2바이트 version=1, 2바이트 header_size=16,
  4바이트 record_count, 4바이트 reserved

Record 20 bytes (little-endian):
  4바이트 serial, 1바이트 site, 1바이트 test_id, 1바이트 status(0=PASS,1=FAIL),
  1바이트 reserved, 4바이트 float value, 4바이트 timestamp,
  4바이트 checksum (앞 16바이트 합 mod 2**32)
```

1. magic/version/header_size가 다르거나 파일이 헤더보다 짧으면 종료 코드 1.
2. 레코드가 잘렸으면 종료 코드 1.
3. 파일을 열 수 없으면 종료 코드 1.
4. checksum 불일치, status가 0/1이 아님, value가 NaN/Inf, site가 1~8 밖,
   test_id가 0인 레코드는 건너뛰고 Invalid로 집계한 뒤 계속 진행한다.
5. `Value`가 NaN/Inf인지는 `math.isnan`/`math.isinf`로 확인한다.
6. `Value`는 소수 셋째 자리까지 **사사오입**한다.
7. 헤더의 `record_count`보다 남은 바이트가 많으면 그 부분은 무시한다.
8. `Records`는 헤더의 `record_count` 값이고, `Valid + Invalid = Records`가 되어야 한다.

`input15.bin`이 없으면 `python3 input15_make.py`로 다시 만들 수 있다.

## 풀이 순서 (⏱ 40분)

1. `struct` 로 헤더 읽기 — 10분
2. 레코드 20바이트 해석 — 12분
3. checksum 계산·검증 — 10분
4. NaN/Inf·site 범위 검사 — 8분

> 실전 가중치가 낮습니다. 시간 없으면 3번 뒤로 미루세요.

## 출력

- `output15.csv` — 헤더는 `Serial,Site,Test,Value,Status,Timestamp`다.
- `output15_summary.txt` — 아래 형태다.

```text
Records=8
Valid=4
Invalid=4
Pass=2
Fail=2
```

## 예시

입력 (`input15.bin` 앞부분):

```text
54 45 53 54 01 00 10 00 08 00 00 00 ...
```

출력 (`output15.csv`):

```text
Serial,Site,Test,Value,Status,Timestamp
1001,1,1,1.250,PASS,1000
```

## 실행

    python3 problem15.py

입력: input15.bin
출력: output15.csv
출력: output15_summary.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input15.bin"
OUTPUT_PATH = HERE / "output15.csv"
SUMMARY_PATH = HERE / "output15_summary.txt"


def solve() -> int:
    """문제 15. 바이너리 데이터로그 파서 (난이도 중상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
