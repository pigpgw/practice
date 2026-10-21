"""문제 5. 고정 크기 링 버퍼 (난이도 중)


## 핵심

**가장 오래된 값을 밀어내는 고정 크기 버퍼**입니다. 덮어쓴 값을 출력에 함께 넣는 게 핵심.

## 풀이 순서 (⏱ 30분)

1. `CAP` 으로 버퍼 크기 지정 — 5분
2. `ADD`: 가득 찼으면 오래된 값 덮어쓰고 그 값 출력 — 10분
3. `STATS`: count/min/max/avg/overwrites — 10분
4. `DUMP`: 오래된 것부터, 빈 버퍼는 `(empty)` — 5분

> 2번까지만 해도 `ADD` 처리(덮어쓰기 + 출력)는 나옵니다.

## 상황

ATE에서 측정한 샘플은 최근 N개만 기억하면 된다. 그래서 크기가 고정된 버퍼를 두고
새 값이 들어올 때마다 가장 오래된 값을 버리는 방식을 씁니다. 실제 테스트 프로그램에도
넓게 쓰이는 구조라 직접 만들어 보시길 권한다.

## 입력

`input05.txt`에 명령이 한 줄씩 들어 있다. `#`으로 시작하는 줄과 빈 줄은 무시한다.

```text
CAP 5
ADD 10.0
STATS
DUMP
```

| 명령 | 의미 |
|---|---|
| `CAP <n>` | 용량 n으로 버퍼를 만든다. 내용과 overwrite 횟수를 초기화한다. |
| `ADD <v>` | 값을 추가한다. 가득 차 있으면 가장 오래된 값을 덮어쓰고 그 값을 함께 출력한다. |
| `STATS` | `STATS count=.. min=.. max=.. avg=.. overwrites=..` 형식으로 요약한다. |
| `DUMP` | 오래된 값부터 공백으로 구분해 출력한다. 비어 있으면 `DUMP (empty)`. |
| `CLEAR` | 내용과 overwrite 횟수를 초기화한다. |

## 처리 규칙

1. `CAP`이 먼저 있어야 한다. `CAP` 전의 `ADD`는 오류이다.
2. 용량(`CAP`)은 1~100만 허용한다. 범위 밖이면 오류이고 버퍼는 그대로 둔다.
3. 덮어썼다면 `ADD 60.00 (overwrite 10.00)` 형식으로 출력한다.
4. 값은 소수 둘째 자리까지 **사사오입**해서 출력한다. `avg`도 같은 방식으로 반올림한다.
5. `STATS`의 `min`/`max`/`avg`는 **보관된 원본 값**으로 계산하고 마지막에 반올림한다.
6. `CLEAR`는 `CLEAR` 한 줄만 출력하고, 내용과 overwrite 횟수를 초기화한다.
   `CAP`이 아직 없으면 `CLEAR`는 오류이다.
7. 빈 버퍼에서 `DUMP`는 `DUMP (empty)`, `STATS`는
   `STATS count=0 min=0.00 max=0.00 avg=0.00 overwrites=0`을 출력한다.
8. 잘못된 값, 범위 밖 capacity, 알 수 없는 명령은 오류로 세고 계속 진행한다.
   오류는 stderr에 `ERROR line N: 이유` 형식으로 출력하고, 마지막 줄에 `ERRORS=n`을
   **출력 파일에** 씁니다.

## 출력

`output05.txt`에 씁니다.

## 예시

입력 (`input05.txt`):

```text
CAP 3
ADD 10
ADD 20
ADD 30
ADD 40
STATS
DUMP
```

출력 (`output05.txt`):

```text
CAP=3
ADD 10.00
ADD 20.00
ADD 30.00
ADD 40.00 (overwrite 10.00)
STATS count=3 min=20.00 max=40.00 avg=30.00 overwrites=1
DUMP 20.00 30.00 40.00
ERRORS=0
```

## 실행

    python3 problem05.py

입력: input05.txt
출력: output05.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input05.txt"
OUTPUT_PATH = HERE / "output05.txt"


def solve() -> int:
    """문제 5. 고정 크기 링 버퍼 (난이도 중)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
