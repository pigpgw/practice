"""문제 2. 회로 계산: 저항 네트워크와 전압 분배 (난이도 중)


## 핵심

**공식으로 숫자를 계산하는 것**입니다. 직렬/병렬/전압분배 세 가지만.

ATE 보드나 테스트 회로를 만들 때마다 "이 저항값으로 전압이 얼마까지 올라오지",
"저쪽으로 흐르는 전류는 얼마지"를 계산한다. 시험장에 회로 보너스가 붙어 나온다는
얘기가 있고, 스펙을 숫자로 계산해 보는 게 회로 지식을 확인하는 방법이기도 하다.

`input02.txt`에 회로 정의가 한 줄씩 들어 있다. `#` 주석과 빈 줄은 무시한다.

```text
SOURCE 5.0
SERIES 100 220
PARALLEL 1000 1000 500
DIVIDER 1000 2000
```

| 명령 | 의미 |
|---|---|
| `SOURCE <v>` | 회로에 인가되는 전압(V)이다. 계산 명령보다 먼저 나와야 한다. |
| `SERIES <R1> <R2> ...` | 직렬 연결. 합성 저항, 전류, 각 저항에 걸리는 전압을 계산한다. |
| `PARALLEL <R1> <R2> ...` | 병렬 연결. 합성 저항만 계산한다. |
| `DIVIDER <R1> <R2>` | 전압 분배. R1과 R2의 중간 지점 전압을 계산한다. |

계산식은 아래와 같다.

```text
직렬:  Rtotal = R1 + R2 + ...        I = V / Rtotal        Vi = I × Ri
병렬:  Rtotal = 1 / (1/R1 + 1/R2 + ...)
분배:  Rtotal = R1 + R2              Vout = V × R2 / Rtotal
       V1 = V × R1 / Rtotal          V2 = V × R2 / Rtotal
```

1. 계산 명령이 나오기 전에 `SOURCE`가 없으면 오류다.
2. 저항값은 0보다 커야 한다. 0 이하이거나 숫자가 아니면 그 명령은 오류다.
3. `SERIES`는 저항을 2개 이상, `PARALLEL`도 2개 이상, `DIVIDER`는 정확히 2개여야 한다.
   개수가 틀리면 오류다.
4. 저항은 소수 둘째 자리, 전압과 전류는 소수 넷째 자리까지 **사사오입**해서 출력한다.
5. 오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **출력 파일에** 쓴다.

## 풀이 순서 (⏱ 25분)

1. 파일 읽고 `SOURCE` 값 저장 — 5분
2. `SERIES`: 합성저항·전류·각 저항 전압 — 8분
3. `PARALLEL`: `1/R` 합으로 합성저항 — 5분
4. `DIVIDER`: `Vout = V × R2 / (R1 + R2)` — 5분
5. 출력 형식 맞추고 예시와 diff — 2분

> 1~3번만 해도 세 명령의 기본형은 나옵니다.

## 출력

`output02.txt`에 명령마다 한 줄씩 쓴다.

```text
SERIES Rtotal=320.00 I=0.0156 A V=1.5625,3.4375
PARALLEL Rtotal=250.00
DIVIDER Rtotal=3000.00 Vout=3.3333 V V1=1.6667 V2=3.3333
```

## 예시

입력 (`input02.txt`):

```text
# 회로 계산 (직렬 / 병렬 / 전압 분배)
# SOURCE 는 회로에 인가되는 전압입니다. 먼저 한 번 선언합니다.
SOURCE 5.0
SERIES 100 220
PARALLEL 1000 1000 500
DIVIDER 1000 2000
SERIES 0 100
DIVIDER 1000
```

출력 (`output02.txt`):

```text
SERIES Rtotal=320.00 I=0.0156 A V=1.5625,3.4375
PARALLEL Rtotal=250.00
DIVIDER Rtotal=3000.00 Vout=3.3333 V V1=1.6667 V2=3.3333
ERRORS=2
```

직렬 100Ω + 220Ω에 5V를 걸면 `I = 5/320 = 0.015625`고,
각 저항의 전압은 `0.015625 × 100 = 1.5625V`, `0.015625 × 220 = 3.4375V`다.
마지막 두 줄은 저항이 0이거나 저항 개수가 틀린 오류 케이스다.

## 실행

    python3 problem02.py

입력: input02.txt
출력: output02.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input02.txt"
OUTPUT_PATH = HERE / "output02.txt"


def solve() -> int:
    """문제 2. 회로 계산: 저항 네트워크와 전압 분배 (난이도 중)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
