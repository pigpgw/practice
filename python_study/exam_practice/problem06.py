"""문제 6. 메모리 테스트 패턴 생성 (난이도 중상)

## 핵심

**메모리 테스트 패턴을 직접 만들어 보는 것**입니다. 실제 ATE에서 쓰는 패턴 여섯 가지를
코드로 옮깁니다.

| 패턴 | 의미 |
|---|---|
| `MARCH1` | 주소 0부터 차례로 1 을 채우는 마칭 패턴. 주소 i 면 하위 i+1 비트가 1 |
| `MARCH0` | `MARCH1` 의 반대. 주소 i 면 하위 i+1 비트가 0, 나머지는 1 |
| `WALK1` | 주소 i 번 비트만 1, 나머지는 0 (한 비트씩 걸어간다) |
| `WALK0` | 주소 i 번 비트만 0, 나머지는 1 |
| `CHECKER` | 인접 비트가 번갈아 1/0. 짝수 주소는 `1010…`, 홀수 주소는 `0101…` |
| `UNIQUE` | 주소 번호 자체를 값으로 넣는다. 주소 i 면 그 i 를 비트로 표현 |

## 풀이 순서 (⏱ 35분)

1. 설정 파싱 (LEN / COUNT / PATTERN) — 8분
2. `MARCH1` / `MARCH0` — 8분
3. `WALK1` / `WALK0` — 7분
4. `CHECKER` (주소 홀짝) — 6분
5. `UNIQUE` — 6분

> 1~3번만 해도 패턴 생성 기본은 나옵니다.

## 상황

메모리 칩을 검사할 때 주소마다 어떤 값을 넣을지가 테스트 패턴입니다.
같은 값만 계속 넣으면 셀 어레이 간의 간섭(coupling)을 못 잡아내고,
주소를 하나씩 바꿔야 인접 셀 문제를 찾을 수 있습니다.
패턴을 만드는 방법 자체가 테스트 프로그램의 핵심입니다.

`input06.txt`에는 다음 키가 한 줄에 하나씩 있다. `#`으로 시작하는 줄과 빈 줄은 무시한다.

- `LEN <n>`: 벡터 길이 (4~16)
- `COUNT <n>`: 패턴 하나당 생성할 벡터 수 (1~LEN)
- `PATTERN <MARCH1|MARCH0|WALK1|WALK0|CHECKER|UNIQUE>`: 패턴 종류. 여러 번 나올 수 있고 나온 순서대로 생성한다.

문자열의 가장 오른쪽이 bit0이다. `output06.csv`에 `Pattern,Index,Vector` 헤더와 함께 쓴다.

## 패턴 예시 (LEN 8)

```text
MARCH1  →  00000001  00000011  00000111  00001111
MARCH0  →  11111110  11111100  11111000  11110000
WALK1   →  00000001  00000010  00000100  00001000
WALK0   →  11111110  11111101  11111011  11110111
CHECKER →  10101010  01010101  10101010  01010101
UNIQUE  →  00000000  00000001  00000010  00000011
```

## 규칙

1. `LEN` 과 `COUNT` 는 각각 한 번만 나와야 한다. 두 번 나오면 오류다.
2. `PATTERN` 은 한 번 이상 나와야 한다.
3. `PATTERN` 의 값은 `MARCH1`, `MARCH0`, `WALK1`, `WALK0`, `CHECKER`, `UNIQUE` 뿐이다.
4. `COUNT` 는 `LEN` 이하여야 한다. `MARCH1`·`MARCH0` 는 `i+1` 비트가 필요하므로
   `COUNT == LEN` 일 때 마지막 주소가 모든 비트를 채운다.
5. `WALK1`·`WALK0` 는 주소 번호 `i` 번 비트만 건드린다. 나머지 비트는 `0`(WALK1) 또는
   `1`(WALK0) 이다.
6. `CHECKER` 는 주소 번호의 홀짝으로 시작 비트를 정한다.
   짝수 주소는 bit0 이 `0`, 홀수 주소는 bit0 이 `1` 이다.
7. `UNIQUE` 는 주소 번호를 `LEN` 비트에 오른쪽 정렬해서 넣는다.
   주소 번호가 `LEN` 비트를 넘으면 오류다.
8. `LEN` 이 4~16 밖이거나 `COUNT` 가 1~LEN 밖이거나 숫자가 아니면 오류다.
9. 잘못된 입력은 stderr에 `ERROR line N: 이유` 형식으로 출력하고 종료 코드 1을 반환한다.

## 출력

`output06.csv`에 쓴다. `PATTERN` 이 나온 순서대로, 그 안에서 주소 순서대로 생성한다.

```text
Pattern,Index,Vector
MARCH1,0,00000001
MARCH1,1,00000011
MARCH1,2,00000111
MARCH1,3,00001111
```

## 예시

입력 예시:

```text
# 메모리 테스트 패턴 생성
LEN 8
COUNT 4
PATTERN MARCH1
PATTERN WALK1
PATTERN CHECKER
```

출력 (`output06.csv`):

```text
Pattern,Index,Vector
MARCH1,0,00000001
MARCH1,1,00000011
MARCH1,2,00000111
MARCH1,3,00001111
WALK1,0,00000001
WALK1,1,00000010
WALK1,2,00000100
WALK1,3,00001000
CHECKER,0,10101010
CHECKER,1,01010101
CHECKER,2,10101010
CHECKER,3,01010101
```

> 실제 입력 파일 `input06.txt` 는 6종 패턴(MARCH1·MARCH0·WALK1·WALK0·CHECKER·UNIQUE)을
> 전부 넣은 것이다. 출력 행은 예시보다 훨씬 많다.

## 실행

    python3 problem06.py

입력: input06.txt
출력: output06.csv
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

INPUT_PATH = HERE / "input06.txt"
OUTPUT_PATH = HERE / "output06.csv"


def solve() -> int:
    """문제 6. 메모리 테스트 패턴 생성 (난이도 중상)"""
    return 0


if __name__ == "__main__":
    raise SystemExit(solve())
